"""This module contains functions and classes for mapping application
models to DynamoDB items.
"""


from enum import Enum
from abc import ABC, abstractmethod
from app.models import User


def create_user_from_item(user_item):
    """Create and return a user model from a DynamoDB item."""
    pass


class UpdateAction(Enum):
    """Enum to represent actions for update expressions in DynamoDB."""

    SET = 0
    ADD = 1
    DELETE = 2
    REMOVE = 3


class UpdateExpression:
    """Class to represent an update expression for DynamoDB."""

    def __init__(self, action, attributes_to_values):
        self._build_expression(action, attributes_to_values)

    def _build_expression(self, action, attributes_to_values):
        """Build an update expression for DynamoDB."""
        expression = []
        self.original_attribute_names = []
        self.attribute_name_placeholders = {}
        self.attribute_value_placeholders = {}
        for attribute_name in attributes_to_values:
            attribute_name_lower = attribute_name.lower()
            self.original_attribute_names.append(attribute_name_lower)

             # handle nested attributes
            nested_attributes = attribute_name_lower.split(".") 
            name_alias = ".#".join(nested_attributes)
            expression.append(
                f"#{name_alias} = :{attribute_name_lower.replace('.', '')}"
            )

            # Map aliases for nested attibutes to actual attributes
            for attribute in nested_attributes:
                self.attribute_name_placeholders[f"#{attribute}"] = attribute

            # Map aliases for attribute values
            self.attribute_value_placeholders[
                f":{attribute_name_lower.replace('.', '')}"
            ] = attributes_to_values[attribute_name]
        self.expression = action.name + " " + ", ".join(expression)

    


