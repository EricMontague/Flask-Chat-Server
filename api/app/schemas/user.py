"""This module contains the schema for serializing and deserializing
User models.
"""


from app.extensions import ma
from app.schemas.location import LocationSchema
from app.schemas.image import ImageSchema
from marshmallow import validate



# Edge cases
# Role - A user should never send this on a POST request
# password - Should never be sent out 
# created_at - should never be sent on a POST request and should never be updated
# last_seen_at - should never be sent on a POST request and should never be updated


class UserSchema(ma.Schema):
    """Class to serialize and deserialize User models."""

    _id = ma.UUID(required=True, data_key="id") # will exclude this on POST requests: schema.load(partial=("id",))
    username = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    name = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    email = ma.Email(required=True, validate=validate.Length(min=1, max=32))
    _created_at = ma.DateTime(required=True, data_key="joined_on")  # defaults to ISO 8601
    last_seen_at = ma.DateTime(required=True)  # defaults to ISO 8601
    bio = ma.Str(validate=validate.Length(max=280))
    location = ma.Nested(LocationSchema, required=True)
    avatar = ma.Nested(ImageSchema)
    cover_photo = ma.Nested(ImageSchema)