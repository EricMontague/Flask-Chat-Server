"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.repositories.abstract_repository import AbstractDatabaseRepository
from app.repositories.exceptions import UniqueConstraintException
from app.clients import dynamodb_client
from app.models import User, UserEmail, Username, CommunityMembership, Community
from app.models.update_models import update_user_model
from app.dynamodb.mapper import create_user_from_item
from app.dynamodb.constants import PrimaryKeyPrefix
from app.repositories.utils import encode_cursor, decode_cursor


class _DynamoDBRepository(AbstractDatabaseRepository):
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client):
        self._dynamodb_client = dynamodb_client

    def get_user(self, user_id):
        """Return a user from DynamoDB by id."""
        user_item = self._dynamodb_client.get_item(User.key(user_id))
        if not user_item:
            return None
        return create_user_from_item(user_item)

    def add_user(self, user):
        """Add a new user to DynamoDB."""
        user_email = UserEmail(user.id, user.email)
        username = Username(user.id, user.username)
        items = {
            "user": user.to_item(),
            "user_email": user_email.to_item(),
            "username": username.to_item(),
        }
        response = self._dynamodb_client.create_user(items)
        if "error" in response:
            raise UniqueConstraintException(response["error"])

    def update_user(self, old_user, updated_user_data):
        """Update a user item in DynamoDB."""
        updated_user = update_user_model(old_user, updated_user_data)
        items = {"user": updated_user.to_item()}

        if old_user.email != updated_user.email:
            items["updated_user_email"] = UserEmail(
                updated_user.id, updated_user.email
            ).to_item()
            items["old_user_email_key"] = UserEmail.key(old_user.email)
        if old_user.username != updated_user.username:
            items["upated_username"] = Username(
                updated_user.id, updated_user.username
            ).to_item()
            items["old_username_key"] = Username.key(old_user.username)
        response = self._dynamodb_client.update_user(items)
        return response

    def remove_user(self, user):
        """Delete a user item from DynamoDB."""
        keys = {
            "user": User.key(user.id),
            "username": Username.key(user.username),
            "user_email": UserEmail.key(user.email),
        }
        response = self._dynamodb_client.delete_user(keys)
        return response

    def get_users(self, limit, encoded_start_key=None):
        """Return a list of user models."""
        decoded_start_key = {}
        if encoded_start_key:
            decoded_start_key = decode_cursor(encoded_start_key)
        results = self._dynamodb_client.get_items(
            limit, decoded_start_key, "UsersIndex"
        )
        next_cursor = encode_cursor(results["LastEvaluatedKey"] or {})
        users = [create_user_from_item(item) for item in results["Items"]]
        response = {
            "models": users,
            "next": next_cursor,
            "has_next": results["LastEvaluatedKey"] is not None,
            "total": len(users)
        }
        return response


dynamodb_repository = _DynamoDBRepository(dynamodb_client)

