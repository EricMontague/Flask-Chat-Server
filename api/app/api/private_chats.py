"""This module contains view functions for accessing private chat
resources.
"""


from hashlib import md5
from http import HTTPStatus
from flask import current_app, url_for, g
from app.api import api
from app.repositories import dynamodb_repository
from app.repositories.exceptions import (
    DatabaseException,
    NotFoundException,
    UniqueConstraintException,
)
from app.schemas import UrlParamsSchema, PrivateChatMessageSchema, PrivateChatSchema
from app.decorators.request_response import handle_request, handle_response
from app.decorators.auth import permission_required
from app.models import RolePermission, PrivateChat
from app.extensions import ma


PrivateChatGeneratedSchema = PrivateChatSchema.from_dict(
    {"other_user_id": ma.UUID(required=True)}
)


@api.route("/private_chats/<private_chat_id>/messages")
@handle_request(UrlParamsSchema())
@handle_response(PrivateChatMessageSchema(many=True))
def get_private_chat_messages(url_params, private_chat_id):
    """Return a list of private chat message resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_private_chat_messages(
            private_chat_id, per_page, cursor=cursor
        )
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


@api.route("/private_chats/<private_chat_id>/messages/<message_id>")
@handle_response(PrivateChatMessageSchema())
def get_private_chat_message(private_chat_id, message_id):
    """Return a private chat message resource."""
    chat_message = dynamodb_repository.get_private_chat_message(
        private_chat_id, message_id
    )
    if not chat_message:
        return {"error": "Private chat message not found"}, HTTPStatus.NOT_FOUND
    return chat_message, HTTPStatus.OK


@api.route("/private_chats/<private_chat_id>")
@handle_response(PrivateChatSchema())
def get_private_chat(private_chat_id):
    """Return a private chat resource."""
    private_chat = dynamodb_repository.get_private_chat(private_chat_id)
    if not private_chat:
        return {"error": "Private chat not found"}, HTTPStatus.NOT_FOUND
    if not private_chat.is_member(g.current_user.id):
        return (
            {"error": "User is not a member of this private chat"},
            HTTPStatus.UNAUTHORIZED,
        )
    return private_chat, HTTPStatus.OK


@api.route("/private_chats", methods=["POST"])
@permission_required(RolePermission.CREATE_PRIVATE_CHAT)
@handle_request(PrivateChatGeneratedSchema())
@handle_response(PrivateChatSchema())
def create_private_chat(data):
    """Create a new private chat between two users."""
    other_user = dynamodb_repository.get_user(data["other_user_id"].hex)
    if not other_user:
        return {"error": "Other user could not be found"}, HTTPStatus.NOT_FOUND
    private_chat_id = md5(g.current_user.id.encode("utf-8") + other_user.id.encode("utf-8")).hexdigest()
    existing_private_chat = dynamodb_repository.get_private_chat(private_chat_id)
    if existing_private_chat:
        return {"error": "A private chat already exists between these two users"}, HTTPStatus.BAD_REQUEST
    private_chat = PrivateChat(private_chat_id, g.current_user, other_user)
    try:
        dynamodb_repository.add_private_chat(private_chat)
    except UniqueConstraintException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    headers = {
        "Location": url_for("api.get_private_chat", private_chat_id=private_chat.id)
    }
    return (private_chat, HTTPStatus.CREATED, headers)
