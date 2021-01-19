"""This module contains a marshmallow schemas used for serializing abd
deserializing message models.
"""


import uuid
from app.extensions import ma
from marshmallow import validate, EXCLUDE, pre_load, post_load, post_dump
from app.schemas.enum_field import EnumField
from app.models import Reaction, ReactionType, MessageType


class ReactionSchema(ma.Schema):
    """Class to serialize and deserialize Reaction models."""

    class Meta:
        unknown = EXCLUDE

    user_id = ma.UUID(dump_only=True, required=True)
    created_at = ma.DateTime(dump_only=True, data_key="timestamp")
    reaction_type = EnumField(ReactionType, required=True)
    message_id = ma.Str(required=True)
    message_type = EnumField(MessageType, required=True)
    chat_id = ma.UUID(load_only=True, required=True)

    @post_load
    def convert_uuid_to_hex(self, data, **kwargs):
        """Convert all UUID fields to their 32-character hexadecimal equivalent."""
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = data[key].hex
        return data


class MessageSchema(ma.Schema):
    """Class to serialize and deserialize message models."""

    _id = ma.Str(required=True, data_key="id")
    _chat_id = ma.UUID(required=True, data_key="chat_id")
    _content = ma.Str(
        data_key="content", validate=validate.Length(min=1, max=500), required=True
    )
    message_type = EnumField(MessageType, required=True)
    _created_at = ma.DateTime(dump_only=True, data_key="timestamp")
    _sent = ma.Boolean(dump_only=True)
    _editted = ma.Boolean(dump_only=True)

    # Links
    user_url = ma.URLFor("api.get_user", user_id="<_user_id>")

    @post_dump(pass_original=True)
    def inject_extra_fields(self, data, original_model, **kwargs):
        """Post processing method to inject extra fields into the
        serialized data.
        """
        reaction_schema = ReactionSchema()
        data["reactions"] = [
            reaction_schema.dump(reaction) for reaction in original_model.reactions
        ]
        return data

    @post_load
    def convert_uuid_to_hex(self, data, **kwargs):
        """Convert all UUID fields to their 32-character hexadecimal equivalent."""
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = data[key].hex
        return data


class PrivateChatMessageSchema(MessageSchema):
    """Class to serialize and deserialize message models for 
    private chats.
    """

    RESOURCE_NAME = "private_chat_message"
    COLLECTION_NAME = "private_chat_messages"

    class Meta:
        unknown = EXCLUDE

    resource_type = ma.Str(dump_only=True, default="PrivateChatMessage")
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

    community_id = ma.UUID(load_only=True, required=True)
    resource_type = ma.Str(dump_only=True, default="GroupChatMessage")
    self_url = ma.URLFor(
        "api.get_group_chat_message", group_chat_id="<_chat_id>", message_id="<_id>"
    )

