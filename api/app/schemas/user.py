"""This module contains the schema for serializing and deserializing
User models.
"""


from app.extensions import ma
from app.schemas.location import LocationSchema
from app.schemas.image import ImageSchema
from marshmallow import validate, pre_load, post_load




# Edge cases
# Role - A user should never send this on a POST request
# password - Should never be sent out 
# created_at - should never be sent on a POST request and should never be updated
# last_seen_at - should never be sent on a POST request and should never be updated


class UserSchema(ma.Schema):
    """Class to serialize and deserialize User models."""

    _id = ma.UUID(data_key="id") # will exclude this on POST requests: schema.load(partial=("id",))
    username = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    name = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    email = ma.Email(required=True, validate=validate.Length(min=1, max=32))
    _created_at = ma.DateTime(data_key="joined_on")  # defaults to ISO 8601
    last_seen_at = ma.DateTime()  # defaults to ISO 8601
    password = ma.Str(required=True, load_only=True)
    bio = ma.Str(validate=validate.Length(max=280))
    resource_type = ma.Str(default="User", dump_only=True)

    location = ma.Nested(LocationSchema, required=True)
    avatar = ma.Nested(ImageSchema)
    cover_photo = ma.Nested(ImageSchema)
    
    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data

    @post_load
    def convert_uuid_to_hex(self, data, many, **kwargs):
        """Convert the user's id to its hex value."""
        data["_id"] = data["_id"].hex
        return data
