"""This module contains a marshmallow schema for serializing
and deserializing group chat models.
"""


import uuid
from app.extensions import ma
from marshmallow import validate, EXCLUDE, pre_load, post_load


class GroupChatSchema(ma.Schema):
    """Class for serializing and deserializing GroupChat models."""

    RESOURCE_NAME = "group_chat"
    COLLECTION_NAME = "group_chats"

    class Meta:
        unknown = EXCLUDE
    
    _id = ma.UUID(required=True, data_key="id")
    _community_id = ma.UUID(required=True, data_key="community_id")
    name = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    description = ma.Str(required=True, validate=validate.Length(min=1, max=140))
    resource_type = ma.Str(default="GroupChat", dump_only=True)

    # Links
    self_url = ma.URLFor(
        "api.get_community_group_chat", community_id="<_community_id>", group_chat_id="<_id>"
    )
    messages_url = ma.URLFor("api.get_group_chat_messages", group_chat_id="<_id>")
    community_url = ma.URLFor("api.get_community", community_id="<_id>")
    members_url = ma.URLFor("api.get_community_group_chat_members", community_id="<_community_id>", group_chat_id="<_id>")


    @post_load
    def convert_uuid_to_hex(self, data, **kwargs):
        """Convert all UUID fields to their 32-character hexadecimal equivalent."""
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = data[key].hex
        return data

    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data