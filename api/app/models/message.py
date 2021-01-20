"""This module contains the chat message model."""


from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Message:
    """Class to represent a message in a chat."""

    def __init__(
        self, 
        id, 
        chat_id, 
        user_id, 
        content,
        message_type, 
        created_at=datetime.now(), 
        sent=False, 
        editted=False,
        reactions={}
    ):
        self._id = id
        self._chat_id = chat_id
        self._user_id = user_id
        self._content = content
        self.message_type = message_type
        self._created_at = created_at
        self._reactions = reactions
        self._sent = sent
        self._editted = editted

    @property
    def id(self):
        """Return the message's id."""
        return self._id

    @property
    def chat_id(self):
        """Return the id of the chat the message belongs to."""
        return self._chat_id

    @property
    def user_id(self):
        """Return the id of the user the message belongs to."""
        return self._user_id

    @property
    def content(self):
        """Return the content of the message."""
        return self._content

    @property
    def timestamp(self):
        """Return the date and time of when the message 
        was created.
        """
        return self._created_at

    @property
    def reactions(self):
        """Return a list of reactions attached to the message."""
        return list(self._reactions.values())

    def add_reaction(self, reaction):
        """Add a reaction to the message."""
        self._reactions[reaction.user_id] = reaction

    def remove_reaction(self, user_id):
        """Remove and return a user's reaction from the chat message."""
        return self._reactions.pop(user_id, None)

    def has_reactions(self):
        """Return True if the message has any reactions, otherwise
        return False.
        """
        return len(self._reactions) > 0

    def was_read(self):
        """Return True if the message has been read,
        otherwise return False."""
        return self._read

    def mark_as_read(self):
        """Mark the chat message as read."""
        self._read = True

    def edit(self, content):
        """Edit the message content."""
        self._content = content
        self._editted = True

    def was_editted(self):
        """Return True if the message has been editted,
        otherwise return False.
        """
        return self._editted

    def __repr__(self):
        """Return a representation of a message."""
        return "Message(id=%r, chat_id=%r, content=%r)" % (
            self._id,
            self._chat_id,
            self._content,
        )


class MessageType(Enum):
    """Enum to represent chat types for messages"""

    PRIVATE_CHAT = 1
    GROUP_CHAT = 2


class ReactionType(Enum):
    """Enum to represent types of reactions that a user can
    have to a message.
    """

    LIKE = 1
    LAUGH = 2
    HEART = 3
    SAD = 4
    EYES = 5
    WOW = 6
    ANGRY = 7



@dataclass(frozen=True)
class Reaction:
    """Class to represent a reaction a user has had to a message."""

    user_id: str
    reaction_type: ReactionType
    created_at: datetime = datetime.now()
