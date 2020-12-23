"""This module contains the notification model and related classes/functions."""


from enum import Enum
from datetime import datetime


# A notification should be immutable, except for the read and seen attributes


class Notification:
    """Class to represent a user notification."""

    def __init__(self, id, notification_type, message, target):
        self._id = id
        self._notification_type = notification_type
        self._message = message
        self._target = target
        self._created_at = datetime.now()
        self._read = False
        self._seen = False

    @property
    def id(self):
        """Return the id of the notification."""
        return self._id

    @property
    def notification_type(self):
        """Return the type of the notification."""
        return self._notification_type

    @property
    def message(self):
        """Return the noticiation message."""
        return self._message

    @property
    def timestamp(self):
        """Return the timestamp of when the notification was created."""
        return self._created_at

    def was_read(self):
        """Return True if the notification has been read,
        otherwise return False."""
        return self._read

    def was_seen(self):
        """Return True is the notification has been seen,
        otherwise return False.
        """
        return self._seen

    def mark_as_read(self):
        """Mark the notification as read by the user."""
        self._read = True

    def mark_as_seen(self):
        """Mark the notification as seen by the user."""
        self._seen = True

    def __lt__(self, other):
        """Comparator dunder method for sorting notifications."""
        pass

    def __repr__(self):
        """Return the representation of the Notification."""
        return "Notification(id=%r, notification_type=%r, message=%r, target=%r)"


class NotificationType(Enum):
    """Enum that holds constants of notification types."""

    NEW_PRIVATE_CHAT_MESSAGE = 1
    NEW_GROUP_CHAT_MESSAGE = 2
    NEW_CHAT_REQUEST = 3
    CHAT_REQUEST_ACCEPTED = 4
    CHAT_REQUEST_REJECTED = 5
    NEW_COMMUNITY_NEAR_YOU = 6

