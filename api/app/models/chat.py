"""This module contains models to represent various types of
chats in the application.
"""


from dataclasses import dataclass
from datetime import datetime


class PrivateChat:
    """Class to represent a private chat between two users"""

    def __init__(self, id, primary_user, secondary_user):
        self._id = id
        self._primary_user = primary_user
        self._secondary_user = secondary_user

    @property
    def id(self):
        """Return the chat's id."""
        return self._id

    def __repr__(self):
        """Return a representatino of a private chat."""
        return "PrivateChat(id=%r, primary_user=%r, secondary_user=%r)" % (
            self._id,
            self._primary_user,
            self._secondary_user,
        )


class GroupChat:
    """Class to represent a group chat between one or more users
    in a specific community
    """

    def __init__(self, id, community_id, name, description):
        self._id = id
        self.name = name
        self.description = description
        self._community_id = community_id

    @property
    def id(self):
        """Return the chat id."""
        return self._id

    @property
    def community_id(self):
        """Return the id of the community the group chat belongs to."""
        return self._community_id

    def __repr__(self):
        """Return a representation of a group chat."""
        return (
            "GroupChat(id=%r, community_id=%r, name=%r, description=%r)"
            % (
                self._id,
                self._community_id,
                self.name,
                self.description
            )
        )


@dataclass(frozen=True)
class PrivateChatMember:
    """Class to represent the relationship between a private chat and 
    a user who is a member of that private chat.
    """

    private_chat_id: str
    user_id: str
    other_user_id: str
    created_at: datetime = datetime.now()


@dataclass(frozen=True)
class GroupChatMember:
    """Class to represent the relationship between a private chat and 
    a user who is a member of that private chat.
    """

    group_chat_id: str
    user_id: str
    created_at: datetime = datetime.now()

