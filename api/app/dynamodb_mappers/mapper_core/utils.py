"""This module contains utility functions and classes to be used in the
DynamoDB Mapper package.
"""


from collections import abc
from collections.abc import Iterable
from enum import Enum
from datetime import datetime, date, time
from decimal import Decimal


class DynamoDBType:
    """Class that holds constants of DynamoDB data types."""

    STRING = "S"
    NUMBER = "N"
    BINARY = "B"
    STRING_SET = "SS"
    NUMBER_SET = "NS"
    BINARY_SET = "BS"
    NULL = "NULL"
    BOOLEAN = "BOOL"
    MAP = "M"
    LIST = "L"


SET_TYPES = {
    "BS": DynamoDBType.BINARY_SET,
    "SS": DynamoDBType.STRING_SET,
    "NS": DynamoDBType.NUMBER_SET,
}


class TypeValidator:
    """Class used to validate various python types for
    the ModelMapper class
    """

    @staticmethod
    def is_dict(value):
        """Return True if the value is a python dictionary, otherwise return False."""
        return isinstance(value, dict)
    
    @staticmethod
    def is_set(value):
        """Return True if the value is a python set, otherwise return False."""
        return isinstance(value, abc.Set)
    
    @staticmethod
    def is_list(value):
        """Return True if the value is a python list, otherwise return False."""
        return isinstance(value, list)
        
    @staticmethod
    def is_tuple(value):
        """Return True if the value is a python tuple, otherwise return False."""
        return isinstance(value, tuple)
            
    @staticmethod
    def is_enum(value):
        """Return True if the value is an Enum, otherwise return False."""
        return isinstance(value, Enum)
            
    @staticmethod
    def is_datetime(value):
        """Return True if the value is a datetime object, otherwise return False."""
        return isinstance(value, datetime)

    @staticmethod
    def is_date(value):
        """Return True if the value is a date object, otherwise return False."""
        return isinstance(value, date)
           
    @staticmethod
    def is_time(value):
        """Return True if the value is a time object, otherwise return False."""
        return isinstance(value, time)
    
    @staticmethod
    def is_iterable(value):
        """Return True if the value is iterable, otherwise return False
        """
        return isinstance(value, Iterable)

    @staticmethod
    def is_string(value):
        """Return True if the value is a string, otherwise return False."""
        return isinstance(value, str)

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
    
    @staticmethod
    def is_decimal(value):
        """Return True if the given value is of type decimal.Decimal, else
        return false.
        """
        return isinstance(value, Decimal)

    @staticmethod
    def is_nested_dict(dict_):
        """Return True if the dictionary is nested, otherwise return False."""
        return any(TypeValidator.is_dict(value) for value in dict_.values())


class DateTimeParser:
    """Class to parse date, time and datetime strings."""

    @staticmethod
    def parse_datetime_string(string, format):
        try:
            return datetime.strptime(string, format)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def parse_date_string(string, format):
        try:
            return datetime.strptime(string, format).date()
        except (ValueError, TypeError):
            return None

    @staticmethod
    def parse_time_string(string, format):
        try:
            return datetime.strptime(string, format).time()
        except (ValueError, TypeError):
            return None


def get_enum_member(enum, name_or_value):
    """Return an enum object given a value matching one of its members
    either by name or value.
    """
    try:
        return enum[name_or_value] # Get by name
    except KeyError:
        return enum(int(name_or_value)) # Get by value


def is_empty_collection(value):
    """Return True if the given value is an empty list, tuple, set,
    or dictionary, else return False.
    """
    return (
        TypeValidator.is_iterable(value)
        and not TypeValidator.is_string(value)
        and len(value) == 0
    )
    

def convert_decimal_to_float_or_int(value):
    """Convert a object of type decimal.Decimal to a float or
    and int based on its value.
    """
    if int(value) == value: # it's an integer
        return int(value)
    return float(value)