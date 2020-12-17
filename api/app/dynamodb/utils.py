"""This module contains utility functions and classes to be used in the
DynamoDB Mapper package.
"""


from collections import abc
from enum import Enum
from datetime import datetime, date, time


class TypeValidator:
    """Class used to validate various python types for
    the ModelMapper class
    """

    @staticmethod
    def is_dict(value):
        """Return True if the value is a python dictionary, otherwise return False."""
        if isinstance(value, dict):
            return True
        return False

    @staticmethod
    def is_set(value):
        """Return True if the value is a python set, otherwise return False."""
        if isinstance(value, abc.Set):
            return True
        return False

    @staticmethod
    def is_list(value):
        """Return True if the value is a python list, otherwise return False."""
        if isinstance(value, list):
            return True
        return False

    @staticmethod
    def is_tuple(value):
        """Return True if the value is a python tuple, otherwise return False."""
        if isinstance(value, tuple):
            return True
        return False

    @staticmethod
    def is_enum(value):
        """Return True if the value is an Enum, otherwise return False."""
        if isinstance(value, Enum):
            return True
        return False

    @staticmethod
    def is_datetime(value):
        """Return True if the value is a datetime object, otherwise return False."""
        if isinstance(value, datetime):
            return True
        return False

    @staticmethod
    def is_date(value):
        """Return True if the value is a date object, otherwise return False."""
        if isinstance(value, date):
            return True
        return False

    @staticmethod
    def is_time(value):
        """Return True if the value is a time object, otherwise return False."""
        if isinstance(value, time):
            return True
        return False

    @staticmethod
    def is_list_like(value):
        """Return True if the value is a list, tuple, or a set, otherwise
        return False
        """
        if (
            TypeValidator.is_set(value)
            or TypeValidator.is_list(value)
            or TypeValidator.is_tuple(value)
        ):
            return True
        return False

    @staticmethod
    def is_type_set(value, validator):
        """Return True if all of the elements in the given set are of
        the same type
        """
        if TypeValidator.is_set(value):
            return all(
                validator(element)
                for element in value
            )
        return False


class DateTimeParser:
    """Class to parse date, time and datetime strings."""

    @staticmethod
    def parse_datetime_string(string, format):
        try:
            return datetime.strptime(string, format)
        except ValueError:
            return None

    @staticmethod
    def parse_date_string(string, format):
        try:
            return datetime.strptime(string, format).date()
        except ValueError:
            return None

    @staticmethod
    def parse_time_string(string, format):
        try:
            return datetime.strptime(string, format).time()
        except ValueError:
            return None


def get_enum_member(enum, name_or_value):
    """Return an enum object given a value matching one of its members
    either by name or value.
    """
    try:
        return enum[name_or_value]
    except KeyError:
        return enum(name_or_value)


def get_attribute_or_dict_value(model_or_dict, attribute_or_key, default=None):
    """Return the value of the matching attribute or key from the given
    model or dictionary.
    """
    if TypeValidator.is_dict(model_or_dict):
        return model_or_dict[attribute_or_key]
    return getattr(model_or_dict, attribute_or_key, default)


def set_attribute_or_dict_value(model_or_dict, attribute_or_key, value):
    """Set the value of the matching attribute or key on the given
    model or in the given dictionary.
    """
    if TypeValidator.is_dict(model_or_dict):
        model_or_dict[attribute_or_key] = value
    else:
        setattr(model_or_dict, attribute_or_key, value)

