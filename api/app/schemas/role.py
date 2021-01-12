"""This module contains a marshmallow schema for serializing
and deserializing Role models.
"""


from app.extensions import ma
from app.schemas.enum_field import EnumField
from app.models import RolePermission, RoleName
from marshmallow import EXCLUDE


class RoleSchema(ma.Schema):
    """Class to serialize and deserialize role models."""

    class Meta:
        unknown = EXCLUDE

    name = EnumField(RoleName, dump_only=True)
    _permissions = ma.List(EnumField(RolePermission), required=True, data_key="permissions")

 