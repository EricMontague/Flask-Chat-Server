"""This file contains fixtures for running integration tests on all
code that interacts with DynamoDB.
"""


import pytest
from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.common_mappers import LocationMapper
from app.models import Location
from enum import Enum


class TestEnum(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3


class TestModel:
    """Class to be used in serialization and deserialization tests."""

    def __init__(
        self,
        id,
        age,
        has_paid,
        role,
        string_set,
        num_set,
        test_enum,
        enum_set,
        enum_list,
        locations_list,
        locations_dict,
    ):
        self.id = id
        self.age = age
        self.has_paid = has_paid
        self.role = role
        self.string_set = string_set
        self.num_set = num_set
        self.test_enum = test_enum
        self.enum_set = enum_set
        self.enum_list = enum_list
        self.locations_list = locations_list
        self.locations_dict = locations_dict


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

    ENUMS = {"test_enum": TestEnum, "enum_set": TestEnum, "enum_list": TestEnum}
    NESTED_MAPPERS = {
        "locations_list": LocationMapper(ignore_partition_key=True),
        "locations_dict": LocationMapper(ignore_partition_key=True),
    }


deserialized_test_model = {
    "PK": {"S": "TESTMODEL#wqtoqin"},
    "SK": {"S": "TESTMODEL#wqtoqin"},
    "age": {"N": "25"},
    "enum_list": {"L": [{"N": "1"}, {"N": "3"}]},
    "enum_set": {"NS": ["2", "3"]},
    "has_paid": {"BOOL": True},
    "id": {"S": "wqtoqin"},
    "locations_dict": {
        "M": {
            "New York": {
                "M": {
                    "city": {"S": "New York"},
                    "country": {"S": "US"},
                    "state": {"S": "New York"},
                }
            },
            "Philadelphia": {
                "M": {
                    "city": {"S": "Philadelphia"},
                    "country": {"S": "US"},
                    "state": {"S": "PA"},
                }
            },
        }
    },
    "locations_list": {
        "L": [
            {
                "M": {
                    "city": {"S": "New York"},
                    "country": {"S": "US"},
                    "state": {"S": "New York"},
                }
            },
            {
                "M": {
                    "city": {"S": "Philadelphia"},
                    "country": {"S": "US"},
                    "state": {"S": "PA"},
                }
            },
        ]
    },
    "num_set": {"NS": ["2", "3", "4", "5"]},
    "role": {"NULL": True},
    "string_set": {"SS": ["A", "B", "C"]},
    "test_enum": {"N": "1"},
    "type": {"S": "Test"},
}


@pytest.fixture
def test_mapper():
    """Return an instance of a TestMapper."""
    return TestMapper()


@pytest.fixture
def test_model():
    """Return an instance of a TesteModel."""
    return TestModel(
        "wqtoqin",
        25,
        True,
        None,
        {"A", "B", "C"},
        {2, 3, 4, 5},
        TestEnum.RED,
        {TestEnum.BLUE, TestEnum.YELLOW},
        [TestEnum.RED, TestEnum.YELLOW],
        [Location("New York", "New York", "US"), Location("Philadelphia", "PA", "US")],
        {
            "New York": Location("New York", "New York", "US"),
            "Philadelphia": Location("Philadelphia", "PA", "US"),
        },
    )


@pytest.fixture
def test_key_prefix():
    """Return the prefix for a test partition or sort key."""
    return "TESTMODEL#"


@pytest.fixture
def test_deserialized_model():
    """Return a deserialized version of the test model."""
    return deserialized_test_model
