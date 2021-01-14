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
from app.models import TokenType, Message, Notification, NotificationType
from app.schemas import GroupChatMessageSchema, NotificationSchema
from marshmallow import ValidationError


@sockets.route("/testing_chat")
def testing_chat():
    return render_template("chat.html")


# Socket - Creates a notification too
# @api.route("/group_chats/<group_chat_id>/messages", methods=["POST"])
@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def create_group_chat_message(data):
    message_schema = GroupChatMessageSchema()
    notification_schema = NotificationSchema()
    try:
        message_data = message_schema.loads(data)
    except ValidationError as err:
        emit("error", json.dumps(err))
    else:
        community_membership = dynamodb_repository.get_community_membership(message_data["community_id"], g.current_user.id)
        if not community_membership:
            emit("error", json.dumps({"error": "User is not a member of this community"}))
        else:
            group_chat = dynamodb_repository.get_group_chat(message_data["community_id"], message_data["chat_id"])
            if not group_chat:
                emit("error", json.dumps({"error": "Group chat not found"}))
            else:
                # Create new message
                chat_message = Message(
                    message_data["_id"], 
                    message_data["_chat_id"], 
                    g.current_user.id, 
                    message_data["_content"]
                )
                dynamodb_repository.add_private_chat_message(chat_message)
                emit(
                    "new_group_chat_message",
                    message_schema.dump(chat_message),
                    room=chat_message.chat_id
                )

                # Create new notification. How do I get all users in this room so I
                # can save this in dynamodb for all of them?
                now = datetime.now()
                notification = Notification(
                    now.isoformat() + "-" + uuid4(),
                    g.current_user.id,
                    NotificationType.NEW_GROUP_CHAT_MESSAGE,
                    f"{g.current_user.username} posted a new message in {group_chat.name}",
                    url_for("api.get_user", user_id=g.current_user.id),
                )
                
                emit(
                    "new_notification",
                    notification_schema.dump(notification),
                    room=chat_message.chat_id
                )

# Socket
# A message that has been marked as read should not be able to be marked as unread
# @api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["PATCH"])
def update_group_chat_message(group_chat_id, message_id):
    pass


# Socket
# @api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["DELETE"])
def delete_group_chat_message(group_chat_id, message_id):
    pass


# Socket
# @api.route(
#     "/group_chats/<group_chat_id>/messages/<message_id>/reactions", methods=["POST"]
# )
def add_reaction_to_group_chat_message(group_chat_id, message_id):
    pass



# Socket
@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def join_group_chat(data):
    payload = json.loads(data)
    group_chat_id = payload.get("group_chat_id")
    community_id = payload.get("community_id")
    if not group_chat_id:
        emit("error", json.dumps({"error": "Missing group chat id in request"}))
    elif not community_id:
        emit("error", json.dumps({"error": "Missing community id in request"}))
    else:
        community_membership = dynamodb_repository.get_community_membership(community_id, g.current_user.id)
        if not community_membership:
            emit("error", json.dumps({"error": "User is not a member of this community"}))
        else:
            group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
            if not group_chat:
                emit("error", json.dumps({"error": "Group chat not found"}))
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
    payload = json.loads(data)
    group_chat_id = payload.get("group_chat_id")
    community_id = payload.get("community_id")
    if not group_chat_id:
        emit("error", json.dumps({"error": "Missing group chat id in request"}))
    elif not community_id:
        emit("error", json.dumps({"error": "Missing community id in request"}))
    else:
        community_membership = dynamodb_repository.get_community_membership(community_id, g.current_user.id)
        if not community_membership:
            emit("error", {"error": "User is not a member of this community"})
        else:
            group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
            if not group_chat:
                emit("error", {"error": "Group chat not found"})
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
    print("Connected to server!")
    print(g.current_user.username)


@socketio.on("disconnect")
def disconnect_handler():
    print(g.disconnect_reason)
    emit("disconnect_reason", g.disconnect_reason)