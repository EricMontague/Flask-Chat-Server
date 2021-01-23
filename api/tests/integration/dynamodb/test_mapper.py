"""This file contains integration tests for serializing and deserializing
models to and from DynamoDB items.

Note: These tests are dependent on the functionality of the boto3 libary
"""


import pytest
from app.dynamodb_mappers.mapper_core.exceptions import ModelNotSetException


def test_create_primary_key_without_sort_key_value(test_key_prefix, test_mapper):
    """Test that a primary key is properly created if a sort key is not provided
    on the mapper class.
    """
    partition_key = "12345"
    primary_key = test_mapper.key(partition_key)
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + "12345"
    assert "SK" not in primary_key


def test_create_primary_key_with_sort_key_value(test_key_prefix, test_mapper):
    """Test that a primary key is properly created if a sort key IS provided
    on the mapper class.
    """
    partition_key = "12345"
    sort_key = "6789"
    primary_key = test_mapper.key(partition_key, sort_key)
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + "12345"
    assert "SK" in primary_key
    assert primary_key["SK"]["S"] == test_key_prefix + "6789"


def test_construct_primary_key_with_partition_and_sort_key(
    test_key_prefix, test_model, test_mapper
):
    """Test of inner construct primary key method to make sure that if
    a partition and sort key are provided, that a primary key is made with
    both of them included.
    """
    partition_key = "12345"
    sort_key = "6789"
    primary_key = test_mapper._construct_primary_key(
        test_model, partition_key_value=partition_key, sort_key_value=sort_key
    )
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + "12345"
    assert "SK" in primary_key
    assert primary_key["SK"]["S"] == test_key_prefix + "6789"


def test_construct_primary_key_without_partition_or_sort_key(
    test_key_prefix, test_model, test_mapper
):
    """Test of inner construct primary key method to make sure that if
    a partition and sort key both not provided, that a primary key is made with
    using the attributes provided on the options class
    """
    primary_key = test_mapper._construct_primary_key(
        test_model, 
        partition_key_value=None, 
        sort_key_value=None
    )
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + test_model.id
    assert "SK" in primary_key
    assert primary_key["SK"]["S"] == test_key_prefix + test_model.id


def test_construct_primary_key_with_partition_key_but_not_sort_key(
    test_key_prefix, test_model, test_mapper
):
    """Test of inner construct primary key method to make sure that if
    a partition key is provided, but the sort key is not that a primary key is made with
    using the passed in partition key value and the sort key from the options class
    """
    partition_key = "1234"
    primary_key = test_mapper._construct_primary_key(
        test_model, 
        partition_key_value=partition_key, 
        sort_key_value=None
    )
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + "1234"
    assert "SK" in primary_key
    assert primary_key["SK"]["S"] == test_key_prefix + test_model.id


def test_construct_primary_key_with_sort_key_but_not_partition_key(
    test_key_prefix, test_model, test_mapper
):
    """Test of inner construct primary key method to make sure that if
    a sort key is provided, but the partition key is not that a primary key is made with
    using the passed in sort key value and the partition key from the options class
    """
    sort_key = "5678"
    primary_key = test_mapper._construct_primary_key(
        test_model, 
        partition_key_value=None, 
        sort_key_value=sort_key
    )
    assert "PK" in primary_key
    assert primary_key["PK"]["S"] == test_key_prefix + test_model.id
    assert "SK" in primary_key
    assert primary_key["SK"]["S"] == test_key_prefix + "5678"


def test_serialization(test_key_prefix, test_model, test_mapper):
    """High level test to confirm that a broad range of types are handled and 
    serialized properly.
    """
    item = test_mapper.serialize_from_model(test_model)
    assert "PK" in item
    assert "SK" in item
    assert "type" in item
    for attribute in test_model.__dict__:
        assert attribute in item

    assert item["PK"]["S"] == test_key_prefix + test_model.id
    assert item["SK"]["S"] == test_key_prefix + test_model.id
    assert item["type"]["S"] == "Test"
    assert item["id"]["S"] == test_model.id
    assert item["age"]["N"] == str(test_model.age)
    assert item["has_paid"]["BOOL"] == test_model.has_paid
    assert item["role"]["NULL"] == True
    assert sorted(item["string_set"]["SS"]) == sorted(test_model.string_set)
    assert sorted(item["num_set"]["NS"]) == sorted(map(str, test_model.num_set))
    assert item["test_enum"]["N"] == str(test_model.test_enum.value)
    assert sorted(item["enum_set"]["NS"]) == sorted(
        map(lambda enum: str(enum.value), test_model.enum_set)
    )
    assert item["enum_list"]["L"] == list(
        map(lambda enum: {"N": str(enum.value)}, test_model.enum_list)
    )

    assert len(item["locations_list"]["L"]) == len(test_model.locations_list)
    assert item["locations_list"]["L"][0]["M"]["city"] == {
        "S": test_model.locations_list[0].city
    }
    assert len(item["locations_dict"]["M"]) == len(test_model.locations_dict)


def test_deserialization(test_deserialized_model, test_model, test_mapper):
    """High level test to confirm that a broad range of types are handled and
    deserialized propertly.
    """
    deserialized_model = test_mapper.deserialize_to_model(test_deserialized_model)
    for attribute in test_model.__dict__:
        assert getattr(test_model, attribute) == getattr(deserialized_model, attribute)


def test_deserialize_model_not_set_in_options_class_raises_exception(
    test_deserialized_model, test_mapper
):
    """Test that an exception is raised if the model is not set in the options class."""
    test_mapper._options.model = None
    with pytest.raises(ModelNotSetException):
        test_mapper.deserialize_to_model(test_deserialized_model)

