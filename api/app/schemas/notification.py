"""This module contains a marshmallow schema used for serializing
and deserializing notification models.
"""


from app.extensions import ma
from app.schemas.enum_field import EnumField
from app.models import NotificationType
from marshmallow import validate, EXCLUDE, ValidationError, validates_schema, pre_load


class NotificationSchema(ma.Schema):
    """Class to serialize and deserialize notification
    models.
    """

    RESOURCE_NAME = "notification"
    COLLECTION_NAME = "notifications"

    class Meta:
        unknown = EXCLUDE

    _id = ma.Str(required=True, data_key="id", dump_only=True)
    _user_id = ma.UUID(required=True, data_key="user_id", dump_only=True)
    _notification_type = EnumField(NotificationType, required=True, data_key="notification_type", dump_only=True)
    _message = ma.Str(required=True, data_key="message", validate=validate.Length(min=1, max=64), dump_only=True)
    _target_url = ma.URL(required=True, data_key="target_url", dump_only=True)
    _created_at = ma.DateTime(data_key="timestamp", dump_only=True)  # defaults to ISO 8601
    _read = ma.Boolean(data_key="read")
    _seen = ma.Boolean(data_key="seen")
    resource_type = ma.Str(default="Notification", dump_only=True)

    @validates_schema
    def validate_read_and_seen(self, data, **kwargs):
        """Raise a ValidationError if both read and seen aren't present
        in the data on load.
        """
        if "_read" not in data and "_seen" not in data:
            raise ValidationError(
                "Please provide at least one field to update. Valid fields to update are: read, seen"
            )
        return data

    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data