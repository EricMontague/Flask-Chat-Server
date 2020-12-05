"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr, And


class _DynamoDBClient:
    """Class that acts as a wrapper around the boto3 library's
    DynamoDB resource.
    """

    _USERS_TABLE = "Users"

    def __init__(self, endpoint_url=""):
        # Endpoint url used for testing with a local version of DynamoDB
        if endpoint_url:
            self._dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
        else:
            self._dynamodb = boto3.resource("dynamodb")
        self._users_table = self._dynamodb.Table(self._USERS_TABLE)

    def query(self, partition_key, sort_key):
        """Return the results of a DynamoDB query to the users table."""
        response = self._users_table.query(
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("PartitionKey").eq(partition_key)
            & Key("SortKey").eq(sort_key),
            ReturnConsumedCapacity="INDEXES",
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def put_item(self, user):
        """Replace an entire item in the users table or create a new item
        if it exists. Returns the response from DynamoDB afterwards
        """
        response = self._users_table.put_item(Item=user)
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def update_item(self, partition_key, sort_key, expression):
        """Update an item in the users table and return the response."""
        response = self._users_table.update_item(
            Key={"PartitionKey": partition_key, "SortKey": sort_key},
            ReturnConsumedCapacity="INDEXES",
            ReturnItemCollectionMetrics="SIZE",
            UpdateExpression=expression.expression,
            ConditionExpression=self._build_condition_expression(expression.original_attribute_names),
            ExpressionAttributeNames=expression.attribute_name_placeholders,
            ExpressionAttributeValues=expression.attribute_value_placeholders,
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def _build_condition_expression(self, attribute_names):
        """Build an expression for conditionally updating one or more fields."""
        if len(attribute_names) > 1:
            condition_expression = [
                Attr(name).exists()
                for name in attribute_names
            ]
            return And(*condition_expression)
        # When updating a single attribute, the AND condition can't be used, else boto3 throws
        # an error, so single attribute updates need to be handled differently

        return Attr(attribute_names[0]).exists()
            
    def delete_item(self, partition_key, sort_key):
        """Delete an item from DynamoDB and return the response."""
        response = self._users_table.delete_item(
            Key={"PartitionKey": partition_key, "SortKey": sort_key},
            ReturnConsumedCapacity="INDEXES",
            ReturnItemCollectionMetrics="SIZE",
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]


dynamodb_client = _DynamoDBClient()
