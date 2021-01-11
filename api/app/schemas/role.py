"""This module contains a marshmallow schema for serializing
and deserializing Role models.
"""


from app.extensions import ma
from app.schemas.enum_field import EnumField
from app.models import RolePermission, RoleName
from marshmallow import validate, EXCLUDE, pre_load, validates


class RoleSchema(ma.Schema):
    """Class to serialize and deserialize role models."""

    class Meta:
        unknown = EXCLUDE

    name = EnumField(RoleName, dump_only=True)
    _permissions = ma.List(EnumField(RolePermission), required=True, data_key="permissions")

    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data