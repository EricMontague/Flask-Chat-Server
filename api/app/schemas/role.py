"""This module contains the marshmallow schema for serializing
and deserializing Role models.
"""


from app.extensions import ma
from app.models import RolePermission
from marshmallow import validate


class RoleSchema(ma.Schema):
    """Class to serialize and deserialize Role models."""

    name = ma.Str(required=True)
    permissions = ma.List(required=True, validate=validate.OneOf(
        [perm.name for perm in RolePermission]
    ))
    