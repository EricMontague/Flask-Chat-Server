"""This module contains a custom field for serializing and deserializing
Enum fields.
"""


from enum import Enum
from marshmallow import fields, ValidationError


class EnumField(fields.Field):
    """Field that serializes Enums to strings or integers 
    and deserializes strings or integers to python Enums.
    """

    def __init__(self, enum, serialize_to_name=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(enum, Enum):
            raise ValueError("Please provide an object of type 'Enum'")
        self.enum = enum
        self.serialize_to_name = serialize_to_name

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize python Enum to a string or integer."""
        if self.serialize_to_name:
            return value.name
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        """Deserialize integer or string to a python Enum."""
        if isinstance(value, str):
            return self._deserialize_string(value.upper())
        elif isinstance(value, int):
            return self._deserialize_integer(value)
        else:
            raise ValidationError("Value must be of type 'str' or 'int'")

    def _deserialize_integer(self, enum_key):
        """Return an Enum given an integer as a key"""
        try:
            return self.enum(enum_key)
        except ValueError as err:
            raise ValidationError(
                f"Must be one of: {[enum.value for enum in self.enum]}"
            ) from err

    def _deserialize_string(self, enum_key):
        """Return an Enum given a string as a key"""
        try:
            return self.enum[enum_key]
        except KeyError as err:
            raise ValidationError(
                f"Must be one of: {[enum.name for enum in self.enum]}"
            ) from err
