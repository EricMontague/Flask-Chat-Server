"""This module contains the chat request model."""


from datetime import datetime


class ChatRequest:
    """Class to represent a request to join a group chat."""

    def __init__(self, id, user):
        self._id = id
        self._user = user
        self._created_at = datetime.now()
        self._status = ChatRequestStatus.PENDING
        self._seen = False

    @property
    def id(self):
        """Return the request id."""
        return self._id

    @property
    def timestamp(self):
        """Return the timestamp of the request."""
        return self._created_at

    @property
    def status(self):
        """Return the request's status."""
        return self._status

    @property
    def user_id(self):
        """Return the id of the user who made the request."""
        return self._user.id

    def was_seen(self):
        """Return True if the request has been seen, otherwise
        return False.
        """
        return self._seen

    def mark_as_seen(self):
        """Mark the request as seen by a member of the group chat."""
        self._seen = True

    def accept(self):
        """Mark the request as accepted."""
        self._status = ChatRequestStatus.ACCEPTED

    def reject(self):
        """Mark the request as rejected."""
        self._status = ChatRequestStatus.REJECTED

    def __repr__(self):
        """Return the representation of a chat request."""
        return "ChatRequest(id=%r, user=%r)" % (self._id, self._user)


class ChatRequestStatus:
    """Class to represent the status of a chat request."""

    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
