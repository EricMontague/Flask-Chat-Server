import json
from http import HTTPStatus
from flask import current_app, g, render_template, request
from flask_socketio import send, emit, join_room, leave_room, disconnect
from app.sockets import sockets
from app.extensions import socketio
from app.repositories import dynamodb_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.decorators.auth import socketio_jwt_required
from app.models import TokenType


@sockets.route("/testing_chat")
def testing_chat():
    return render_template("chat.html")


# Socket - Creates a notification too
# @api.route("/group_chats/<group_chat_id>/messages", methods=["POST"])
def create_group_chat_message(group_chat_id):
    pass


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
@socketio.on("join")
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def join_group_chat(data):
    payload = json.loads(data)
    group_chat_id = payload.get("group_chat_id")
    community_id =payload.get("community_id")
    if not group_chat_id:
        return {"error": "Please provide a group chat id"}, HTTPStatus.UNPROCESSABLE_ENTITY
    if not community_id:
        return {"error": "Please provide a community id"}, HTTPStatus.UNPROCESSABLE_ENTITY
 
    try:
        dynamodb_repository.add_group_chat_member(
            community_id, group_chat_id, g.current_user.id
        )
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    annoucement = f"{g.current_user.username} has joined the chat!"
    join_room(group_chat_id)
    socketio.emit("new_group_chat_member", {"payload": annoucement})


# Socket
# @api.route("/group_chats/<group_chat_id>/members/<user_id>", methods=["DELETE"])
def leave_group_chat(group_chat_id, user_id):
    pass


@socketio.on("message")
def message(content):
    print(f"Received message: {content}")
    send(content)


@socketio.event
def custom_event(data):
    print(f"Received data from custom event: {data}")


@socketio.on("connect")
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def connect_handler():
    print("Connected to server!")
    print(g.current_user.username)


@socketio.on("disconnect")
def disconnect_handler():
    print(g.disconnect_reason)
    emit("disconnect_reason", g.disconnect_reason)