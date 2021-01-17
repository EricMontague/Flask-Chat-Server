"""This module contains socketio event handlers for private chats."""


import json
from hashlib import md5
from datetime import datetime
from uuid import uuid4
from json.decoder import JSONDecodeError
from http import HTTPStatus
from flask import current_app, g, render_template, request, url_for
from flask_socketio import send, emit, join_room, leave_room, disconnect
from app.sockets import sockets
from app.extensions import socketio
from app.repositories import dynamodb_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.decorators.auth import socketio_jwt_required
from app.models import TokenType, Message, Notification, NotificationType, Reaction, ReactionType
from app.schemas import PrivateChatMessageSchema, NotificationSchema, ReactionSchema
from marshmallow import ValidationError


# TODO - Validate that the current user is connected to the room before creating the message
@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def create_private_chat_message(data):
    """Create a new private chat message."""
    message_schema = PrivateChatMessageSchema(partial=["_id"])
    notification_schema = NotificationSchema()
    try:
        message_data = message_schema.loads(data)
    except ValidationError as err:
        emit("error", json.dumps({"error": err.messages}))
    else:
        private_chat = dynamodb_repository.get_private_chat(message_data["_chat_id"])
        if not private_chat:
            emit("error", json.dumps({"error": "Private chat not found"}))
        else:
            now = datetime.now()
            # Create new message
            chat_message = Message(
                now.isoformat() + "-" + uuid4().hex, 
                message_data["_chat_id"], 
                g.current_user.id, 
                message_data["_content"]
            )
            dynamodb_repository.add_private_chat_message(chat_message)
            # When should the message be confirmed as sent?
            emit(
                "new_chat_message",
                message_schema.dumps(chat_message),
                room=chat_message.chat_id
            )

            other_user = private_chat.get_other_user(g.current_user.id)
            notification = Notification(
                now.isoformat() + "-" + uuid4().hex,
                other_user.id,
                NotificationType.NEW_PRIVATE_CHAT_MESSAGE,
                f"{g.current_user.username} sent you a new message",
                url_for(
                    "api.get_private_chat_message", 
                    private_chat_id=chat_message.chat_id,
                    message_id=chat_message.id
                ),
            )
            dynamodb_repository.add_user_notification(notification)
            if other_user.socketio_session_id:
                emit(
                    "new_notification",
                    notification_schema.dumps(notification),
                    room=other_user.socketio_session_id
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def update_private_chat_message(data):
    """Update the content of a private chat message."""
    message_schema = PrivateChatMessageSchema()
    try:
        message_data = message_schema.loads(data)
    except ValidationError as err:
        emit("error", json.dumps({"error": err.messages}))
    else:
        chat_message = dynamodb_repository.get_private_chat_message(
            message_data["_chat_id"], message_data["_id"]
        )
        if not chat_message:
            emit("error", json.dumps({"error": "Private chat message not found"}))
        elif chat_message.user_id != g.current_user.id:
            emit("error", json.dumps({"error": "User is not the sender of this message"}))
        else:
            chat_message.edit(message_data["_content"])
            dynamodb_repository.add_private_chat_message(chat_message)
            emit(
                "chat_message_editted",
                message_schema.dumps(chat_message),
                room=chat_message.chat_id
            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def delete_private_chat_message(data):
    """Delete an existing private chat message."""
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        private_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        if not private_chat_id:
            emit("error", json.dumps({"error": "Missing private chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        else:
            chat_message = dynamodb_repository.get_private_chat_message(
                private_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Private chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                dynamodb_repository.remove_private_chat_message(chat_message)
                emit(
                    "chat_message_deleted",
                    json.dumps({"message_id": chat_message.id, "resource_type": "PrivateChatMessage"}),
                    room=chat_message.chat_id
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def react_to_private_chat_message(data):
    """Add a new reaction to a private chat message."""
    reaction_schema = ReactionSchema()
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        private_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        reaction_type = payload.get("reaction_type")
        if not private_chat_id:
            emit("error", json.dumps({"error": "Missing private chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        elif not reaction_type:
            emit("error", json.dumps({"error": "Missing reaction type in event data"}))
        elif reaction_type.upper() not in {type_.name for type_ in ReactionType}:
            emit("error", json.dumps({"error": f"{reaction_type} not a valid reaction type"}))
        else:
            chat_message = dynamodb_repository.get_private_chat_message(
                private_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Private chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                reaction = Reaction(g.current_user.id, ReactionType[reaction_type.upper()])
                chat_message.add_reaction(reaction)
                dynamodb_repository.add_private_chat_message(chat_message)
                emit(
                    "new_chat_message_reaction",
                    json.dumps({
                        "reaction": reaction_schema.dumps(reaction),
                        "message_id": chat_message.id,
                        "resource_type": "PrivateChatMessage"
                    }),
                    room=chat_message.chat_id,
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def unreact_to_private_chat_message(data):
    """Remove a reaction from a private chat message."""
    reaction_schema = ReactionSchema()
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        private_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        if not private_chat_id:
            emit("error", json.dumps({"error": "Missing private chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        else:
            chat_message = dynamodb_repository.get_private_chat_message(
                private_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Private chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                reaction = chat_message.remove_reaction(g.current_user.id)
                if not reaction:
                    emit("error", json.dumps({"error": "User has not yet reacted to this message"}))
                else:
                    dynamodb_repository.add_private_chat_message(chat_message)
                    emit(
                        "removed_chat_message_reaction",
                        json.dumps({
                            "reaction": reaction_schema.dumps(reaction),
                            "message_id": chat_message.id,
                            "resource_type": "PrivateChatMessage"
                        }),
                        room=chat_message.chat_id,
                    )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def join_private_chat(data):
    """Add a user to a socketio room. Rooms are identified by private chat ids."""
    payload = json.loads(data)
    private_chat_id = payload.get("private_chat_id")
    if not private_chat_id:
        emit("error", json.dumps({"error": "Missing private chat id in event data"}))
    else:
        private_chat = dynamodb_repository.get_private_chat(private_chat_id)
        if not private_chat:
            emit("error", json.dumps({"error": "Private chat not found"}))
        else:
            join_room(private_chat.id)
            emit(
                "joined_private_chat", 
                json.dumps({"message": f"{g.current_user.username} has entered the chat!"}),
                room=private_chat.id
            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def leave_private_chat(data):
    """Remove a user from a socketio room. Roomas are identified by private chat ids."""
    payload = json.loads(data)
    private_chat_id = payload.get("private_chat_id")
    if not private_chat_id:
        emit("error", json.dumps({"error": "Missing private chat id in event data"}))
    else:
        private_chat = dynamodb_repository.get_private_chat(private_chat_id)
        if not private_chat:
            emit("error", json.dumps({"error": "Private chat not found"}))
        else:
            leave_room(private_chat.id)
            emit(
                "left_private_chat", 
                json.dumps({"message": f"{g.current_user.username} has left the chat"}),
                room=private_chat.id
            )