"""Temporary module to house custom exceptions for the api."""


class NotificationNotFoundException(Exception):
    """Exception to be raised when a user notification
    cannot be found.
    """

    pass


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


class CommunityNotFoundException(Exception):
    """Exception to be raised when a community cannot
    be found.
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


class CommunityMemberNotFoundException(Exception):
    """Exception to be raised when a given user 
    cannot be identified as a member of a community.
    """

    pass

