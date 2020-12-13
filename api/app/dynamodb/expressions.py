"""This module contains classes and functions that abstract away
the creation of various 'Expressions' for making calls to DynamoDB.
"""


from enum import Enum


class UpdateAction(Enum):
    """Enum to represent actions for update expressions in DynamoDB."""

    SET = 1
    ADD = 2
    DELETE = 3
    REMOVE = 4


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

    def __str__(self):
        """Return a string representation of an expression."""
        return self.expression

