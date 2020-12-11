"""This module contains exceptions for the DynamoDB Mapper package."""


class DynamoDBMapperException(Exception):
    """Base class for all mapper class related exceotions."""


class MapperInstanceResolutionException(DynamoDBMapperException, TypeError):
    """Raised when mapper to instantiate is neither a ModelMapper class nor 
    an instance.
    """


class UnserialializableTypeException(DynamoDBMapperException, TypeError):
    """Raised when an attribute cannot be serialized to a known type."""


class ModelNotSetException(DynamoDBMapperException, ValueError):
    """Raised when a model hasn't been set on a ModelMapper."""
