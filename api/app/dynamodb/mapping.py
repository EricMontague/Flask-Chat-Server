"""This module contains functions and classes for mapping application
models to DynamoDB items.
"""


from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.models import (
    User,
    Notification,
    Community,
    GroupChat,
    PrivateChat,
    ChatRequest,
    Location,
    Image,
)


class BaseItemMapper(ABC):
    """Abstract base class for all DynamoDB item mappers."""

    model = None
    fields_to_include = ()
    fields_to_exclude = ()

    def load(self, item):
        """Convert an item from DynamoDB into a model."""
        pass
        

    def dump(self, model):
        """Convert a model in an item to be inserted into
        DynamoDB.
        """
        pass


class UserItemMapper(BaseItemMapper):
    """Class to map user models to dynamodb items
    and vice versa.
    """
    fields_to_include = (
        "id",
        "username",
        "name",
        "password_hash",
        "email",
        "created_at",
        "last_seen_at",
        "role",
        "bio",
        "location",
        "avatar.url",
        "cover_photo.url",
    )
    fields_to_exclude = (
        "notifications",
        "pending_chat_requests",
        "private_chats",
        "group_chats",
        "communities",
    )

    def load(self, item):
        """Convert an item from DynamoDB into a model."""
        user = User(**item["profile_data"])
        self._add_notifications(user, item["notifications"])
        self._add_communities(user, item["communities"])
        self._add_group_chats(user, item["group_chats"])
        self._add_private_chats(user, item["private_chats"])
        self._add_chat_requests(user, item["chat_requests"])
        # location = Location(**item.get("location"))
        # avatar = Image(**item.get("avatar"))
        # cover_photo = Image(**item.get("cover_photo"))
        # role = Image(**item.get("role"))
        return user

    def _add_notifications(self, user, notifications):
        # need to sort notifications first
        user._notifications = {
            notification_id: Notification(**notification)
            for notification_id, notification in notifications.items()
        }

    def _add_communities(self, user, communities):
        user._communities = {
            community_id: Community(**community)
            for community_id, community in communities.items()
        }

    def _add_group_chats(self, user, group_chats):
        user._group_chats = {
            group_chat_id: GroupChat(**group_chat)
            for group_chat_id, group_chat in group_chat.items()
        }

    def _add_private_chats(self, user, private_chats):
        user._private_chats = {
            private_chat_id: PrivateChat(**private_chat)
            for private_chat_id, private_chat in private_chats.items()
        }

    def _add_chat_requests(self, user, chat_requests):
        user._pending_chat_requests = {
            chat_request_id: ChatRequest(**chat_request)
            for chat_request_id, chat_request in chat_requests.items()
        }


@dataclass
class UpdateExpression:
    """Class to represent an update expression for DynamoDB."""

    expression: str
    attribute_names: dict
    attribute_values: dict


# expression = UpdateExpression("set #L.#S=:state", {"#L": "location", "#S": "state"}, {":state": "New Jersey"})
