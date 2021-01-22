"""This module contains socketio event handlers for chat messages."""


import json
from flask import g
from flask_socketio import emit
from app.extensions import socketio
from app.decorators.auth import socketio_jwt_required, socketio_permission_required
from app.decorators.views import socketio_handle_arguments
from app.models import TokenType, RolePermission, Reaction, MessageType
from app.schemas import GroupChatMessageSchema, PrivateChatMessageSchema, MessageSchema, ReactionSchema
from app.repositories import database_repository


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(MessageSchema())
def update_chat_message(message_data, message_schema):
    """Update the content of a chat message."""
    chat_message = database_repository.get_chat_message(
        message_data["_chat_id"], message_data["_id"], message_data["message_type"]
    )
    if not chat_message:
        emit("error", json.dumps({"error": "Chat message not found"}))
    elif chat_message.user_id != g.current_user.id:
        emit("error", json.dumps({"error": "User is not the sender of this message"}))
    elif not g.current_user.in_room(chat_message.chat_id):
        emit("error", json.dumps({"error": "User has not joined the chat"}))
    else:
        chat_message.edit(message_data["_content"])
        database_repository.add_chat_message(chat_message)
        if chat_message.message_type == MessageType.PRIVATE_CHAT:
            schema = PrivateChatMessageSchema()
        else:
            schema = GroupChatMessageSchema()
        emit(
            "chat_message_editted",
            schema.dumps(chat_message),
            room=chat_message.chat_id
        )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(MessageSchema(only=["_id", "_chat_id", "message_type"]))
def delete_chat_message(message_data, message_schema):
    """Delete an existing chat message."""
    chat_message = database_repository.get_chat_message(
        message_data["_chat_id"], message_data["_id"], message_data["message_type"]
    )
    if not chat_message:
        emit("error", json.dumps({"error": "Chat message not found"}))
    elif chat_message.user_id != g.current_user.id:
        emit("error", json.dumps({"error": "User is not the sender of this message"}))
    elif not g.current_user.in_room(chat_message.chat_id):
        emit("error", json.dumps({"error": "User has not joined the chat"}))
    else:
        database_repository.remove_chat_message(chat_message)
        emit(
            "chat_message_deleted",
            json.dumps({"message_id": chat_message.id, "message_type": message_data["message_type"].name}),
            room=chat_message.chat_id
        )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(ReactionSchema())
def react_to_chat_message(reaction_data, reaction_schema):
    """Add a new reaction to a group chat message."""
    chat_message = database_repository.get_chat_message(
        reaction_data["chat_id"], reaction_data["message_id"], reaction_data["message_type"]
    )
    if not chat_message:
        emit("error", json.dumps({"error": "Chat message not found"}))
    elif not g.current_user.in_room(chat_message.chat_id):
        emit("error", json.dumps({"error": "User has not joined the chat"}))
    else:
        reaction = Reaction(g.current_user.id, reaction_data["reaction_type"])
        chat_message.add_reaction(reaction)
        database_repository.add_chat_message(chat_message)
        emit(
            "new_chat_message_reaction",
            reaction_schema.dumps(reaction),
            room=chat_message.chat_id,
        )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
@socketio_permission_required(RolePermission.WRITE_CHAT_MESSAGE)
@socketio_handle_arguments(ReactionSchema(partial=["reaction_type"]))
def unreact_to_chat_message(reaction_data, reaction_schema):
    """Remove a reaction from a chat message."""
    chat_message = database_repository.get_chat_message(
        reaction_data["chat_id"], reaction_data["message_id"], reaction_data["message_type"]
    )
    if not chat_message:
        emit("error", json.dumps({"error": "Chat message not found"}))
    elif not g.current_user.in_room(chat_message.chat_id):
        emit("error", json.dumps({"error": "User has not joined the chat"}))
    else:
        reaction = chat_message.remove_reaction(g.current_user.id)
        if not reaction:
            emit("error", json.dumps({"error": "User has not yet reacted to this message"}))
        else:
            database_repository.add_chat_message(chat_message)
            emit(
                "removed_chat_message_reaction",
                reaction_schema.dumps(reaction),
                room=chat_message.chat_id,
            )



    