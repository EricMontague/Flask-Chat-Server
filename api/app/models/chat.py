"""This module contains models to represent various types of
chats in the application.
"""


from abc import ABC


class Chat(ABC):
    """Abstract base class that represents a chat."""

    def __init__(self, id, name, description):
        self._id = id
        self.name = name
        self.description = description
        self._messages = {}
        self._members = {}

    def post_message(self, message):
        """Add a message to the chat's list of messages."""
        self._messages[message.id] = message
        return True

    def edit_message(self, message_id, new_content):
        """Edit a message in the chat."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages[message_id].edit(new_content)

    def delete_message(self, message_id):
        """Delete the given message from the chat."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages.pop(message_id)

    def has_message(self, message_id):
        """Return True if a message with the given id exists
        in the chat, otherwise return False.
        """
        return message_id in self._messages

    def react_to_message(self, message_id, reaction):
        """Add a reaction to the given message."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages[message_id].add_reaction(reaction)

    @property
    def id(self):
        """Return the chat id."""
        return self._id

    @property
    def messages(self):
        """Return a list of the chat's messages sorted
        from most recent to least recent.
        """
        return sorted(self._messages, key=lambda m: m.timestamp)



class PrivateChat(Chat):
    """Class to represent a private chat between two users"""

    CAPACITY = 2

    def __init__(self, id, name, description):
        super().__init__(id, name, description)

    def get_other_user(self, member_id):
        """Return the other user in the private chat."""
        for id in self._members:
            if id != member_id:
                return self._members[id]


class GroupChat(Chat):
    """Class to represent a group chat between one or more users."""

    def __init__(self, id, name, description, capacity, private):
        super().__init__(id, name, description)
        self._capacity = capacity
        self._private = private
        self._num_members = 0
        self._pending_chat_requests = {}

    @property
    def num_members(self):
        """Return the number of members in the group chat."""
        return self._num_members

    def num_members_online(self):
        pass

    def add_member(self, member):
        pass

    def remove_member(self, member_id):
        pass

    def is_member(self, user_id):
        pass
    
    def add_request(self, request):
        pass

    def remove_request(self, user_id):
        pass
    
    def has_pending_request(self, user_id):
        pass

    def is_full(self):
        pass

    def is_private(self):
        """Return True if this group chat is private,
        otherwise return False.
        """
        return self._private



class ChatMessageNotFoundException(Exception):
    """Exception to be raised when a chat message
    cannot be found.
    """

    pass
