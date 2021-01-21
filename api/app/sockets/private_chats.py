"""This module contains socketio event handlers for private chats."""


import json
from datetime import datetime
from uuid import uuid4
from http import HTTPStatus
from flask import g, current_app, url_for
from flask_socketio import emit, join_room, leave_room
from app.sockets.helpers import send_private_chat_notifications
from app.extensions import socketio
from app.repositories import dynamodb_repository
from app.decorators.auth import socketio_jwt_required, socketio_permission_required
from app.decorators.views import socketio_handle_arguments
from app.models import TokenType, Message, MessageType, RolePermission
from app.schemas import PrivateChatMessageSchema, PrivateChatSchema


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(PrivateChatMessageSchema(partial=["_id"]))
def create_private_chat_message(message_data, message_schema):
    """Create a new private chat message."""
    private_chat = dynamodb_repository.get_private_chat(message_data["_chat_id"])
    if not private_chat:
        emit("error", json.dumps({"error": "Private chat not found"}))
    elif not g.current_user.in_room(private_chat.id):
        emit("error", json.dumps({"error": "User has not joined the private chat"}))
    else:
        now = datetime.now()
        # Create new message
        chat_message = Message(
            now.isoformat() + "-" + uuid4().hex,
            message_data["_chat_id"],
            g.current_user.id,
            message_data["_content"],
            MessageType.PRIVATE_CHAT,
        )
        dynamodb_repository.add_chat_message(chat_message)
        # When should the message be confirmed as sent?
        emit(
            "new_chat_message",
            message_schema.dumps(chat_message),
            room=chat_message.chat_id,
        )
        target_url = url_for(
            "api.get_private_chat_message",
            private_chat_id=private_chat.id,
            message_id=chat_message.id,
        )
        socketio.start_background_task(
            send_private_chat_notifications, target_url,
            g.current_user, chat_message, private_chat
        )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_handle_arguments(PrivateChatSchema(only=["_id"]))
def join_private_chat(private_chat_data, chat_schema):
    """Add a user to a socketio room. Rooms are identified by private chat ids."""
    private_chat = dynamodb_repository.get_private_chat(private_chat_data["_id"])
    if not private_chat:
        emit("error", json.dumps({"error": "Private chat not found"}))
    else:
        g.current_user.add_room(private_chat.id)
        dynamodb_repository.update_user(g.current_user, {"rooms": g.current_user.rooms})
        join_room(private_chat.id)
        emit(
            "joined_private_chat",
            json.dumps({"message": f"{g.current_user.username} has entered the chat!"}),
            room=private_chat.id,
        )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_handle_arguments(PrivateChatSchema(only=["_id"]))
def leave_private_chat(private_chat_data, chat_schema):
    """Remove a user from a socketio room. Roomas are identified by private chat ids."""
    private_chat = dynamodb_repository.get_private_chat(private_chat_data["_id"])
    if not private_chat:
        emit("error", json.dumps({"error": "Private chat not found"}))
    elif not g.current_user.in_room(private_chat.id):
        emit("error", json.dumps({"error": "User has not joined this private chat"}))
    else:
        g.current_user.remove_room(private_chat.id)
        dynamodb_repository.update_user(g.current_user, {"rooms": g.current_user.rooms})
        leave_room(private_chat.id)
        emit(
            "left_private_chat",
            json.dumps({"message": f"{g.current_user.username} has left the chat"}),
            room=private_chat.id,
        )
