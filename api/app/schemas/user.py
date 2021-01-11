"""This module contains the schema for serializing and deserializing
User models.
"""


from app.extensions import ma
from app.schemas.location import LocationSchema
from app.schemas.image import ImageSchema
from marshmallow import validate, pre_load, post_load, post_dump, EXCLUDE


class UserSchema(ma.Schema):
    """Class to serialize and deserialize User models."""

    COLLECTION_NAME = "users"
    RESOURCE_NAME = "user"

    class Meta:
        unknown = EXCLUDE

    _id = ma.UUID(data_key="id", dump_only=True)
    username = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    name = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    email = ma.Email(required=True, validate=validate.Length(min=1, max=32))
    _created_at = ma.DateTime(data_key="joined_on", dump_only=True)  # defaults to ISO 8601
    last_seen_at = ma.DateTime(dump_only=True)  # defaults to ISO 8601
    password = ma.Str(required=True, load_only=True)
    bio = ma.Str(validate=validate.Length(max=280))
    resource_type = ma.Str(default="User", dump_only=True)
    location = ma.Nested(LocationSchema, required=True)
    avatar = ma.Nested(ImageSchema, dump_only=True)
    cover_photo = ma.Nested(ImageSchema, dump_only=True)

    # links
    self_url = ma.URLFor("api.get_user", user_id="<_id>")
    communities_url= ma.URLFor("api.get_user_communities", user_id="<_id>")
    notifications_url = ma.URLFor("api.get_user_notifications", user_id="<_id>")
    private_chats_url = ma.URLFor("api.get_user_private_chats", user_id="<_id>")
    group_chats_url = ma.URLFor("api.get_user_group_chats", user_id="<_id>")

    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data

    @post_dump(pass_original=True)
    def inject_extra_fields(self, data, original_model, **kwargs):
        """Post processing method to inject extra fields into the
        serialized data.
        """
        if hasattr(original_model, "role"):
            data["is_admin"] = original_model.is_admin()
        return data

