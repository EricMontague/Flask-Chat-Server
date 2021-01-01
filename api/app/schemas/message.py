"""This module contains a marshmallow schemas used for serializing abd
deserializing message models.
"""


from app.extensions import ma
from marshmallow import validate, EXCLUDE
from app.schemas.enum_field import EnumField
from app.models import Reaction


class MessageSchema(ma.Schema):
    """Class to serialize and deserialize message models."""

    _id = ma.UUID(dump_only=True, data_key="id")
    _chat_id = ma.UUID(dump_only=True, data_key="chat_id")
    _content = ma.Str(dump_only=True, data_key="content", validate=validate.Length(min=1, max=500))
    _created_at = ma.DateTime(dump_only=True, data_key="timestamp")
    _reactions = ma.List(
        EnumField(Reaction), 
        dump_only=True,
        validate=validate.OneOf([reaction.name for reaction in Reaction])
    )
    _read = ma.Boolean(required=True)
    _editted = ma.Boolean(dump_only=True)
    resource_type = ma.Str(dump_only=True, default="Message")


class PrivateChatMessageSchema(MessageSchema):
    """Class to serialize and deserialize message models for 
    private chats.
    """

    RESOURCE_NAME = "private_chat_message"
    COLLECTION_NAME = "private_chat_messages"

    class Meta:
        unknown = EXCLUDE


class GroupChatMessageSchema(MessageSchema):
    """Class to serialize and deserialize message models for
    group chats.
    """

    RESOURCE_NAME = "group_chat_message"
    COLLECTION_NAME = "group_chat_messages"

    class Meta:
        unknown = EXCLUDE

