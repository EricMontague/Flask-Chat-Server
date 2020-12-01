"""This file is a temporary holding place for various functions that
will exist in the service layer of the application. They will be
moved to their appropriate directories when api routes are created.
These are just prototypes of what the final implementations could look
like in the end.
"""


from uuid import uuid4
from app.exceptions import (
    ChatNotFoundException,
    ChatRequestNotFoundException,
    UserNotFoundException,
    DuplicateChatRequestException,
    ChatCapacityReachedException,
    CommunityNameAlreadyExistsException,
    CommunityNotFoundException,
)
from app.models import (
    Notification,
    NotificationType,
    ChatRequest,
    GroupChat,
    Message,
    Community,
)


def create_group_chat_request(current_user, chat_request_data, repo):
    # Fetch group chat from storage layer
    group_chat = repo.get_group_chat(chat_request_data["chat_id"])
    if not group_chat:
        raise ChatNotFoundException("Group chat could not be found")
    if group_chat.has_pending_request(current_user.id):
        raise DuplicateChatRequestException(
            "User already has a pending request to join this chat"
        )
    chat_request = ChatRequest(**chat_request_data)
    # Update user and chat states
    group_chat.add_request(chat_request)
    current_user.add_request(chat_request)

    # create notification for all group chat members
    # These will be sent to users via SocketIO
    notification = Notification(
        uuid4(),
        NotificationType.NEW_CHAT_REQUEST,
        f"{current_user.username} wants to join the chat",
        current_user,
    )
    for member in group_chat.members:
        member.add_notification(notification)

    # Update data in storage layer
    repo.write_many(
        {
            "put": {
                "group_chat": group_chat,
                "users": group_chat.members + [current_user],  # this is suspect
                "chat_request": chat_request,
                "notification": notification,
            }
        }
    )


def accept_group_chat_request(current_user, requesting_user_id, chat_id, repo):
    # current user is a member of the group chat
    data = repo.get_many(
        {
            "chat_request": requesting_user_id,
            "group_chat": chat_id,
            "user": requesting_user_id,
        }
    )
    # Validation
    if "chat_request" not in data:
        raise ChatRequestNotFoundException("Chat request could not be found")
    if "user" not in data:
        raise UserNotFoundException(
            "The user who requested to join the group chat could not be found"
        )
    if "group_chat" not in data:
        raise ChatNotFoundException("Group chat could not be found")

    # extract models
    chat_request = data["chat_request"]
    user = data["user"]
    group_chat = data["group_chat"]
    if group_chat.is_full():
        raise ChatCapacityReachedException("Sorry, the group chat is full")

    # Update states of models
    chat_request.accept()
    user.join_group_chat(group_chat)
    group_chat.add_member(user)

    # Update notification for requesting user
    # These will be sent to users via SocketIO
    notification = Notification(
        uuid4(),
        NotificationType.CHAT_REQUEST_ACCEPTED,
        f"Your request to join {group_chat.name} has been accepted!",
        group_chat,
    )
    user.add_notification(notification)

    # This should be a transaction
    repo.write_many(
        {
            "put": {
                "chat_request": chat_request,
                "group_chat": group_chat,
                "user": user,
                "notification": notification,
            }
        }
    )


def reject_group_chat_request(current_user, requesting_user_id, chat_id, repo):
    # current user is a member of the group chat
    data = repo.get_many(
        {
            "chat_request": requesting_user_id,
            "group_chat": chat_id,
            "user": requesting_user_id,
        }
    )

    # Validation
    if "chat_request" not in data:
        raise ChatRequestNotFoundException("Chat request could not be found")
    if "user" not in data:
        raise UserNotFoundException(
            "The user who requested to join the group chat could not be found"
        )
    if "group_chat" not in data:
        raise ChatNotFoundException("Group chat could not be found")

    # Extract models
    chat_request = data["chat_request"]
    user = data["user"]
    group_chat = data["group_chat"]

    # Update model state
    chat_request.reject()
    user.remove_group_chat_request(group_chat.id)
    group_chat.remove_request(user.id)

    # send notification to user of rejection
    # These will be sent to users via SocketIO
    notification = Notification(
        uuid4(),
        NotificationType.CHAT_REQUEST_REJECTED,
        f"Your request to join {group_chat.name} has been rejected",
        group_chat,
    )
    user.add_notification(notification)

    # This should be a transaction
    repo.write_many(
        {
            "put": {
                "chat_request": chat_request,
                "group_chat": group_chat,
                "user": user,
                "notification": notification,
            }
        }
    )


