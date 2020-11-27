"""This module contains the chat message model."""


from datetime import datetime


class Message:
    """Class to represent a message in a chat."""

    def __init__(self, id, content):
        self._id = id
        self._content = content
        self._created_at = datetime.now()
        self._reactions = set()
        self._read = False
        self._editted = False

    @property
    def id(self):
        """Return the message's id."""
        return self._id

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
        return "Message(id=%r, content=%r)" % (self._id, self._content)


class Reaction:
    """Class to represent reactions that a user can
    have to a message.
    """

    LIKE = "like"
    LAUGH = "laugh"
    HEART = "heart"
    SAD = "sad"
    EYES = "eyes"
    WOW = "wow"
    ANGRY = "angry"

