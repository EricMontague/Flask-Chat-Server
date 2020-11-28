"""This file is a temporary holding place for various functions that
will exist in the service layer of the application. They will be
moved to their appropriate directories when api routes are created.
I'm creating them mainly to flesh out the different access patterns
for the api. Broad assumptions are made about the repository's behaviors
as it is not implemented yet
"""


from app.exceptions import (
    ChatNotFoundException,
    ChatRequestNotFoundException
)


# TODO - How will these functions handle 'NotFound' exceptions?

def create_group_chat_request(current_user, chat_request, repo):
    group_chat = repo.get_group_chat(chat_request.chat_id)
    if not group_chat:
        raise ChatNotFoundException(
            "Group chat could not be found"
        )
    group_chat.add_request(chat_request)
    current_user.add_request(chat_request)

    # Should this be a transaction?
    repo.update_chat(group_chat)
    repo.update_user(current_user)


def accept_group_chat_request(current_user, requesting_user_id, chat_id, repo):
    # current user is a member of the group chat
    data = repo.get_many({
        "chat_request_id": requesting_user_id,
        "chat_id": chat_id,
        "user_id": requesting_user_id
    })
    if "chat_request" not in data:
        raise ChatRequestNotFoundException("Chat request could not be found")
    if "user" not in data:
        raise UserNotFoundException(
            "The user who requested to join the group chat could not be found"
        )
    if "group_chat" not in data:
        raise ChatNotFoundException("Group chat could not be found")
    chat_request = data["chat_request"]
    user = data["user"]
    group_chat = data["group_chat"]

    # TODO - Move these inside the methods of these objects
    chat_request.accept()
    user.remove_group_chat_request(group_chat.id)
    user.join_group_chat(group_chat)
    chat.add_member(user)
    chat.remove_group_chat_request(user.id)

    # Should this be a transaction?
    repo.write_many([user, chat_request, chat])

def reject_group_chat_request(current_user, requesting_user_id, repo):
    pass