# When a user wants to rescind their request
def cancel_chat_request(current_user, chat_id, repo):
    data = repo.get_many({"chat_request": current_user.id, "group_chat": chat_id})
    if "chat_request" not in data:
        raise ChatRequestNotFoundException("Chat request could not be found")
    if "group_chat" not in data:
        raise ChatNotFoundException("Group chat could not be found")
    group_chat = data["group_chat"]
    current_user.remove_group_chat_request(group_chat.id)
    group_chat.remove_request(current_user.id)
    repo.write_many(
        {
            "put": {"user": current_user, "group_chat": group_chat},
            "delete": {"chat_request": current_user.id},
        }
    )


# This can probably just be done in the API layer as not
# much benefit is gained from abstracting this away
def create_group_chat(current_user, group_chat_data, repo):
    group_chat = GroupChat(**group_chat_data)
    repo.create_group_chat(group_chat)


def leave_group_chat(current_user, group_chat_id, repo):
    group_chat = repo.get_group_chat(group_chat_id)
    if not group_chat:
        raise ChatNotFoundException("Group chat could not be found")
    current_user.leave_group_chat(group_chat.id)
    group_chat.remove_member(current_user.id)
    repo.write_many({"put": {"group_chat": group_chat, "user": current_user}})


# Some SocketIO stuff will be needed here for notifications and messages
def post_message_to_group_chat(current_user, group_chat_id, message_data, repo):
    group_chat = repo.get_group_chat(group_chat_id)
    if not group_chat:
        raise ChatNotFoundException("Group chat could not be found")
    # How should this be handled? Should I go through the user to post to the
    # group chat, or go directly to the group chat itself? # If group chats
    # and users are in separate tables, how will both tables get updated?
    message = Message(**message_data)
    current_user.message_group(message)

    # group_chat.post_message(message)

    notification = Notification(
        uuid4(),
        NotificationType.NEW_GROUP_CHAT_MESSAGE,
        f"A new message from {current_user.username} was posted in {group_chat.name}!",
        group_chat,
    )
    for member in group_chat.members:
        member.add_notification(notification)

    # Persist changes
    repo.write_many(
        {
            "put": {
                "message": message,
                "group_chat": group_chat,
                "users": group_chat.members + [current_user],  # this is suspect
                "notification": notification,
            }
        }
    )


# later on I could send notifications to users that a community
# near their location was created
def create_community(current_user, community_data, repo):
    existing_community = repo.get_community_by_name(community_data["name"])
    if existing_community is not None:
        raise CommunityNameAlreadyExistsException(
            "A community with that name already exists"
        )
    community = Community(**community_data)
    repo.create_community(community)


def join_community(current_user, community_id, repo):
    community = repo.get_community(community_id)
    if not community:
        raise CommunityNotFoundException("Community could not be found")
    current_user.join_community(community)
    community.add_member(current_user)
    repo.write_many({"put": {"user": current_user, "community": community}})


def leave_community(current_user, community_id, repo):
    community = repo.get_community(community_id)
    if not community:
        raise CommunityNotFoundException("Community could not be found")
    current_user.leave_community(community.id)
    community.remove_member(current_user.id)
    repo.write_many({"put": {"user": current_user, "community": community}})

