"""This module contains the schema for serializing and deserializing
User models.
"""


from app.extensions import ma
from app.schemas.location import LocationSchema
from app.schemas.role import RoleSchema
from app.schemas.image import ImageSchema
from marshmallow import validate


class UserSchema(ma.Schema):
    """Class to serialize and deserialize User models."""

    id = ma.UUID()
    password = ma.Str(load_only=True)
    username = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    name = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    email = ma.Email(required=True, validate=validate.Length(min=1, max=32))
    created_at = ma.DateTime(required=True)  # defaults to ISO 8601
    last_seen_at = ma.DateTime(required=True)  # defaults to ISO 8601
    bio = ma.Str(validate=validate.Length(max=280))
    role = ma.Nested(RoleSchema, required=True)
    location = ma.Nested(LocationSchema, required=True)
    avatar = ma.Nested(ImageSchema, required=True)
    cover_photo = ma.Nested(ImageSchema, required=True)
