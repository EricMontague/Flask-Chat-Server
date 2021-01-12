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
    _user_id = ma.UUID(dump_only=True, data_key="user_id")
    _content = ma.Str(
        dump_only=True, data_key="content", validate=validate.Length(min=1, max=500)
    )
    _created_at = ma.DateTime(dump_only=True, data_key="timestamp")
    _reactions = ma.List(
        EnumField(Reaction),
        dump_only=True
    )
    _read = ma.Boolean(required=True)
    _editted = ma.Boolean(dump_only=True)
    resource_type = ma.Str(dump_only=True, default="Message")

    # Links
    user_url = ma.URLFor("api.get_user", user_id="<_user_id>")


class PrivateChatMessageSchema(MessageSchema):
    """Class to serialize and deserialize message models for 
    private chats.
    """

    RESOURCE_NAME = "private_chat_message"
    COLLECTION_NAME = "private_chat_messages"

    class Meta:
        unknown = EXCLUDE

    self_url = ma.URLFor(
        "api.get_private_chat_message", private_chat_id="<_chat_id>", message_id="<_id>"
    )


class GroupChatMessageSchema(MessageSchema):
    """Class to serialize and deserialize message models for
    group chats.
    """

    RESOURCE_NAME = "group_chat_message"
    COLLECTION_NAME = "group_chat_messages"

    class Meta:
        unknown = EXCLUDE

    self_url = ma.URLFor(
        "api.get_group_chat_message", group_chat_id="<_chat_id>", message_id="<_id>"
    )

