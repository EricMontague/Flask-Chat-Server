"""This module contains the chat message model."""


from enum import Enum
from datetime import datetime


class Message:
    """Class to represent a message in a chat."""

    def __init__(
        self, id, chat_id, user_id, content, created_at=datetime.now(), read=False, editted=False
    ):
        self._id = id
        self._chat_id = chat_id
        self._user_id = user_id
        self._content = content
        self._created_at = created_at
        self._reactions = set()
        self._read = read
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
        return self.user_id

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

    def add_reaction(self, reaction):
        """Add a reaction to the message."""
        self._reactions.add(reaction)

    def has_reactions(self):
        """Return True if the message has any reactions, otherwise
        return False.
        """
        return len(self._reactions) > 0

    def was_read(self):
        """Return True if the message has been read,
        otherwise return False."""
        return self._read

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


class Reaction(Enum):
    """Enum to represent reactions that a user can
    have to a message.
    """

    LIKE = 1
    LAUGH = 2
    HEART = 3
    SAD = 4
    EYES = 5
    WOW = 6
    ANGRY = 7

