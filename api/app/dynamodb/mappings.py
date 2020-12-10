"""This module contains functions and classes for mapping DynamoDB items to models.
"""


from abc import ABC
from datetime import datetime, date, time
from dataclasses import dataclass
from enum import Enum
from app.models import User, Role, RoleName, RolePermission, Location, Image, ImageType
from app.dynamodb.constants import PrimaryKeyPrefix
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


DYNAMODB_TYPE_MAPPING = {
    "str": "S",
    "int": "N",
    "bytes": "B",
    "string_set": "SS",
    "number_set": "NS",
    "binary_set": "BS",
    "float": "S",  # special case. Store floats as strings and convert them back on deserialization
    "dict": "M",
    "list": "L",
    "tuple": "L",
    "None": "NULL",
    "True": "BOOL",
    "False": "BOOL",
}


class DynamoDBMapperException(Exception):
    """Base class for all mapper class related exceotions."""


class MapperInstanceResolutionException(DynamoDBMapperException, TypeError):
    """Raised when mapper to instantiate is neither a ModelMapper class nor 
    an instance.
    """


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


class MapperMeta(type):
    """Metaclass for the Mapper class. Sets the ``opts`` class attribute, which is
    the Schema class's ``class Meta`` options.
    """

    pass


class MapperOptions:
    """class Meta options for the :class:`ModelMapper`. Defines defaults."""

    DEFAULT_PK_NAME = "PK"
    DEFAULT_SK_NAME = "SK"

    def __init__(self, meta):
        self.validate_options(meta)
        self.model = meta.model
        self.included_fields = meta.included_fields
        self.excluded_fields = meta.excluded_fields
        self.enum_attribute = meta.enum_attribute
        self.partition_key = Key(meta.partition_key_name, meta.partition_key_prefix)
        self.sort_key = Key(meta.sort_key_name, meta.sort_key_prefix)
        self.partition_key_attribute = meta.partition_key_attribute
        self.sort_key_attribute = meta.sort_key_attribute
        self.date_format = meta.date_format
        self.time_format = meta.time_format
        self.datetime_format = meta.datetime_format
        

    def validate_options(self, meta):
        """Validate that the option types are correct and that all required
        options are set
        """
        # Validate model option
        if meta.model is None:
            raise ValueError("`model` option must be set")

        # Validate fields options
        if not isinstance(meta.included_fields, (list, tuple)):
            raise ValueError("`included_fields` option must be a list or a tuple")
        if not isinstance(meta.excluded_fields, (list, tuple)):
            raise ValueError("`excluded_fields` option must be a list or a tuple")
        if meta.included_fields and meta.excluded_fields:
            raise ValueError(
                "Cannot set both `included fields` and `excluded fields` options"
            )

        # Validate primary key attributes
        if not meta.partition_key_name:
            raise ValueError("`partition_key_name` attribute not set")

        # Validate enum option
        if meta.enum_attribute not in {"name", "value"}:
            raise ValueError("`enum_attribute option must be either `name` or `value`")


