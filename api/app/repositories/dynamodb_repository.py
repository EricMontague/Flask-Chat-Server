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
        response, status = self._dynamodb_client.query(
            KeyPrefix.USER + user_id, KeyPrefix.USER + user_id 
        )
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        if "Items" not in response:
            return (None, None)
        return response, status

    def create_user(self, user):
        """Add a user to DynamoDB."""
        response, status = self._dynamodb_client.put_item(user.to_dynamo())
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        return response, status

    def update_user(self, user):
        """Update a user item in DynamoDB."""
        expression = UpdateExpression(
            "SET #loc.#cit = :city, #loc.#sta = :state, #loc.#cou = :country",
            {"#loc": "location", "#city": "city", "#sta": "state", "#cou": "country"},
            {":city": city, ":state": state, ":country": country}
        )
        response, status = self._dynamodb_client.update_item(
            KeyPrefix.USER + user.id, KeyPrefix.USER + user.id, expression
        )
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        return response, status

    def delete_user(self, user_id):
        """Delete a user from DynamoDB."""
        response, status = self._dynamodb_client.delete_item(
            KeyPrefix.USER + user_id, KeyPrefix.USER + user_id
        )
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        return response, status


dynamodb_repository = _DynamoDBRepository(dynamodb_client)

