"""This module contains view functions for accessing private chat
resources.
"""


from http import HTTPStatus
from flask import current_app
from app.api import api
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException, NotFoundException
from app.schemas import UrlParamsSchema, PrivateChatMessageSchema
from app.decorators.request_response import handle_request, handle_response


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


