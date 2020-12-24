"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""


import os
import logging
import logging.config
import boto3
from config import PROJECT_ROOT_DIRECTORY
from pathlib import Path
from pprint import pprint
from app.dynamodb.expressions import UpdateExpression, UpdateAction
from botocore.exceptions import ClientError


logging.config.fileConfig(PROJECT_ROOT_DIRECTORY + "/logging.conf")
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
        parameters = self._build_create_item_parameters(items)
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

    def update_user(self, items):
        """Update a user in the table """
        logger.info("Updating user in DynamoDB")
        parameters = self._build_update_user_parameters(items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            error_message = "Could not update user information"
            return {"error": error_message}

    def delete_user(self, keys):
        """Delete a user item from DynamoDB."""
        logger.info("Deleting a user from DynamoDB")
        parameters = self._build_delete_item_parameters(keys)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")

            error_message = "Could not delete user"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if any(
                    reason["Code"] for reason in err.response["CancellationReasons"]
                ):
                    error_message = "User could not be found"
            return {"error": error_message}

    def create_community(self, items):
        """Add a new community to DynamoDB."""
        logger.info("Adding new community to DynamoDB")
        parameters = self._build_create_item_parameters(items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")

            error_message = "Could not add community"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if (
                    err.response["CancellationReasons"][1]["Code"]
                    == "ConditionalCheckFailed"
                ):
                    error_message = "A community with this name already exists"
            return {"error": error_message}

    def update_community(self, items):
        """Update a community item in DynamoDB."""
        logger.info("Updating a community in DynamoDB")
        parameters = self._build_update_commmunity_parameters(items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            error_message = "Could not update community information"
            return {"error": error_message}

    def delete_community(self, keys):
        """Delete a community from DynamoDB."""
        logger.info("Deleting a community from DynamoDB")
        parameters = self._build_delete_item_parameters(keys)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")

            error_message = "Could not delete community"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if any(
                    reason["Code"] for reason in err.response["CancellationReasons"]
                ):
                    error_message = "Community could not be found"
            return {"error": error_message}

    def get_items(self, limit, start_key, index=None):
        """Return a list of items from the table or an index if given."""
        logger.info("Getting items from DynamoDB")
        results = {"Items": [], "LastEvaluatedKey": None}
        if index:
            response = self._scan_index(limit, start_key, index)
        else:
            response = self._scan_table(limit, start_key)

        results["Items"].extend(response["Items"])
        results["LastEvaluatedKey"] = response.get("LastEvaluatedKey")
        return results

    def get_item(self, key):
        """Return a single item from DynamoDB. This method
        will return the item with all of its attributes.
        """
        response = self._dynamodb.get_item(TableName=self._table_name, Key=key,)
        return response.get("Item")

    def put_item(self, user_item):
        """Replace an entire item in the table or create a new item
        if it exists. Returns the response from DynamoDB afterwards
        """
        response = self._dynamodb.put_item(Item=user_item)
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def delete_item(self, key):
        """Delete an item from DynamoDB and return the response."""
        response = self._dynamodb.delete_item(TableName=self._table_name, Key=key)
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def query(self, limit, start_key, primary_key, index=None):
        logger.info("Querying items from DynamoDB")
        results = {"Items": [], "LastEvaluatedKey": None}
        if index:
            response = self._query_index(limit, start_key, primary_key, index)
        else:
            response = self._query_table(limit, start_key, primary_key)

        results["Items"].extend(response["Items"])
        results["LastEvaluatedKey"] = response.get("LastEvaluatedKey")
        return results

    def _query_index(self, limit, start_key, primary_key, index):
        if start_key:
            response = self._dynamodb.query(
                TableName=self._table_name,
                IndexName=index,
                Limit=limit,
                ExclusiveStartKey=start_key,
                KeyConditionExpression=f"{primary_key['pk_name']} = :pk",
                ExpressionAttributeValues={":pk": primary_key["pk_value"]},
            )
        else:
            response = self._dynamodb.query(
                TableName=self._table_name,
                IndexName=index,
                Limit=limit,
                KeyConditionExpression=f"{primary_key['pk_name']} = :pk",
                ExpressionAttributeValues={":pk": primary_key["pk_value"]},
            )
        return response

    def _query_table(self, limit, start_key, primary_key):
        pass

    def batch_write_items(self, requests):
        """Write multiple items at a time to the table."""
        logger.info("Executing batch write request")
        batch_request = self._build_batch_write_request(requests)
        try:
            response = self._dynamodb.batch_write_item(
                RequestItems={self._table_name: batch_request}
            )
        except ClientError as err:
            # logger.error(err.response["Error"]["Code"])
            # logger.error(err.response["Error"]["Message"])
            pprint(err.response)
            response = {"error": "Batch write was unsuccessful"}
        return response

    def _execute_transact_write(self, parameters):
        """Write the given items into DynamoDB as part of a transaction."""
        response = self._dynamodb.transact_write_items(TransactItems=parameters)
        return response

    def _scan_index(self, limit, start_key, index):
        """Perform a scan on an index and return a list of items."""
        if start_key:
            response = self._dynamodb.scan(
                TableName=self._table_name,
                IndexName=index,
                ExclusiveStartKey=start_key,
                Limit=limit,
            )
        else:
            response = self._dynamodb.scan(
                TableName=self._table_name, IndexName=index, Limit=limit
            )
        return response

    def _scan_table(self, limit, start_key):
        """Perform a scan on the table and return a list of items."""
        if start_key:
            response = self._dynamodb.scan(
                TableName=self._table_name, ExclusiveStartKey=start_key, Limit=limit
            )
        else:
            response = self._dynamodb.scan(TableName=self._table_name, Limit=limit)
        return response

    # May move these _build_* methods into another module and make them functions if this
    # module becomes too large
    def _build_create_item_parameters(self, items):
        """Return the parameters necessary to create an item in a transaction."""
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

    def _build_update_user_parameters(self, items):
        """Return the parameters necessary to update a user in a transaction."""
        parameters = []
        if "old_user_email_key" in items:
            parameters.append(
                {
                    "Delete": {
                        "Key": items.pop("old_user_email_key"),
                        "TableName": self._table_name,
                    }
                }
            )
        if "old_username_key" in items:
            parameters.append(
                {
                    "Delete": {
                        "Key": items.pop("old_username_key"),
                        "TableName": self._table_name,
                    }
                }
            )
        for item in items:
            parameters.append(
                {"Put": {"Item": items[item], "TableName": self._table_name}}
            )
        return parameters

    def _build_update_commmunity_parameters(self, items):
        """Return the parameters necessary to update a community in a transaction."""
        parameters = []
        if "old_community_name_key" in items:
            parameters.append(
                {
                    "Delete": {
                        "Key": items.pop("old_community_name_key"),
                        "TableName": self._table_name,
                    }
                }
            )
        for item in items:
            parameters.append(
                {"Put": {"Item": items[item], "TableName": self._table_name}}
            )
        return parameters

    def _build_delete_item_parameters(self, keys):
        """Return the parameters necessary for deleting an item in a transaction."""
        parameters = [
            {
                "Delete": {
                    "Key": keys[key],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK)",
                }
            }
            for key in keys
        ]
        return parameters

    def _build_batch_write_request(self, requests):
        """Return a list that contains all of the requests to batch writes
        to DynamoDB.
        """
        batch_request = []
        for method, item_or_key in requests:
            if method == "PutRequest":
                batch_request.append({method: {"Item": item_or_key}})
            elif method == "DeleteRequest":
                batch_request.append({method: {"Key": item_or_key}})
        return batch_request


dynamodb_client = _DynamoDBClient()
