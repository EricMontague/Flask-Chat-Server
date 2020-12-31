"""This module contains view functions for accessing chat
resources.
"""


from app.api import api
from app.repositories import dynamodb_repository


# A user cannot create a second private chat with the same user
@api.route("/private_chats", methods=["POST"])
def create_private_chat():
    pass


@api.route("/private_chats/<private_chat_id>/messages")
def get_private_chat_messages(private_chat_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages", methods=["POST"])
def create_private_chat_message(private_chat_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages/message_id", methods=["PATCH"])
def update_private_chat_message(private_chat_id, message_id):
    pass


@api.route("/private_chats/<private_chat_id>/messages/message_id", methods=["DELETE"])
def delete_private_chat_message(private_chat_id, message_id):
    pass


