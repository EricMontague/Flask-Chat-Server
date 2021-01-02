"""This module contains an marshmallow schema used
serialize and deserialize PrivateChat models.
"""


from app.extensions import ma
from app.schemas.user import UserSchema


class PrivateChatSchema(ma.Schema):
    """Class to serialize PrivateChat models."""

    _id = ma.UUID(dump_only=True)
    _primary_user = ma.Nested(UserSchema(), dump_only=True, data_key="primary_user")
    _secondary_user = ma.Nested(UserSchema(), dump_only=True, data_key="secondary_user")
    resource_type = ma.Str(dump_only=True, default="PrivateChat")
    messages_url = ma.URLFor("api.get_private_chat_messages", private_chat_id="<_id>")
    