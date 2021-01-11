"""This module contains view functions for accessing group
chat resources.
"""


from http import HTTPStatus
from flask import current_app
from app.api import api
from app.schemas import UrlParamsSchema, GroupChatMessageSchema, UserSchema
from app.repositories import dynamodb_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.helpers import handle_response, handle_request, jwt_required
from app.models import TokenType


@api.route("/group_chats/<group_chat_id>/messages")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(GroupChatMessageSchema(many=True))
def get_group_chat_messages(url_params, group_chat_id):
    """Return a list of group chat message resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_group_chat_messages(group_chat_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


@api.route("/group_chats/<group_chat_id>/messages/<message_id>")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_response(GroupChatMessageSchema())
def get_group_chat_message(group_chat_id, message_id):
    """Return a group chat message resource."""
    chat_message = dynamodb_repository.get_group_chat_message(group_chat_id, message_id)
    if not chat_message:
        return {"error": "Group chat message not found"}, HTTPStatus.NOT_FOUND
    return chat_message, HTTPStatus.OK


# Socket - Creates a notification too
@api.route("/group_chats/<group_chat_id>/messages", methods=["POST"])
def create_group_chat_message(group_chat_id):
    pass


# Socket
# A message that has been marked as read should not be able to be marked as unread
@api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["PATCH"])
def update_group_chat_message(group_chat_id, message_id):
    pass


# Socket
@api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["DELETE"])
def delete_group_chat_message(group_chat_id, message_id):
    pass


# Socket
@api.route(
    "/group_chats/<group_chat_id>/messages/<message_id>/reactions", methods=["POST"]
)
def add_reaction_to_group_chat_message(group_chat_id, message_id):
    pass


# Socket
@api.route("/group_chats/<group_chat_id>/members", methods=["POST"])
def join_group_chat(group_chat_id):
    pass


# Socket
@api.route("/group_chats/<group_chat_id>/members/<user_id>", methods=["DELETE"])
def leave_group_chat(group_chat_id, user_id):
    pass
