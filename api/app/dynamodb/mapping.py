"""This module contains functions and classes for mapping application
models to DynamoDB items.
"""


from enum import Enum
from abc import ABC, abstractmethod


class BaseItemMapper(ABC):
    """Abstract base class for all DynamoDB item mappers."""

    fields_to_exclude = ()

    def load(self, item):
        """Convert an item from DynamoDB into a model."""
        pass

    @classmethod
    def dump(cls, model):
        """Convert a model into an item to be inserted into
        DynamoDB.
        """
        pass


class UserItemMapper(BaseItemMapper):
    """Class to map user models to dynamodb items
    and vice versa.
    """

    fields_to_exclude = (
        "notifications",
        "pending_chat_requests",
        "private_chats",
        "group_chats",
        "communities",
    )

    @classmethod
    def load(cls, item):
        """Convert an item from DynamoDB into a model."""
        # user = User(**item["profile_data"])
        # cls._add_notifications(user, item["notifications"])
        # self._add_communities(user, item["communities"])
        # self._add_group_chats(user, item["group_chats"])
        # self._add_private_chats(user, item["private_chats"])
        # self._add_chat_requests(user, item["chat_requests"])
        # # location = Location(**item.get("location"))
        # # avatar = Image(**item.get("avatar"))
        # # cover_photo = Image(**item.get("cover_photo"))
        # # role = Image(**item.get("role"))
        # return user
        return None

    # def _add_notifications(self, user, notifications):
    #     # need to sort notifications first
    #     user._notifications = {
    #         notification_id: Notification(**notification)
    #         for notification_id, notification in notifications.items()
    #     }

    # def _add_communities(self, user, communities):
    #     user._communities = {
    #         community_id: Community(**community)
    #         for community_id, community in communities.items()
    #     }

    # def _add_group_chats(self, user, group_chats):
    #     user._group_chats = {
    #         group_chat_id: GroupChat(**group_chat)
    #         for group_chat_id, group_chat in group_chat.items()
    #     }

    # def _add_private_chats(self, user, private_chats):
    #     user._private_chats = {
    #         private_chat_id: PrivateChat(**private_chat)
    #         for private_chat_id, private_chat in private_chats.items()
    #     }

    # def _add_chat_requests(self, user, chat_requests):
    #     user._pending_chat_requests = {
    #         chat_request_id: ChatRequest(**chat_request)
    #         for chat_request_id, chat_request in chat_requests.items()
    #     }


class UpdateAction(Enum):
    """Enum to represent actions for update expressions in DynamoDB."""

    SET = 0
    ADD = 1
    DELETE = 2
    REMOVE = 3


class UpdateExpression:
    """Class to represent an update expression for DynamoDB."""

    def __init__(self, action, attributes_to_values):
        self._build_expression(action, attributes_to_values)

    def _build_expression(self, action, attributes_to_values):
        expression = []
        self.original_attribute_names = []
        self.attribute_name_placeholders = {}
        self.attribute_value_placeholders = {}
        for attribute_name in attributes_to_values:
            attribute_name_lower = attribute_name.lower()
            self.original_attribute_names.append(attribute_name_lower)
            nested_attributes = attribute_name_lower.split(
                "."
            )  # handle nested attributes
            name_alias = ".#".join(nested_attributes)
            expression.append(
                f"#{name_alias} = :{attribute_name_lower.replace('.', '')}"
            )
            # Map aliases for nested attibutes to actual attributes
            for attribute in nested_attributes:
                self.attribute_name_placeholders[f"#{attribute}"] = attribute
            self.attribute_value_placeholders[
                f":{attribute_name_lower.replace('.', '')}"
            ] = attributes_to_values[attribute_name]
        self.expression = action.name + " " + ", ".join(expression)

