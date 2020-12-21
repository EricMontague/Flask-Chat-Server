"""This file contains fixtures for running integration tests on all
code that interacts with DynamoDB.
"""


import pytest
from app.dynamodb.mapper import ModelMapper
from app.dynamodb.model_mappers import LocationMapper
from app.models import Location
from enum import Enum


class TestEnum(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3


class TestModel:
    """Class to be used in serialization and deserialization tests."""

    def __init__(self):
        self.id = "wqtoqin"
        self.age = 25
        self.has_paid = True
        self.role = None
        self.string_set = {"A", "B", "C"}
        self.num_set = {2, 3, 4, 5}
        self.test_enum = TestEnum.RED
        self.enum_set = {TestEnum.BLUE, TestEnum.YELLOW}
        self.enum_list = [TestEnum.RED, TestEnum.YELLOW]
        self.locations_list = [Location("New York", "New York", "US"), Location("Philadelphia", "PA", "US")]
        self.locations_dict = {
            "New York": Location("New York", "New York", "US"),
            "Philadelphia": Location("Philadelphia", "PA", "US")
        }



class TestMapper(ModelMapper):
    """Class to be used to run tests serializing and deserializing a 
    variety of different types of attributes that could be present on a model.
    """
    
    class Meta:
        model = TestModel
        fields = (
            "id", 
            "age", 
            "has_paid", 
            "role", 
            "string_set", 
            "num_set",
            "test_enum",
            "enum_set",
            "enum_list",
            "locations_list",
            "locations_dict",
        )
        partition_key_attribute = "id"
        sort_key_attribute = "id"
        type_ = "Test"
        enum_attribute = "value"

    ENUMS = {"test_enum": TestEnum}
    NESTED_MAPPERS = {
        "locations_list": LocationMapper(ignore_partition_key=True),
        "locations_dict": LocationMapper(ignore_partition_key=True)
    }


@pytest.fixture
def test_mapper():
    """Return an instance of a TestMapper."""
    return TestMapper()


@pytest.fixture
def test_model():
    """Return an instance of a TesteModel."""
    return TestModel()


@pytest.fixture
def test_key_prefix():
    """Return the prefix for a test partition or sort key."""
    return "TESTMODEL#"