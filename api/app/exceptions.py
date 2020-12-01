"""Temporary module to house custom exceptions for the api."""


# User exceptions
class UserNotFoundException(Exception):
    """Exception to be raised when a user
    cannot be found.
    """

    pass


# Notification exceptions
class NotificationNotFoundException(Exception):
    """Exception to be raised when a user notification
    cannot be found.
    """

    pass


# Chat Exceptions
class ChatNotFoundException(Exception):
    """Exception to be raised when a particular chat
    cannot be found.
    """

    pass


class ChatRequestNotFoundException(Exception):
    """Exception to be raised when a chat request
    cannot be found.
    """

    pass


class ChatMessageNotFoundException(Exception):
    """Exception to be raised when a chat message
    cannot be found.
    """

    pass


class ChatCapacityReachedException(Exception):
    """Exception to be raised when a chat
    is at its capacity and cannot accept any
    more members.
    """

    pass


class ChatMemberNotFoundException(Exception):
    """Exception to be raised when a given user
    cannot be identified as a member of a chat.
    """

    pass


class DuplicateChatRequestException(Exception):
    """Exception to be raised when a user has made
    a duplicate request to join a chat.
    """

    pass


# Community exceptions
class CommunityMemberNotFoundException(Exception):
    """Exception to be raised when a given user 
    cannot be identified as a member of a community.
    """

    pass


class CommunityNotFoundException(Exception):
    """Exception to be raised when a community cannot
    be found.
    """

    pass


class CommunityNameAlreadyExistsException(Exception):
    """Exception to be raised when a community already
    exists the the provided name.
    """

    pass

