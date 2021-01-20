"""This module contains socketio event handlers for group chats."""


import json
from datetime import datetime
from uuid import uuid4
from http import HTTPStatus
from flask import g
from flask_socketio import emit, join_room, leave_room
from app.sockets.helpers import send_group_chat_notifications
from app.extensions import socketio
from app.repositories import dynamodb_repository
from app.decorators.auth import socketio_jwt_required, socketio_permission_required
from app.decorators.views import socketio_handle_arguments
from app.models import TokenType, Message, MessageType, RolePermission
from app.schemas import GroupChatMessageSchema, GroupChatSchema


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(GroupChatMessageSchema(partial=["_id"]))
def create_group_chat_message(message_data, message_schema):
    """Create a new group chat message."""
    group_chat = dynamodb_repository.get_group_chat(message_data["community_id"], message_data["_chat_id"])
    if not group_chat:
        emit("error", json.dumps({"error": "Group chat not found"}))
    else:
        member = dynamodb_repository.get_group_chat_member(message_data["_chat_id"], g.current_user.id)
        if not member:
            emit("error", json.dumps({"error": "User is not a member of this group chat"}))
        elif not member.in_room(group_chat.id):
            emit("error", json.dumps({"error": "User has not joined the group chat"})) 
        else:
            now = datetime.now()
            # Create new message
            chat_message = Message(
                now.isoformat() + "-" + uuid4().hex, 
                message_data["_chat_id"], 
                g.current_user.id, 
                message_data["_content"],
                MessageType.GROUP_CHAT
            )
            dynamodb_repository.add_chat_message(chat_message)

            # When should the message be confirmed as sent?
            emit(
                "new_chat_message",
                message_schema.dumps(chat_message),
                room=chat_message.chat_id
            )

            socketio.start_background_task(
                send_group_chat_notifications, dynamodb_repository, chat_message, group_chat
            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.READ_CHAT_MESSAGE)
@socketio_handle_arguments(GroupChatSchema(only=["_id", "_community_id"]))
def join_group_chat(group_chat_data, chat_schema):
    """Add a user to a socketio room. Rooms are identified by group chat ids."""
    group_chat_id = group_chat_data["_id"]
    community_id = group_chat_data["_community_id"]
    group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
    if not group_chat:
        emit("error", json.dumps({"error": "Group chat not found"}))
    else:
        member = dynamodb_repository.get_group_chat_member(group_chat_id, g.current_user.id)
        if not member:
            emit("error", json.dumps({"error": "User is not a member of this group chat"}))    
        else:
            member.add_room(group_chat_id)
            dynamodb_repository.update_user(member, {"rooms": member.rooms})
            join_room(group_chat_id)
            emit(
                "joined_group_chat", 
                json.dumps({"message": f"{g.current_user.username} has entered the chat!"}),
                room=group_chat_id
            )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_handle_arguments(GroupChatSchema(only=["_id", "_community_id"]))
def leave_group_chat(group_chat_data, chat_schema):
    """Remove a user from a socketio room. Roomas are identified by group chat ids."""
    group_chat_id = group_chat_data["_id"]
    community_id = group_chat_data["_community_id"]
    group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
    if not group_chat:
        emit("error", json.dumps({"error": "Group chat not found"}))
    else:
        member = dynamodb_repository.get_group_chat_member(group_chat_id, g.current_user.id)
        if not member:
            emit("error", json.dumps({"error": "User is not a member of this group chat"}))
        elif not member.in_room(group_chat_id):
            emit("error", json.dumps({"error": "User has not joined this group chat"}))
        else:
            member.remove_room(group_chat_id)
            dynamodb_repository.update_user(member, {"rooms": member.rooms})
            leave_room(group_chat_id)
            emit(
                "left_group_chat", 
                json.dumps({"message": f"{g.current_user.username} has left the chat"}),
                room=group_chat_id
            )



