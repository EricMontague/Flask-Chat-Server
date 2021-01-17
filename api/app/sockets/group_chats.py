"""This module contains socketio event handlers for group chats."""


import json
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
from app.schemas import GroupChatMessageSchema, NotificationSchema, ReactionSchema
from marshmallow import ValidationError


@sockets.route("/testing_chat")
def testing_chat():
    return render_template("chat.html")


# TODO - Validate that the current user is connected to the room before creating the message
@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def create_group_chat_message(data):
    """Create a new group chat message."""
    message_schema = GroupChatMessageSchema(partial=["_id"])
    notification_schema = NotificationSchema()
    try:
        message_data = message_schema.loads(data)
    except ValidationError as err:
        emit("error", json.dumps({"error": err.messages}))
    else:
        group_chat = dynamodb_repository.get_group_chat(message_data["community_id"], message_data["_chat_id"])
        if not group_chat:
            emit("error", json.dumps({"error": "Group chat not found"}))
        else:
            member = dynamodb_repository.get_group_chat_member(message_data["_chat_id"], g.current_user.id)
            if not member:
                emit("error", json.dumps({"error": "User is not a member of this group chat"}))
            else:
                now = datetime.now()
                # Create new message
                chat_message = Message(
                    now.isoformat() + "-" + uuid4().hex, 
                    message_data["_chat_id"], 
                    g.current_user.id, 
                    message_data["_content"]
                )
                dynamodb_repository.add_group_chat_message(chat_message)
                # When should the message be confirmed as sent?
                emit(
                    "new_chat_message",
                    message_schema.dumps(chat_message),
                    room=chat_message.chat_id
                )
                limit = 25
                results = dynamodb_repository.get_group_chat_members(
                    message_data["community_id"], message_data["_chat_id"], limit
                )
                for member in results["models"]:
                    if member.id != g.current_user.id:
                        notification = Notification(
                            now.isoformat() + "-" + uuid4().hex,
                            member.id,
                            NotificationType.NEW_GROUP_CHAT_MESSAGE,
                            f"{g.current_user.username} posted a new message in {group_chat.name}",
                            url_for(
                                "api.get_group_chat_message", 
                                group_chat_id=chat_message.chat_id, 
                                message_id=chat_message.id
                            ),
                        )
                        dynamodb_repository.add_user_notification(notification)
                        if member.socketio_session_id:
                            emit(
                                "new_notification",
                                notification_schema.dumps(notification),
                                room=member.socketio_session_id
                            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def update_group_chat_message(data):
    """Update the content of a group chat message."""
    message_schema = GroupChatMessageSchema()
    try:
        message_data = message_schema.loads(data)
    except ValidationError as err:
        emit("error", json.dumps({"error": err.messages}))
    else:
        chat_message = dynamodb_repository.get_group_chat_message(
            message_data["_chat_id"], message_data["_id"]
        )
        if not chat_message:
            emit("error", json.dumps({"error": "Group chat message not found"}))
        elif chat_message.user_id != g.current_user.id:
            emit("error", json.dumps({"error": "User is not the sender of this message"}))
        else:
            chat_message.edit(message_data["_content"])
            dynamodb_repository.add_group_chat_message(chat_message)
            emit(
                "chat_message_editted",
                message_schema.dumps(chat_message),
                room=chat_message.chat_id
            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def delete_group_chat_message(data):
    """Delete an existing group chat message."""
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        group_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        if not group_chat_id:
            emit("error", json.dumps({"error": "Missing group chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        else:
            chat_message = dynamodb_repository.get_group_chat_message(
                group_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Group chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                dynamodb_repository.remove_group_chat_message(chat_message)
                emit(
                    "chat_message_deleted",
                    json.dumps({"message_id": chat_message.id, "resource_type": "GroupChatMessage"}),
                    room=chat_message.chat_id
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def react_to_group_chat_message(data):
    """Add a new reaction to a group chat message."""
    reaction_schema = ReactionSchema()
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        group_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        reaction_type = payload.get("reaction_type")
        if not group_chat_id:
            emit("error", json.dumps({"error": "Missing group chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        elif not reaction_type:
            emit("error", json.dumps({"error": "Missing reaction type in event data"}))
        elif reaction_type.upper() not in {type_.name for type_ in ReactionType}:
            emit("error", json.dumps({"error": f"{reaction_type} not a valid reaction type"}))
        else:
            chat_message = dynamodb_repository.get_group_chat_message(
                group_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Group chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                reaction = Reaction(g.current_user.id, ReactionType[reaction_type.upper()])
                chat_message.add_reaction(reaction)
                dynamodb_repository.add_group_chat_message(chat_message)
                emit(
                    "new_chat_message_reaction",
                    json.dumps({
                        "reaction": reaction_schema.dumps(reaction),
                        "message_id": chat_message.id,
                        "resource_type": "GroupChatMessage"
                    }),
                    room=chat_message.chat_id,
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def unreact_to_group_chat_message(data):
    """Remove a reaction from a group chat message."""
    reaction_schema = ReactionSchema()
    try:
        payload = json.loads(data)
    except (TypeError, JSONDecodeError):
        emit("error", json.dumps({"error": "Missing JSON body in event data"}))
    else:
        group_chat_id = payload.get("chat_id")
        message_id = payload.get("message_id")
        reaction_type = payload.get("reaction_type")
        if not group_chat_id:
            emit("error", json.dumps({"error": "Missing group chat id in event data"}))
        elif not message_id:
            emit("error", json.dumps({"error": "Missing chat message id in event data"}))
        else:
            chat_message = dynamodb_repository.get_group_chat_message(
                group_chat_id, message_id
            )
            if not chat_message:
                emit("error", json.dumps({"error": "Group chat message not found"}))
            elif chat_message.user_id != g.current_user.id:
                emit("error", json.dumps({"error": "User is not the sender of this message"}))
            else:
                reaction = chat_message.remove_reaction(g.current_user.id)
                if not reaction:
                    emit("error", json.dumps({"error": "User has not yet reacted to this message"}))
                else:
                    dynamodb_repository.add_group_chat_message(chat_message)
                    emit(
                        "removed_chat_message_reaction",
                        json.dumps({
                            "reaction": reaction_schema.dumps(reaction),
                            "message_id": chat_message.id,
                            "resource_type": "GroupChatMessage"
                        }),
                        room=chat_message.chat_id,
                    )

@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def join_group_chat(data):
    """Add a user to a socketio room. Rooms are identified by group chat ids."""
    payload = json.loads(data)
    group_chat_id = payload.get("group_chat_id")
    community_id = payload.get("community_id")
    if not group_chat_id:
        emit("error", json.dumps({"error": "Missing group chat id in event data"}))
    elif not community_id:
        emit("error", json.dumps({"error": "Missing community id in event data"}))
    else:
        group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
        if not group_chat:
            emit("error", json.dumps({"error": "Group chat not found"}))
        else:
            member = dynamodb_repository.get_group_chat_member(group_chat_id, g.current_user.id)
            if not member:
                emit("error", json.dumps({"error": "User is not a member of this group chat"}))    
            else:
                join_room(group_chat_id)
                emit(
                    "joined_group_chat", 
                    json.dumps({"message": f"{g.current_user.username} has entered the chat!"}),
                    room=group_chat_id
                )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def leave_group_chat(data):
    """Remove a user from a socketio room. Roomas are identified by group chat ids."""
    payload = json.loads(data)
    group_chat_id = payload.get("group_chat_id")
    community_id = payload.get("community_id")
    if not group_chat_id:
        emit("error", json.dumps({"error": "Missing group chat id in event data"}))
    elif not community_id:
        emit("error", json.dumps({"error": "Missing community id in event data"}))
    else:
        group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
        if not group_chat:
            emit("error", json.dumps({"error": "Group chat not found"}))
        else:
            member = dynamodb_repository.get_group_chat_member(group_chat_id, g.current_user.id)
            if not member:
                emit("error", json.dumps({"error": "User is not a member of this group chat"}))
            else:
                leave_room(group_chat_id)
                emit(
                    "left_group_chat", 
                    json.dumps({"message": f"{g.current_user.username} has left the chat"}),
                    room=group_chat_id
                )
    

@socketio.on("connect")
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def connect_handler():
    """Establish a connection from the client to the server.
    The user's session is saved in the database for as long as the 
    connection is alive.
    """
    dynamodb_repository.update_user(
        g.current_user, {"socketio_session_id": request.sid, "is_online": True}
    )
    print(f"{g.current_user.username} connected to server!")


@socketio.on("disconnect")
def disconnect_handler():
    """Remove the user's session id from the database and do any other
    necessary cleanup when the client disconnects from the server.
    """
    dynamodb_repository.update_user(
        g.current_user, {"socketio_session_id": "", "is_online": False}
    )
    