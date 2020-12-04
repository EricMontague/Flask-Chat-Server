"""This module contains the user model."""

from app import bcrypt
from app.dynamodb import KeyPrefix
from datetime import datetime, timedelta
from app.exceptions import (
    NotificationNotFoundException,
    ChatNotFoundException,
    ChatRequestNotFoundException,
    CommunityNotFoundException,
)


# TODO - Too many arguments in constructor, need to look for a solution for this
# Maybe the Builder pattern?

# Maybe split the class up into separate classes? - NotificationManager,  RequestManager, ChatManager
# and CommunityManager?

# These classes would maintain hash tables that map user id's to their domain object and all operations
# performed would go through them. e.g. noticiation_manager.mark_as_read(user_id=1)
class User:
    """Class to represent a user."""

    def __init__(
        self,
        id,
        username,
        name,
        email,
        created_at,
        last_seen_at,
        role,
        bio="",
        location=None,
        avatar=None,
        cover_photo=None,
    ):
        self._id = id
        self.username = username
        self.name = name
        self._password_hash = None
        self.email = email
        self.bio = bio
        self.location = location
        self._created_at = created_at
        self.last_seen_at = last_seen_at
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.role = role
        self.is_online = True
        self._notifications = {}
        self._pending_chat_requests = {}
        self._private_chats = {}
        self._group_chats = {}
        self._communities = {}

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
        self._password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """Return True if the given password matches the user's password,
        otherwise return False.
        """
        return bcrypt.check_password_hash(self._password_hash, password)

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

    def add_notification(self, notification):
        """Add a new notification for the user."""
        self._notifications[notification.id] = notification

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
        self._pending_chat_requests[group_chat_id] = request

    def remove_group_chat_request(self, group_chat_id):
        """Remove a request from the dictionary containing the user's
        pending group chat requests for a particular group chat
        """
        if not self.has_pending_request(group_chat_id):
            raise ChatRequestNotFoundException(
                "A pending chat request could not be found for the given group chat"
            )
        self._pending_chat_requests.pop(group_chat_id)

    def has_pending_request(self, group_chat_id):
        """Return True if the user has a pending group chat request
        for the given chat, otherwise return False.
        """
        return group_chat_id in self._pending_chat_requests

    def join_private_chat(self, private_chat):
        """Add a private chat to the user's dictionary of private chats."""
        other_user = private_chat.get_other_member(self)
        self._private_chats[other_user.id] = private_chat

    def leave_private_chat(self, other_user_id):
        """Remove a private chat to the user's dictionary of private chats."""
        if not self.in_private_chat(other_user_id):
            raise ChatNotFoundException(
                "The current user is not in a private chat with the given user"
            )
        self._private_chats.pop(other_user_id)

    def join_group_chat(self, group_chat):
        """Add a group chat to the user's dictionary of group chats."""
        self.remove_group_chat_request(group_chat.id)
        self._group_chats[group_chat.id] = group_chat

    def leave_group_chat(self, group_chat_id):
        """Remove a group chat with the given id from the user's dictionary
        of group chats.
        """
        if not self.in_group_chat(group_chat_id):
            raise ChatNotFoundException(
                "The user is not a member of the given group chat"
            )
        self._group_chats.pop(group_chat_id)

    def in_group_chat(self, group_chat_id):
        """Return True if the user is a part of a group chat with
        the given id, otherwise return False.
        """
        return group_chat_id in self._group_chats

    def in_private_chat(self, other_user_id):
        """Return True if the user is a part of a private chat with
        another user with the given id, otherwise return False.
        """
        return other_user_id in self._private_chats

    # TODO - Add methods to edit and delete a message from a private chat
    def message_user(self, user_id, message):
        """Send a message to a private chat."""
        if not self.in_private_chat(user_id):
            raise ChatNotFoundException(
                "The current user is not in a private chat with the given user"
            )
        self._private_chats[user_id].post_message(message)

    # TODO - Add methods to edit and delete a message from a group chat
    def message_group(self, group_chat_id, message):
        """Send a message to a group chat that the user is a
        part of.
        """
        if not self.in_group_chat(group_chat_id):
            raise ChatNotFoundException(
                "The user is not a member of the given group chat"
            )
        self._group_chats[group_chat_id].post_message(message)

    def join_community(self, community):
        """Add the community to the user's mapping of communities."""
        self._communities[community.id] = community

    def leave_community(self, community_id):
        """Remove the community from the user's mapping of communities."""
        if not self.is_member_of(community_id):
            raise CommunityNotFoundException(
                "The user is not a member of the given community"
            )
        self._communities.pop(community_id)

    def is_member_of(self, community_id):
        """Return True if the user is a member of the given
        community, otherwise return False.
        """
        return community_id in self._communities

    def to_dynamo(self):
        """Return a representation of a user as stored in DynamoDB."""
        return {
            "PartitionKey": KeyPrefix.USER + self._id,
            "SortKey": KeyPrefix.USER + self._id,
            "username": self.username,
            "name": self.name,
            "password_hash": self._password_hash,
            "email": self.email,
            "bio": self.bio,
            "location": self.location.to_dynamo(),
            "created_at": self._created_at.isoformat(),
            "last_seen_at": self.last_seen_at.isoformat(),
            "avatar": self.avatar.to_dynamo(),
            "cover_photo": self.cover_photo.to_dynamo(),
            "role": self.role.to_dynamo(),
            "is_online": self.is_online
        }

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
            "User(id=%r, username=%r, name=%r,"
            + "email=%r, bio=%r,created_at=%r, last_seen_at=%r,"
            + "avatar=%r, cover_photo=%r, role=%r"
        ) % (
            self._id,
            self.username,
            self.name,
            self.email,
            self.bio,
            self._created_at,
            self.last_seen_at,
            self.avatar,
            self.cover_photo,
            self.role,
        )

