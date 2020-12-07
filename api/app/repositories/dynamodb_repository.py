"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.clients import dynamodb_client
from app.dynamodb import UpdateExpression, PrimaryKeyPrefix, UpdateAction
from app.models import (
    User, 
    UserEmail,
    Username,
    CommunityMembership, 
    Community
)


class _DynamoDBRepository:
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client):
        self._dynamodb_client = dynamodb_client

    def get_user(self, user_id):
        """Return a user from DynamoDB by id."""
        response = self._dynamodb_client.get_item(User.key(user_id))
        return response

    def add_user(self, user):
        """Add a new user to DynamoDB."""
        user_email = UserEmail(user.id, user.email)
        username = Username(user.id, user.username)
        data = {
            "user_item": user.to_item(),
            "user_email": user_email.to_item(),
            "username": username.to_item()
        }
        response = self._dynamodb_client.create_user(data)
        if "error" in response:
            # should I raise an exception here?
            print("Error!")
        return response

    def get_community(self, community_id):
        """Return a community from DynamoDB by id."""

        response, status = self._dynamodb_client.query(
            PrimaryKeyPrefix.COMMUNITY + community_id,
            PrimaryKeyPrefix.COMMUNITY + community_id,
        )
        if status != 200:
            # This will later be where logging happens
            print(f"Non-200 status code! {status}")
        if "Items" not in response:
            return (None, None)
        return response, status

    def create_community(self, community):
        """Add a new community to DynamoDB."""
        membership = CommunityMembership(community._founder.id, community.id)
        responses = self._dynamodb_client.batch_create(
            [community.to_item(), membership.to_item()]
        )
        return responses

    def create_community_group_chat(self, group_chat, community_group_chat):
        """Add a new community group chat to DynamoDB."""
        responses = self._dynamodb_client.batch_create(
            [group_chat.to_item(), community_group_chat.to_item()]
        )
        return responses

    def update_user(self, user_id, attributes_to_values):
        """Update a user item in DynamoDB."""
        expression = UpdateExpression(UpdateAction.SET, attributes_to_values)
        response, status = self._dynamodb_client.update_item(
            PrimaryKeyPrefix.USER + user_id, PrimaryKeyPrefix.USER + user_id, expression
        )
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        return response, status

    def delete_user(self, user_id):
        """Delete a user from DynamoDB."""
        response, status = self._dynamodb_client.delete_item(
            PrimaryKeyPrefix.USER + user_id, PrimaryKeyPrefix.USER + user_id
        )
        if status != 200:
            # This will later be turned into a log statement
            print(f"Non-200 status code! {status}")
        return response, status


dynamodb_repository = _DynamoDBRepository(dynamodb_client)

