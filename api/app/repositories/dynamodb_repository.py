"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.clients import dynamodb_client
from app.dynamodb import UpdateExpression, KeyPrefix
from app.models import User




class _DynamoDBRepository:
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client):
        self._dynamodb_client = dynamodb_client

    def get_user_by_id(self, user_id):
        """Return a user from DynamoDB by id."""
        response, status = self._dynamodb_client.get_user(
            KeyPrefix.USER + user_id
        )
        if "Item" not in response:
            return None
        return response

dynamodb_repository = _DynamoDBRepository(dynamodb_client)

