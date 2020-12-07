"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""


import os
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr, And
from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _DynamoDBClient:
    """Class that acts as a wrapper around the boto3 library's
    DynamoDB resource.
    """

    def __init__(self):
        self._dynamodb = boto3.client("dynamodb")
        self._table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME", "ChatAppTable")

    def create_user(self, data):
        """Add a new user item to DynamoDB."""
        parameters = self._build_create_user_parameters(data)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logging.error(f"{err.response['Error']['Code']}")
            logging.error(f"{err.response['Error']['Message']}")

            error_message = "Could not add user"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if err.response["CancellationReasons"][1]["Code"] == "ConditionalCheckFailed":
                    error_message = "A user with this email already exists"
                elif err.response["CancellationReasons"][2]["Code"] == "ConditionalCheckFailed":
                    error_message = "A user with this username already exists"
            return {"error": error_message}
    
    def _build_create_user_parameters(self, data):
        """Return the parameters necessary to create a user in DynamoDB."""
        parameters = {
            "transact_items": [
                {
                    "Put": {
                        "Item": data["user_item"],
                        "TableName": self._table_name,
                        "ConditionExpression": "attribute_not_exists(PK)"
                    }
                },
                {
                    "Put": {
                        "Item": data["user_email"],
                        "TableName": self._table_name,
                        "ConditionExpression": "attribute_not_exists(email)"
                    }
                },
                {
                    "Put": {
                        "Item": data["username"],
                        "TableName": self._table_name,
                        "ConditionExpression": "attribute_not_exists(username)"
                    }
                }
            ]
        }
        return parameters

    def get_item(self, primary_key):
        """Return a single item from DynamoDB. This method
        will return the item with all of its attributes.
        """
        response = self._dynamodb.get_item(
            TableName=self._table_name,
            Key=primary_key,
        )
        return response

    def _execute_transact_write(self, parameters):
        """Write the given items into DynamoDB as part of a transaction."""
        response = self._dynamodb.transact_write_items(
            TransactItems=parameters["transact_items"]
        )
        return response

    def query(self, partition_key, sort_key):
        """Return the results of a DynamoDB query to the users table."""
        response = self._dynamodb.query(
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("PK").eq(partition_key) & Key("SK").eq(sort_key),
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def put_item(self, user_item):
        """Replace an entire item in the users table or create a new item
        if it exists. Returns the response from DynamoDB afterwards
        """
        response = self._dynamodb.put_item(Item=user_item)
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def update_item(self, partition_key, sort_key, expression):
        """Update an item in the users table and return the response."""
        response = self._dynamodb.update_item(
            Key={"PK": partition_key, "SK": sort_key},
            UpdateExpression=expression.expression,
            ConditionExpression=self._build_condition_expression(
                expression.original_attribute_names
            ),
            ExpressionAttributeNames=expression.attribute_name_placeholders,
            ExpressionAttributeValues=expression.attribute_value_placeholders,
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def _build_condition_expression(self, attribute_names):
        """Build an expression for conditionally updating one or more fields."""
        if len(attribute_names) > 1:
            condition_expression = [Attr(name).exists() for name in attribute_names]
            return And(*condition_expression)
        # When updating a single attribute, the AND condition can't be used, else boto3 throws
        # an error, so single attribute updates need to be handled differently

        return Attr(attribute_names[0]).exists()

    def delete_item(self, primary_key):
        """Delete an item from DynamoDB and return the response."""
        response = self._dynamodb.delete_item(
            TableName=self._table_name,
            Key=primary_key
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]


dynamodb_client = _DynamoDBClient()
