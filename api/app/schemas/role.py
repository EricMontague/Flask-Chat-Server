"""This module contains the marshmallow schema for serializing
and deserializing Role models.
"""


from app.extensions import ma
from app.models import RoleName, RolePermission
from app.schemas.enum_field import EnumField
from marshmallow import validate


class RoleSchema(ma.Schema):
    """Class to serialize and deserialize Role models."""

    name = EnumField(RoleName)
    permissions = ma.List(
        EnumField(RolePermission),
        required=True
        # validate=validate.OneOf([perm.name for perm in RolePermission])
    )

