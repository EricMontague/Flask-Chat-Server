"""This module contains an marshmallow schema used
serialize PrivateChat models.
"""


import uuid
from app.extensions import ma
from app.schemas.user import UserSchema
from marshmallow import post_load


class PrivateChatSchema(ma.Schema):
    """Class to serialize PrivateChat models."""

    RESOURCE_NAME = "private_chat"
    COLLECTION_NAME = "private_chats"

    _id = ma.UUID(required=True, data_key="id")
    _primary_user = ma.Nested(UserSchema(), dump_only=True, data_key="primary_user")
    _secondary_user = ma.Nested(UserSchema(), dump_only=True, data_key="secondary_user")
    resource_type = ma.Str(dump_only=True, default="PrivateChat")

    # Links
    messages_url = ma.URLFor("api.get_private_chat_messages", private_chat_id="<_id>")


    @post_load
    def convert_uuid_to_hex(self, data, **kwargs):
        """Convert all UUID fields to their 32-character hexadecimal equivalent."""
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = data[key].hex
        return data
    
    
    