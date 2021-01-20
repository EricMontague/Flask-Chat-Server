"""This module contains view functions for accessing group
chat resources.
"""


from http import HTTPStatus
from flask import current_app, request, g
from app.api import api
from app.schemas import UrlParamsSchema, GroupChatMessageSchema, UserSchema, GroupChatUrlParamsSchema
from app.repositories import dynamodb_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.decorators.views import handle_response, handle_request
from app.models import MessageType


@api.route("/group_chats/<group_chat_id>/messages")
@handle_request(GroupChatUrlParamsSchema())
@handle_response(GroupChatMessageSchema(many=True))
def get_group_chat_messages(url_params, group_chat_id):
    """Return a list of group chat message resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    community_id = url_params["community_id"]
    try:
        results = dynamodb_repository.get_group_chat_messages(community_id, group_chat_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


@api.route("/group_chats/<group_chat_id>/messages/<message_id>")
@handle_response(GroupChatMessageSchema())
def get_group_chat_message(group_chat_id, message_id):
    """Return a group chat message resource."""
    chat_message = dynamodb_repository.get_chat_message(group_chat_id, message_id, MessageType.GROUP_CHAT)
    if not chat_message:
        return {"error": "Group chat message not found"}, HTTPStatus.NOT_FOUND
    return chat_message, HTTPStatus.OK


@api.route("/group_chats/<group_chat_id>/members/<user_id>", methods=["PUT"])
def join_group_chat(group_chat_id, user_id):
    """Add a user as a new member of a group chat."""
    payload = request.json
    if not payload:
        return {"error": "Missing JSON body in request"}, HTTPStatus.UNPROCESSABLE_ENTITY
    community_id = payload.get("community_id")
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
    return {}, HTTPStatus.OK


@api.route("/group_chats/<group_chat_id>/members/<user_id>", methods=["DELETE"])
def leave_group_chat(group_chat_id, user_id):
    """Remove a user as a member of a group chat."""
    try:
        dynamodb_repository.remove_group_chat_member(group_chat_id, g.current_user.id)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    return {}, HTTPStatus.NO_CONTENT