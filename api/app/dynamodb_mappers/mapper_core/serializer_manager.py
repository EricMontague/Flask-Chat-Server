"""This module contains the classes responsible for performing the
actual serialization and deserialization of models and items.
"""


from datetime import datetime, date, time
from app.dynamodb_mappers.mapper_core.exceptions import UnserialializableTypeException
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from app.dynamodb_mappers.mapper_core.utils import (
    TypeValidator, 
    DateTimeParser, 
    get_enum_member, 
    convert_decimal_to_float_or_int,
    DynamoDBType,
    SET_TYPES
)
from pprint import pprint


class SerializerManager:
    """Class to unify and extend the functionality of boto3's TypeSerializer and 
    TypeDeserializer classes.
    """

    def __init__(self, serializer, deserializer):
        self._serializer = serializer
        self._deserializer = deserializer

    def serialize(self, field, value, **kwargs):
        """Serialize the given value to the correct DynamoDB data type."""
        try:
            serialized_value = self._serializer.serialize(value)
        except TypeError:
            serialized_value = self._serialize_unsupported_types(field, value, **kwargs)
        return serialized_value

    def deserialize(self, field, value, **kwargs):
        """Deserialize the given value from a DynamoDB item or data type
        to a native python value.
        """
        deserialized_value = self._deserialize_unsupported_types(field, value, **kwargs)
        if not deserialized_value:
            deserialized_value = self._deserializer.deserialize(value)
            if TypeValidator.is_decimal(deserialized_value):
                deserialized_value = convert_decimal_to_float_or_int(deserialized_value)
        return deserialized_value

    def _serialize_unsupported_types(self, field, value, **kwargs):
        """Method to serialize types not natively supported by boto3's TypeSerializer."""
        if TypeValidator.is_type_set(value, TypeValidator.is_enum):
            enum_set = {getattr(element, kwargs["enum_attribute"]) for element in value}
            serialized_value = self._serializer.serialize(enum_set)
        elif TypeValidator.is_enum(value):
            enum_value = getattr(value, kwargs["enum_attribute"])
            serialized_value = self._serializer.serialize(enum_value)
        elif TypeValidator.is_datetime(value):
            formatted_datetime = datetime.strftime(value, kwargs["datetime_format"])
            serialized_value = self._serializer.serialize(formatted_datetime)
        elif TypeValidator.is_date(value):
            formatted_date = date.strftime(value, kwargs["date_format"])
            serialized_value = self._serializer.serialize(formatted_date)
        elif TypeValidator.is_time(value):
            formatted_time = datetime.strftime(value, kwargs["time_format"])
            serialized_value = self._serializer.serialize(formatted_time)
        else:
            raise UnserialializableTypeException(
                f"Unsupported type. Could not serialize field: {field}"
            )
        return serialized_value

    def _deserialize_unsupported_types(self, field, value, **kwargs):
        """Method to deserialize types not natively support by boto3's TypeDeserializer."""
        deserialized_value = None
        if TypeValidator.is_dict(value):
            inner_value = list(value.values())[0]
        if kwargs.get("enum"):
            data_type = list(value.keys())[0]
            if data_type == DynamoDBType.LIST:
                deserialized_value = [
                    get_enum_member(kwargs["enum"], element)
                    for element in inner_value
                ]
            elif data_type in SET_TYPES:
                deserialized_value = {
                    get_enum_member(kwargs["enum"], element)
                    for element in inner_value
                }
            else:
                deserialized_value = get_enum_member(kwargs["enum"], inner_value)
        else:
            deserialized_value = (
                DateTimeParser.parse_datetime_string(inner_value, kwargs["datetime_format"])
                or DateTimeParser.parse_date_string(inner_value, kwargs["date_format"])
                or DateTimeParser.parse_time_string(
                    inner_value, kwargs["time_format"]
                )
            )
        return deserialized_value


serializer_manager = SerializerManager(TypeSerializer(), TypeDeserializer())
