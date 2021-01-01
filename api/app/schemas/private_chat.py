"""This module contains an marshmallow schema used
serialize and deserialize PrivateChat models.
"""


from app.extensions import ma
from app.schemas.user import UserSchema


class PrivateChatSchema(ma.Schema):
    """Class to serialize and deserialize PrivateChat models."""

    _id = ma.UUID(dump_only=True)
    primary_user = ma.Nested(UserSchema(), dump_only=True)
    secondary_user = ma.Nested(UserSchema(), dump_only=True)
    resource_type = ma.Str(dump_only=True, default="PrivateChat")

    