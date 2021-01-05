"""This module contains view functions for accessing group
chat resources.
"""


from app.api import api


@api.route("/group_chats/<group_chat_id>/messages")
def get_group_chat_messages(group_chat_id):
    pass


@api.route("/group_chats/<group_chat_id>/messages", methods=["POST"])
def create_group_chat_message(group_chat_id):
    pass


@api.route("/group_chats/<group_chat_id>/messages/<message_id>")
def get_group_chat_message(group_chat_id, message_id):
    pass


@api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["PATCH"])
def update_group_chat_message(group_chat_id, message_id):
    pass


@api.route("/group_chats/<group_chat_id>/messages/<message_id>", methods=["DELETE"])
def delete_group_chat_message(group_chat_id, message_id):
    pass


@api.route(
    "/group_chats/<group_chat_id>/messages/<message_id>/reactions", methods=["POST"]
)
def add_reaction_to_group_chat_message(group_chat_id, message_id):
    pass


@api.route("/group_chats/<group_chat_id>/members")
def get_group_chat_members(group_chat_id):
    pass


@api.route("/group_chats/<group_chat_id>/members/<user_id>", methods=["DELETE"])
def leave_group_chat(group_chat_id, user_id):
    pass
