"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""


import os
import logging
import logging.config
import boto3
from pprint import pprint
from app.dynamodb import UpdateExpression, UpdateAction
from botocore.exceptions import ClientError


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("dynamoDBClient")


class _DynamoDBClient:
    """Class that acts as a wrapper around the boto3 library's
    DynamoDB resource.
    """

    def __init__(self):
        self._dynamodb = boto3.client("dynamodb")
        self._table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME", "ChatAppTable")

    def create_user(self, items):
        """Add a new user item to DynamoDB."""
        logger.info("Adding new user to DynamoDB")
        parameters = self._build_create_user_parameters(items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            
            error_message = "Could not add user"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if (
                    err.response["CancellationReasons"][1]["Code"]
                    == "ConditionalCheckFailed"
                ):
                    error_message = "A user with this email already exists"
                elif (
                    err.response["CancellationReasons"][2]["Code"]
                    == "ConditionalCheckFailed"
                ):
                    error_message = "A user with this username already exists"
            return {"error": error_message}

    def delete_user(self, keys):
        """Delete a user item from DynamoDB."""
        logger.info("Deleting a user from DynamoDB")
        parameters = self._build_delete_user_parameters(keys)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            error_message = "Could not delete user"
            pprint(err.response)
            return {"error": error_message}

    def get_item(self, key):
        """Return a single item from DynamoDB. This method
        will return the item with all of its attributes.
        """
        response = self._dynamodb.get_item(TableName=self._table_name, Key=key,)
        return response

    def query(self, partition_key, sort_key):
        """Return the results of a DynamoDB query on the table."""
        response = self._dynamodb.query(
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("PK").eq(partition_key) & Key("SK").eq(sort_key),
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def put_item(self, user_item):
        """Replace an entire item in the table or create a new item
        if it exists. Returns the response from DynamoDB afterwards
        """
        response = self._dynamodb.put_item(Item=user_item)
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def update_user(self, keys, attributes):
        """Update a user item in the table """
        # Special cases are changing a user's email, or username
        if "email" in attributes or "username" in attributes or "role" in attributes:
            return self._update_with_transaction(keys, attributes)
        return self._update_without_transaction(keys["user"], attributes)

    def _update_with_transaction(self, keys, attributes):
        parameters = self._build_update_user_parameters(keys, attributes)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")

            error_message = "Could not update user"
            return {"error": error_message}
    
    def _update_without_transaction(self, key, attributes):
        expression = UpdateExpression(UpdateAction.SET, attributes)
        response = self._dynamodb.update_item(
            TableName=self._table_name,
            Key=key,
            UpdateExpression=expression.expression,
            ConditionExpression=self._build_condition_expression(
                expression.original_attribute_names
            ),
            ExpressionAttributeNames=expression.attribute_name_placeholders,
            ExpressionAttributeValues=expression.attribute_value_placeholders,
        )
        return response

    def delete_item(self, key):
        """Delete an item from DynamoDB and return the response."""
        response = self._dynamodb.delete_item(
            TableName=self._table_name, Key=key
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def _execute_transact_write(self, parameters):
        """Write the given items into DynamoDB as part of a transaction."""
        response = self._dynamodb.transact_write_items(
            TransactItems=parameters
        )
        return response

    def _build_condition_expression(self, attribute_names):
        """Build an expression for conditionally updating one or more fields."""
        condition_expression = [f"attribute_exists({name})" for name in attribute_names]
        return " AND ".join(condition_expression)
        
    # May move these _build_* methods into another module and make them functions if this
    # module becomes too large
    def _build_create_user_parameters(self, items):
        """Return the parameters necessary to create a user in a transaction."""
        parameters = [
            {
                "Put": {
                    "Item": items[item],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_not_exists(PK)",
                }
            }
            for item in items
        ]
        return parameters

    def _build_update_user_parameters(self, keys, attributes):
        """Return the parameters necessary for updating a user in a transaction."""
        expressions = [
            UpdateExpression(UpdateAction.SET, attributes[key])
            for key in keys
        ]
        parameters = [
            {
                "Update": {
                    "Key": keys[key],
                    "TableName": self._table_name,
                    "UpdateExpression": expressions[key],
                    "ConditionExpression": "attribute_exists(PK)"
                }
            }
            for key in keys
        ]
        if "role" in attributes:
            parameters.append(
                {
                    "ConditionCheck": {
                        "TableName": self._table_name,
                        "Key": key["user"],
                        "ConditionExpression": f'role.name = {attributes["role"]["name"]["S"]}'
                    }
                }
            )
        return parameters  

    def _build_delete_user_parameters(self, keys):
        """Return the parameters necessary for deleting a user in a transaction."""
        parameters = [
            {
                "Delete": {
                    "Key": keys[key],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK)"
                }
            }
            for key in keys
        ]
        return parameters

    


dynamodb_client = _DynamoDBClient()
