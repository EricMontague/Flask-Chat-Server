"""This module contains view functions for accessing private chat
resources.
"""


from app.api import api
from app.repositories import dynamodb_repository


@api.route("/private_chats/<private_chat_id>/messages")
def get_private_chat_messages(private_chat_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages/<message_id>")
def get_private_chat_message(private_chat_id, message_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages", methods=["POST"])
def create_private_chat_message(private_chat_id):
    pass


# A message that has been marked as read should not be able to be marked as unread
@api.route("/private_chats/<private_chat_id>/messages/<message_id>", methods=["PATCH"])
def update_private_chat_message(private_chat_id, message_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages/<message_id>", methods=["DELETE"])
def delete_private_chat_message(private_chat_id, message_id):
    pass


# A user shouldn't have more than one reaction per message
@api.route(
    "/private_chats/<private_chat_id>/messages/<message_id>/reactions", methods=["POST"]
)
def add_reaction_to_private_chat_message(private_chat_id, message_id):
    pass