class ModelMapper(ABC):
    """Abstract base class to serialize and deserialize 
    models to and from DynamoDB items.
    """

    OPTIONS_CLASS = MapperOptions
    NESTED_MAPPERS = {}

    def __init__(self, use_sort_key=True):
        self.options = self.OPTIONS_CLASS(self.Meta)
        self.use_sort_key = use_sort_key
        self._serializer = TypeSerializer()
        self._deserializer = TypeDeserializer()

    class Meta:
        """Class to define options for the ModelMapper class. 
        Defaults are already defined for each field
        """

        model = None
        included_fields = ()
        excluded_fields = ()
        partition_key_name = "PK"
        parition_key_prefix = model.__name__.upper() + "#"
        partition_key_attribute = None
        sort_key_name = "SK"
        sort_key_prefix = model.__name__.upper() + "#"
        sort_key_attribute = None
        date_format = "%Y-%m-%d"
        time_format = "%H:%M:%S.%f"
        datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
        enum_attribute = "name"

    def key(self, partition_key_value, sort_key_value=None):
        """Return a dictionary containing the formatted primary key for
        the item.
        """

        pk_name = self.options.partition_key.column_name
        if self.use_sort_key:
            sk_name = self.options.sort_key.column_name
            return {
                pk_name: self.options.partition_key.prefix + str(partition_key_value),
                sk_name: self.options.sort_key.prefix + str(sort_key_value),
            }
        return {
            pk_name: self.options.partition_key.prefix + str(partition_key_value),
        }

    def serialize(self, model, partition_key_value=None, sort_key_value=None):
        """Serialize the given model to a DynamoDB item."""
        primary_key = self._construct_primary_key(
            model, partition_key_value, sort_key_value
        )
        item = {**primary_key}
        if self.options.included_fields:
            fields = self.options.included_fields
        else:
            fields = self.options.excluded_fields

        for field in fields:
            value = getattr(model, field)
            try:
                serialized_value = self._serializer.serialize(value)
            except TypeError:
                serialized_value = self._fallback_serializer(field, value)
            item[field] = serialized_value
        return item

    def _fallback_serializer(self, field, value):
        """Method to serialize types not natively supported by boto3's TypeSerializer."""
        if self.is_enum(value):
            enum_value = getattr(value, self.options.enum_attribute)
            serialized_value = self._serializer.serialize(enum_value)
        elif self.is_datetime(value):
            formatted_datetime = datetime.strftime(value, self.options.datetime_format)
            serialized_value = self._serializer.serialize(formatted_datetime)
        elif self.is_date(value):
            formatted_date = date.strftime(value, self.options.date_format)
            serialized_value = self._serializer.serialize(formatted_date)
        elif self.is_time(value):
            formatted_time = datetime.strftime(value, self.options.time_format)
            serialized_value = self._serializer.serialize(formatted_time)
        elif field in self.NESTED_MAPPERS:
            mapper = resolve_mapper_instance(self.NESTED_MAPPERS[field])
            serialized_value = mapper.serialize(value)  # how to pass pk and sk here?
        else:
            raise TypeError(f"Unsupported type. Could not serialize field: {field}")
        return serialized_value

    def is_enum(self, value):
        """Return True if the value is an Enum, otherwise return False."""
        if isinstance(value, Enum):
            return True
        return False

    def is_datetime(self, value):
        """Return True if the value is a datetime object, otherwise return False."""
        if isinstance(value, datetime):
            return True
        return False

    def is_date(self, value):
        """Return True if the value is a date object, otherwise return False."""
        if issubclass(value, date):
            return True
        return False

    def is_time(self, value):
        """Return True if the value is a time object, otherwise return False."""
        if isinstance(value, time):
            return True
        return False

    def deserialize(self, item, attributes_to_monkey_patch):
        """Deserialize the given item back to a model."""
        pass

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
                getattr(model, str(self.options.partition_key_attribute)),
                getattr(model, str(self.options.sort_key_attribute), None),
            )
        # Partition key but no sort key
        elif partition_key_value and not sort_key_value:
            primary_key = self.key(
                partition_key_value,
                getattr(model, str(self.options.sort_key_attribute), None),
            )
        # Sort Key but no partition key
        elif not partition_key_value and sort_key_value:
            primary_key = self.key(
                getattr(model, str(self.options.partition_key_attribute)),
                sort_key_value,
            )
        return primary_key


class UserMapper(ModelMapper):
    """Class to serialize and deserialize user models to and from
    DynamoDB items.
    """

    class Meta:
        model = User
        excluded_fields = (
            "_notifications",
            "_pending_chat_requests",
            "_private_chats",
            "_group_chats",
            "_communities",
        )
        partition_key_attribute = "_id"
        sort_key_attribute = "_id"

    NESTED_MAPPERS = {
        "location": LocationMapper,
        "avatar": ImageMapper,
        "cover_photo": ImageMapper,
        "role": RoleMapper,
    }


# TODO - Delete these once the Mapper classes are finished
def create_user_from_item(user_item):
    """Create and return a user model from a DynamoDB item."""
    # Remove uneeded attributes
    del user_item["SK"]
    del user_item["type"]
    user_id = user_item.pop("PK")["S"].split("#")[-1]
    user_attributes = {"id": user_id}
    for attribute_name, attribute_value in user_item.items():
        if attribute_name in {"avatar", "cover_photo"}:
            actual_value = create_image_from_map(user_item[attribute_name]["M"])
        elif attribute_name == "location":
            actual_value = create_location_from_map(user_item["location"]["M"])
        elif attribute_name == "role":
            actual_value = create_role_from_map(user_item["role"]["M"])
        elif attribute_name in {"last_seen_at", "created_at"}:
            actual_value = datetime.fromisoformat(attribute_value["S"])
        else:
            actual_value = list(user_item[attribute_name].values())[0]
        user_attributes[attribute_name] = actual_value
    password_hash = user_attributes.pop("password_hash")
    user = User(**user_attributes)
    user._password_hash = password_hash
    return user


def create_location_from_map(location_map):
    """Create and return a location model from a DynamoDB map."""
    location_attributes = {}
    for attribute_name, attribute_value in location_map.items():
        location_attributes[attribute_name] = attribute_value["S"]
    return Location(**location_attributes)


def create_role_from_map(role_map):
    """Create and return a role model from a DynamoDB map."""
    role_attributes = {}
    for attribute_name, attribute_value in role_map.items():
        if attribute_name == "name":
            actual_value = RoleName[attribute_value["S"]]
        elif attribute_name == "permissions":
            actual_value = {RolePermission[perm] for perm in attribute_value["SS"]}
        role_attributes[attribute_name] = actual_value
    return Role(**role_attributes)


def create_image_from_map(image_map):
    """Create and return an image model from a DynamoDB map."""
    image_attributes = {}
    for attribute_name, attribute_value in image_map.items():
        if attribute_name in {"width", "height"}:
            actual_value = int(attribute_value["N"])
        elif attribute_name == "image_type":
            actual_value = ImageType[attribute_value["S"]]
        elif attribute_name == "uploaded_at":
            actual_value = datetime.fromisoformat(attribute_value["S"])
        else:
            actual_value = attribute_value["S"]
        image_attributes[attribute_name] = actual_value
    return Image(**image_attributes)

