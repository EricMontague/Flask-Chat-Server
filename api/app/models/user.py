"""This module contains the user model."""

from app import flask_bcrypt
from datetime import datetime, timedelta


# Too many arguments in constructor, need to look for a solution for this
class User:
    """Class to represent a user."""

    def __init__(
        self,
        id,
        username,
        name,
        password_hash,
        email,
        bio,
        created_at,
        last_seen_at,
        avatar,
        cover_photo,
        role,
        notifications,
        pending_chat_requests,
        private_chats,
        group_chats,
        communities,
    ):
        self._id = id
        self.username = username
        self.name = name
        self.password_hash = password_hash
        self.email = email
        self.bio = bio
        self._created_at = created_at
        self.last_seen_at = last_seen_at
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.role = role
        self.is_online = True
        self._notifications = notifications
        self._pending_chat_requests = pending_chat_requests
        self._private_chats = private_chats
        self._group_chats = group_chats
        self._communities = communities

    @property
    def id(self):
        """Return the user id."""
        return self._id

    @property
    def joined_on(self):
        """Return the timestamp of when the user was created."""
        return self._created_at

    @property
    def notifications(self):
        """Return a list of the user's notifications sorted from
        most recent to least recent
        """
        return sorted(self._notifications.values(), key=lambda n: n.timestamp)

    @property
    def password(self):
        """Raise an AttributeError is an attempt is made to read the
        password attribute.
        """
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Hash and set the user's password."""
        self.password_hash = flask_bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """Return True if the given password matches the user's password,
        otherwise return False.
        """
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def ping(self):
        """Mark the user as recently seen and online."""
        self._last_seen_at = datetime.now()
        self.is_online = True

    # TODO - Need to decide whether I need a different method for community
    # specific permissions
    def has_permissions(self, permissions):
        """Return True if the user has the given permissions,
        otherwise return False. Permissions are determined by the
        role that the user has.
        """
        return self.role.has_permissions(permissions)

    # TODO - notifications will only maintain the last 20 or so notifications
    # What happens if this notification id is for a notification that hasn't
    # been read, but isn't in the dictionary? The same goes for mark as seen
    def mark_notification_as_read(self, notification_id):
        """Mark the notification with the given id as read."""
        if not self.has_notification(notification_id):
            raise NotificationNotFoundException("User notification not found")
        self._notifications[notification_id].mark_as_read()

    def mark_notification_as_seen(self, notification_id):
        """Mark the notificaiton with the given id as seen."""
        if not self.has_notification(notification_id):
            raise NotificationNotFoundException("User notification not found")
        self._notifications[notification_id].mark_as_seen()

    def has_notification(self, notification_id):
        """Return True if a notification with the given id is in
        the user's dictionary of notifications, otherwise return False.
        """
        return notification_id in self._notifications

    def add_group_chat_request(self, group_chat_id, request):
        """Add a request to the dictionary containing the user's
        pending group chat requests for a particular group chat
        """
        if not self.has_group_chat(group_chat_id):
            raise UserGroupChatNotFoundException(
                "A group chat with the given id could not be found for the user"
            )
        self._pending_chat_requests[group_chat_id] = request

    def remove_group_chat_request(self, group_chat_id):
        """Remove a request from the dictionary containing the user's
        pending group chat requests for a particular group chat
        """
        if not self.has_group_chat(group_chat_id):
            raise UserGroupChatNotFoundException(
                "A group chat with the given id could not be found for the user"
            )
        if not self.has_pending_request(group_chat_id):
            raise ChatRequestNotFoundException(
                "A pending chat request could not be found for the given group chat"
            )
        self._pending_chat_requests.pop(group_chat_id)

    def has_group_chat(self, group_chat_id):
        """Return True if the user is a part of a group chat with
        the given id, otherwise return False.
        """
        return group_chat_id in self._group_chats

    def has_pending_request(self, group_chat_id):
        """Return True if the user has a pending group chat request
        for the given chat, otherwise return False.
        """
        return group_chat_id in self._pending_chat_requests

    def __str__(self):
        """Return a more readable string representation 
        of a user than __repr__ with far less fields.
        """
        return (
            "User(id=%r, username=%r, name=%r, email=%r, bio=%r,"
            + "created_at=%r, last_seen_at=%r, role=%r"
        ) % (
            self._id,
            self.username,
            self.name,
            self.email,
            self.bio,
            self._created_at,
            self.last_seen_at,
            self.role,
        )

    def __repr__(self):
        """Return a verbose representation of the user."""
        return (
            "User(id=%r, username=%r, name=%r, password_hash=%r,"
            + "email=%r, bio=%r,created_at=%r, last_seen_at=%r,"
            + "avatar=%r, cover_photo=%r, role=%r, notifications=%r,"
            + "pending_chat_requests=%r, private_chats=%r, group_chats=%r,"
            + "communities=%r"
        ) % (
            self._id,
            self.username,
            self.name,
            self.password_hash,
            self.email,
            self.bio,
            self._created_at,
            self.last_seen_at,
            self.avatar,
            self.cover_photo,
            self.role,
            self._notifications,
            self._pending_chat_requests,
            self._private_chats,
            self._group_chats,
            self._communities,
        )


class NotificationNotFoundException(Exception):
    """Exception to be raised when a user notification
    cannot be found.
    """

    pass


class UserGroupChatNotFoundException(Exception):
    """Exception to be raised when a particular group
    chat cannot be found for the given user.
    """

    pass


class ChatRequestNotFoundException(Exception):
    """Exception to be raised when a chat request
    for the given user cannot be found.
    """

    pass

