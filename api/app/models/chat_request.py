"""This module contains the chat request model."""


from enum import Enum
from datetime import datetime


class ChatRequest:
    """Class to represent a request to join a group chat."""

    def __init__(self, id, user_id, chat_id):
        self._id = id
        self._user_id = user_id
        self._chat_id = chat_id
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

    def to_dict(self):
        """Return a dictionary representation of a notification."""
        return {
            "id": self._id,
            "user_id": self._user_id,
            "chat_id": self._chat_id,
            "created_at": self._created_at.isoformat(),
            "status": self._status.name,
            "seen": self._seen,
        }

    def __repr__(self):
        """Return the representation of a chat request."""
        return "ChatRequest(id=%r, user_id=%r, chat_id=%r)" % (
            self._id,
            self._user_id,
            self._chat_id,
        )


class ChatRequestStatus(Enum):
    """Enum to represent the status of a chat request."""

    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
