"""This module contains functions and classes for mapping DynamoDB items to models.
"""


from abc import ABC
from datetime import datetime, date, time
from dataclasses import dataclass
from enum import Enum
from app.dynamodb.constants import PrimaryKeyPrefix
from app.dynamodb.exceptions import (
    MapperInstanceResolutionException,
    ModelNotSetException,
    UnserialializableTypeException,
)
from app.dynamodb.utils import (
    TypeValidator,
    DateTimeParser,
    get_attribute_or_dict_value,
    set_attribute_or_dict_value,
    DynamoDBType,
)
from app.dynamodb.serializer_manager import serializer_manager


def resolve_mapper_instance(cls_or_instance):
    """Return a mapper instance from a ModelMapper class or instance."""
    if isinstance(cls_or_instance, type):
        if not issubclass(cls_or_instance, ModelMapper):
            raise MapperInstanceResolutionException("Class must be of type ModelMapper")
        return cls_or_instance()

    if not isinstance(cls_or_instance, ModelMapper):
        raise MapperInstanceResolutionException(
            "Please provide a valid ModelMapper instance"
        )
    return cls_or_instance


@dataclass(frozen=True)
class Key:

    column_name: str
    prefix: str = ""


class MapperOptions:
    """class Meta options for the :class:`ModelMapper`. Defines defaults."""

    DEFAULT_PK_NAME = "PK"
    DEFAULT_SK_NAME = "SK"

    def __init__(self, meta):
        self.type = getattr(meta, "type_", None)
        self.model = getattr(meta, "model", None)
        if not self.model:
            raise ValueError("`model` field cannot be None")

        self.fields = getattr(meta, "fields", ())
        if not isinstance(self.fields, (list, tuple)):
            raise ValueError("`fields` option must be a list or a tuple")

        self.enum_attribute = getattr(meta, "enum_attribute", "name")
        if self.enum_attribute not in {"name", "value"}:
            raise ValueError("`enum_attribute option must be either `name` or `value`")

        self.attributes_to_monkey_patch = getattr(
            meta, "attributes_to_monkey_patch", ()
        )
        if not isinstance(self.attributes_to_monkey_patch, (list, tuple)):
            raise ValueError(
                "`attributes_to_monkey_patch` option must be a list or a tuple"
            )

        partition_key_prefix = getattr(
            meta, "partition_key_prefix", self.model.__name__.upper() + "#"
        )
        sort_key_prefix = getattr(
            meta, "sort_key_prefix", self.model.__name__.upper() + "#"
        )
        partition_key_name = getattr(meta, "partition_key_name", "PK")
        sort_key_name = getattr(meta, "sort_key_name", "SK")

        self.partition_key = Key(partition_key_name, partition_key_prefix)
        self.sort_key = Key(sort_key_name, sort_key_prefix)

        self.partition_key_attribute = getattr(meta, "partition_key_attribute", "")
        self.sort_key_attribute = getattr(meta, "sort_key_attribute", "")

        self.date_format = getattr(meta, "date_format", "%Y-%m-%d")
        self.time_format = getattr(meta, "time_format", "%H:%M:%S.%f")
        self.datetime_format = getattr(meta, "datetime_format", "%Y-%m-%dT%H:%M:%S.%f")


