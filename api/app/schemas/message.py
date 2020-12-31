"""This module contains a marshmallow schemas used for serializing abd
deserializing message models.
"""


from app.extensions import ma



class MessageSchema(ma.Schema):
    """Class to serialize and deserialize message models."""

    pass


class PrivateChatMessageSchema(ma.Schema):
    """Class to serialize and deserialize message models for 
    private chats.
    """

    pass


class GroupChatMessageSchema(ma.Schema):
    """Class to serialize and deserialize message models for
    group chats.
    """

    pass

