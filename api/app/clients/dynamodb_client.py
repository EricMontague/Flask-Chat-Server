"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""


import os
import logging
import logging.config
import boto3
from enum import Enum
from config import PROJECT_ROOT_DIRECTORY
from pprint import pprint
from botocore.exceptions import ClientError


logging.config.fileConfig(PROJECT_ROOT_DIRECTORY + "/logging.conf")
logger = logging.getLogger("dynamoDBClient")



class ErrorType(Enum):
    """Class to represent types of errors."""
    NOT_FOUND = 0
    UNIQUE_CONSTRAINT = 1
    OTHER = 2


class _DynamoDBClient:
    """Class that acts as a wrapper around the boto3 library's
    DynamoDB resource.
    """

    def __init__(self, region, endpoint_url=None):
        self._dynamodb = boto3.client("dynamodb", region, endpoint_url=endpoint_url)
        self._table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME")

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

    def add_community_member(self, keys, item):
        """Add a community membership item to DynamoDB."""
        parameters = self._build_add_community_member_parameters(keys, item)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            error_message = "Could not add user to community"
            error_type = ErrorType.OTHER
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if err.response["CancellationReasons"][0]["Code"] == "ConditionalCheckFailed":
                    error_message = "User could not be found"
                    error_type = ErrorType.NOT_FOUND
                elif err.response["CancellationReasons"][1]["Code"] == "ConditionalCheckFailed":
                    error_message = "Community could not be found"
                    error_type = ErrorType.NOT_FOUND
                elif err.response["CancellationReasons"][2]["Code"] == "ConditionalCheckFailed":
                    error_message = "User is already a member of this community"
                    error_type = ErrorType.UNIQUE_CONSTRAINT
            return {"error": error_message, "error_type": error_type}

    def remove_community_member(self, key):
        """Delete a community membership item from DynamoDB."""
        try:
            return self.delete_item(key)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            
            error_message = "Could not remove member from community"
            if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
                error_message = "Community or user not found"
            return {"error": error_message}

    def create_private_chat(self, items):
        """Add private chat and private chat member items to DynamoDB"""
        logger.info("Adding new private chat to DynamoDB")
        parameters = self._build_create_item_parameters(items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")

            error_message = "Could not create private chat"
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if (
                    err.response["CancellationReasons"][0]["Code"]
                    == "ConditionalCheckFailed"
                ):
                    error_message = "Users already have a private chat together"
            
            return {"error": error_message}
    
    def create_group_chat(self, keys, items):
        """Add group chat, group chat member, and community group chat items
        to DynamoDB.
        """
        logger.info("Adding new group chat to DynamoDB")
        parameters = self._build_create_group_chat_parameters(keys, items)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            error_message = "Could not create group chat"
            error_type = ErrorType.OTHER
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if err.response["CancellationReasons"][2]["Code"] == "ConditionalCheckFailed":
                    error_message = "User is not a member of the community"
            return {"error": error_message, "error_type": error_type}

    def add_group_chat_member(self, keys, item):
        """Add a group chat member item to DynamoDB."""
        parameters = self._build_add_group_chat_member_parameters(keys, item)
        try:
            return self._execute_transact_write(parameters)
        except ClientError as err:
            logger.error(f"{err.response['Error']['Code']}")
            logger.error(f"{err.response['Error']['Message']}")
            

            error_message = "Could not add user to group chat"
            error_type = ErrorType.OTHER
            if err.response["Error"]["Code"] == "TransactionCanceledException":
                if err.response["CancellationReasons"][0]["Code"] == "ConditionalCheckFailed":
                    error_message = "User could not be found"
                    error_type = ErrorType.NOT_FOUND
                elif err.response["CancellationReasons"][1]["Code"] == "ConditionalCheckFailed":
                    error_message = "Group chat could not be found"
                    error_type = ErrorType.NOT_FOUND
                elif err.response["CancellationReasons"][2]["Code"] == "ConditionalCheckFailed":
                    error_message = "User is not a member of the community this group chat is in"
                    error_type = ErrorType.NOT_FOUND
                elif err.response["CancellationReasons"][3]["Code"] == "ConditionalCheckFailed":
                    error_message = "User is already a member of this group chat"
                    error_type = ErrorType.UNIQUE_CONSTRAINT
            return {"error": error_message, "error_type": error_type}

    def batch_delete_items(self, keys):
        dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ.get("AWS_DYNAMODB_ENDPOINT_URL"))
        table = dynamodb.Table(self._table_name)
        with table.batch_writer() as batch:
            for key in keys:
                batch.delete_item(Key=key)
        return True

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

    def put_item(self, item, use_condition_expression=False):
        """Replace an entire item in the table or create a new item
        if it exists. Returns the response from DynamoDB afterwards
        """
        if use_condition_expression:
            try:
                response = self._dynamodb.put_item(
                    TableName=self._table_name,
                    Item=item,
                    ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)"
                )
            except ClientError as err:
                logger.error(f"{err.response['Error']['Code']}")
                logger.error(f"{err.response['Error']['Message']}")
                return False
        else:
            response = self._dynamodb.put_item(
                TableName=self._table_name,
                Item=item
            )
        return True
        
    def delete_item(self, key):
        """Delete an item from DynamoDB and return the response."""
        try:
            response = self._dynamodb.delete_item(
                TableName=self._table_name,
                Key=key,
                ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except ClientError as err:
            return False
        return True

    def query(self, limit, start_key, primary_key, **kwargs):
        logger.info("Querying items from DynamoDB")
        results = {"Items": [], "LastEvaluatedKey": None}
        if kwargs.get("index") is not None:
            response = self._query_index(limit, start_key, primary_key, **kwargs)
        else:
            response = self._query_table(limit, start_key, primary_key, **kwargs)

        results["Items"].extend(response["Items"])
        results["LastEvaluatedKey"] = response.get("LastEvaluatedKey")
        return results

    def _query_index(self, limit, start_key, primary_key, **kwargs):
        key_condition_expression = f"{primary_key['pk_name']} = :pk"
        expression_attribute_values = {":pk": primary_key["pk_value"]}
        if "sk_name" in primary_key:
            key_condition_expression += (
                f" AND begins_with({primary_key['sk_name']}, :sk)"
            )
            expression_attribute_values[":sk"] = primary_key["sk_value"]
        if start_key:
            response = self._dynamodb.query(
                TableName=self._table_name,
                IndexName=kwargs["index"],
                Limit=limit,
                ExclusiveStartKey=start_key,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=kwargs.get("scan_forward", True)
            )
        else:
            response = self._dynamodb.query(
                TableName=self._table_name,
                IndexName=kwargs["index"],
                Limit=limit,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=kwargs.get("scan_forward", True)
            )
        return response

    def _query_table(self, limit, start_key, primary_key, **kwargs):
        key_condition_expression = f"{primary_key['pk_name']} = :pk"
        expression_attribute_values = {":pk": primary_key["pk_value"]}
        if "sk_name" in primary_key:
            key_condition_expression += (
                f" AND begins_with({primary_key['sk_name']}, :sk)"
            )
            expression_attribute_values[":sk"] = primary_key["sk_value"]
        if start_key:
            response = self._dynamodb.query(
                TableName=self._table_name,
                Limit=limit,
                ExclusiveStartKey=start_key,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=kwargs.get("scan_forward", True)
            )
        else:
            response = self._dynamodb.query(
                TableName=self._table_name,
                Limit=limit,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=kwargs.get("scan_forward", True)
            )
        return response

    def batch_get_items(self, keys):
        """Return multiple items from DynamoDB."""
        logger.info("Making batch get call")
        return self._dynamodb.batch_get_item(
            RequestItems={
                self._table_name: {
                    "Keys": keys
                }
            }
        )

    def batch_write_items(self, requests):
        """Write multiple items at a time to the table."""
        logger.info("Executing batch write request")
        batch_request = self._build_batch_write_request(requests)
        try:
            response = self._dynamodb.batch_write_item(
                RequestItems={self._table_name: batch_request}
            )
        except ClientError as err:
            logger.error(err.response["Error"]["Code"])
            logger.error(err.response["Error"]["Message"])
            
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
                    "Item": items[key],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_not_exists(PK)",
                }
            }
            for key in items
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

    def _build_add_community_member_parameters(self, keys, item):
        parameters = [
            {
                "ConditionCheck": {
                    "Key": keys["user_key"],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
                }
            },
            {
                "ConditionCheck": {
                    "Key": keys["community_key"],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
                }
            },
            {
                "Put": {
                    "Item": item, "TableName": self._table_name,
                    "ConditionExpression": "attribute_not_exists(PK) AND attribute_not_exists(SK)"
                }
            },
        ]
        return parameters
    
    def _build_add_group_chat_member_parameters(self, keys, item):
        parameters = [
            {
                "ConditionCheck": {
                    "Key": keys["user_key"],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
                }
            },
            {
                "ConditionCheck": {
                    "Key": keys["group_chat_key"],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
                }
            },
            {
                "ConditionCheck": {
                    "Key": keys["community_membership_key"],
                    "TableName": self._table_name,
                    "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
                }
            },
            {
                "Put": {
                    "Item": item, "TableName": self._table_name,
                    "ConditionExpression": "attribute_not_exists(PK) AND attribute_not_exists(SK)"
                }
            },
        ]
        return parameters

    def _build_create_group_chat_parameters(self, keys, items):
        parameters = self._build_create_item_parameters(items)
        parameters.append({
            "ConditionCheck": {
                "Key": keys["community_membership_key"],
                "TableName": self._table_name,
                "ConditionExpression": "attribute_exists(PK) AND attribute_exists(SK)",
            }
        })
        return parameters


dynamodb_client = _DynamoDBClient(
    os.environ.get("AWS_DEFAULT_REGION"),
    endpoint_url=os.environ.get("AWS_DYNAMODB_ENDPOINT_URL")
)