# TODO - Determine how to intelligently split this class up if necessary
class ModelMapper(ABC):
    """Abstract base class to serialize and deserialize 
    models to and from DynamoDB items.
    """

    OPTIONS_CLASS = MapperOptions
    TYPE_VALIDATOR = TypeValidator
    DATETIME_PARSER = DateTimeParser
    NESTED_MAPPERS = {}
    ENUMS = {}

    class Meta:
        """Class to define options for the ModelMapper class. 
        
        Example usage:

            class Meta:
                model = User
                fields = ("id", "username", "password_hash", "age")
                partition_key_attribute = "id"
                sort_key_attribute = "id"
                type_ = "user"
        

        Available options:

            - ``model``: Instance of a Python object to serialize to a DynamoDB item
            - ``fields``: Tuple or list of fields to be included in the serialized result
            - ``partition_key_name``: String that is the name of the partition key for the
            serialized item
            - ``partition_key_prefix``: Prefix to be added to the beginning of the partition key
            - ``partition_key_attribute``: Attribute of the model to be used to create the 
            partition key
            - ``sort_key_name``: String that is the name of the sort key for the serialized item
            - ``sort_key_prefix``: Prefix to be added to the beginning of the sort key
            - ``sort_key_attribute``: Attribute of the model to be used to create the sort key
            - ``date_format``: Format for attributes of type datetime.date
            - ``time_format``: Format for attributes of type datetime.time
            -  ``datetime_format``: Format for attributes of type datetime.datetime
            - ``enum_attribute``: String that indicates which value of an attribute of type 
            enum.Enum to use
            - ``type_``: String that indicates the type of the item
            


        Default Values:
            model = None
            fields = ()
            partition_key_name = "PK"
            parition_key_prefix = None
            partition_key_attribute = None
            sort_key_name = "SK"
            sort_key_prefix = None
            sort_key_attribute = None
            date_format = "%Y-%m-%d"
            time_format = "%H:%M:%S.%f"
            datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
            enum_attribute = "name"
            type_ = None
        """

    def __init__(self, ignore_partition_key=False):
        self._options = self.OPTIONS_CLASS(self.Meta())
        self.ignore_partition_key = ignore_partition_key
        self._serializer_manager = serializer_manager

    def key(self, partition_key_value, sort_key_value=None):
        """Return a dictionary containing the formatted primary key for
        the item.
        """
        pk_name = self._options.partition_key.column_name
        partition_key = self._options.partition_key.prefix + str(partition_key_value)
        if not sort_key_value:
            return {
                pk_name: self._serializer_manager.serialize("", partition_key),
            }
        sk_name = self._options.sort_key.column_name
        sort_key = self._options.sort_key.prefix + str(sort_key_value)
        return {
            pk_name: self._serializer_manager.serialize("", partition_key),
            sk_name: self._serializer_manager.serialize("", sort_key),
        }

    def serialize_from_model(
        self,
        model,
        partition_key_value=None,
        sort_key_value=None,
        additional_attributes={},
    ):
        """Serialize the given model to a DynamoDB item."""
        item = self._serialize(model, partition_key_value, sort_key_value)
        self._serialize_additional_attributes(item, additional_attributes)
        return item

    def deserialize_to_model(self, item):
        """Deserialize the given item to a model."""
        if not self._options.model:
            raise ModelNotSetException("Please set a model in the Mapper's model class")
        model_dict = self._deserialize(item)
        model_instance = self._options.model(**model_dict)
        self._deserialize_additional_attributes(
            model_instance, item, self._options.attributes_to_monkey_patch
        )
        return model_instance

    @staticmethod
    def merge_items(*items):
        """Merge an arbitary number of DynamoDB items into a single itme."""
        merged_item = {}
        for item in items:
            merged_item.update(item)
        return merged_item

    def _serialize(self, model_or_dict, partition_key_value=None, sort_key_value=None):
        """Serialize the given model or dictionary to a DynamoDB item."""
        item = {}
        if not self.ignore_partition_key:
            primary_key = self._construct_primary_key(
                model_or_dict, partition_key_value, sort_key_value
            )
            item.update(primary_key)
        for field in self._options.fields:
            value = get_attribute_or_dict_value(model_or_dict, field)
            item[field] = self._handle_serialization(field, value)
        if self._options.type is not None:
            item["type"] = self._serializer_manager.serialize(
                "type", self._options.type
            )
        return item

    def _handle_serialization(self, field, value):
        """Serialize the given field value based on its type."""
        options = {
            "datetime_format": self._options.datetime_format,
            "date_format": self._options.date_format,
            "time_format": self._options.time_format,
            "enum_attribute": self._options.enum_attribute,
        }
        if self.TYPE_VALIDATOR.is_set(value):
            serialized_value = self._serializer_manager.serialize(
                field, value, **options
            )
        elif self.TYPE_VALIDATOR.is_list(value) or self.TYPE_VALIDATOR.is_tuple(value):
            serialized_value = {
                "L": [self._handle_serialization(field, element) for element in value]
            }
        elif self.TYPE_VALIDATOR.is_dict(value):
            serialized_value = {
                "M": dict(
                    [
                        (k, self._handle_serialization(field, v))
                        for k, v in value.items()
                    ]
                )
            }
        elif field in self.NESTED_MAPPERS:
            mapper = resolve_mapper_instance(self.NESTED_MAPPERS[field])
            serialized_value = {"M": mapper.serialize_from_model(value)}
        else:
            serialized_value = self._serializer_manager.serialize(
                field, value, **options
            )
        return serialized_value

    def _serialize_additional_attributes(self, item, attributes):
        """Serialize and add additional attributes to the item."""
        for attribute_name in attributes:
            item[attribute_name] = self._handle_serialization(
                attribute_name, attributes[attribute_name]
            )

    def _deserialize(self, item):
        """Deserialize the given item to a python dictionary."""
        attributes_to_skip = set(self._options.attributes_to_monkey_patch)
        model_dict = {}
        for field in self._options.fields:
            if field not in attributes_to_skip:
                value = item[field]
                model_dict[field.lstrip("_")] = self._handle_deserialization(
                    field, value, item
                )
        return model_dict

    # TODO - Break up into separate methods
    def _handle_deserialization(self, field, value, item):
        """Deserialize the given field value based on its type."""
        options = {
            "datetime_format": self._options.datetime_format,
            "date_format": self._options.date_format,
            "time_format": self._options.time_format,
        }
        data_type = None
        if self.TYPE_VALIDATOR.is_dict(value):
            data_type = list(value.keys())[0]
        if data_type == DynamoDBType.LIST:
            deserialized_value = [
                self._handle_deserialization(field, element, value)
                for element in value["L"]
            ]
        elif field in self.NESTED_MAPPERS:
            mapper = resolve_mapper_instance(self.NESTED_MAPPERS[field])
            if list(value["M"].keys())[0] in mapper._options.fields:
                deserialized_value = mapper.deserialize_to_model(value["M"])
            else:  # Dictionary of dictionaries
                deserialized_value = {}
                for k, v in value["M"].items():
                    deserialized_value[k] = mapper.deserialize_to_model(v["M"])
        elif (
            data_type == DynamoDBType.MAP
        ):  # this may be unecessary since boto3 can handle Maps
            deserialized_value = {}
            for k, v in value.items():
                deserialized_value[k] = self._handle_deserialization(
                    field, v, item["M"]
                )
        else:
            # Since the field may be an enum, premptively load it into the options dict
            options["enum"] = self.ENUMS.get(field)
            deserialized_value = self._serializer_manager.deserialize(
                field, value, **options
            )
        return deserialized_value

    def _deserialize_additional_attributes(self, model_or_dict, item, attributes):
        """Add additional attributes to the model or dictionary after deserialization
        has taken place.
        """
        for attribute in attributes:
            value = item[attribute]
            deserialized_value = self._handle_deserialization(attribute, value, item)
            set_attribute_or_dict_value(model_or_dict, attribute, deserialized_value)

    def _construct_primary_key(self, model, partition_key_value, sort_key_value):
        """Return a formatted primary key based on the passed in parameters
        and options set on the Mapper class. Values passed into this function
        override the values set in the options class
        """
        # Passed in PK and SK values override values set in the options class
        if partition_key_value and sort_key_value:
            primary_key = self.key(partition_key_value, sort_key_value)
        # Both not passed in, use options class values
        elif not partition_key_value and not sort_key_value:
            primary_key = self.key(
                get_attribute_or_dict_value(
                    model, str(self._options.partition_key_attribute)
                ),
                get_attribute_or_dict_value(
                    model, str(self._options.sort_key_attribute), None
                ),
            )
        # Partition key but no sort key
        elif partition_key_value and not sort_key_value:
            primary_key = self.key(
                partition_key_value,
                get_attribute_or_dict_value(
                    model, str(self._options.sort_key_attribute), None
                ),
            )
        # Sort Key but no partition key
        elif not partition_key_value and sort_key_value:
            primary_key = self.key(
                get_attribute_or_dict_value(
                    model, str(self._options.partition_key_attribute)
                ),
                sort_key_value,
            )
        return primary_key

