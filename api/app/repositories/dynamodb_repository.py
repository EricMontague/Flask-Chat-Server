"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.repositories.abstract_repository import AbstractDatabaseRepository
from app.repositories.exceptions import UniqueConstraintException
from app.clients import dynamodb_client
from app.models import User, UserEmail, Username, CommunityMembership, Community
from app.models.update_models import update_user_model
from app.dynamodb import UserMapper, UsernameMapper, UserEmailMapper
from app.dynamodb.constants import PrimaryKeyPrefix
from app.repositories.utils import encode_cursor, decode_cursor


class _DynamoDBRepository(AbstractDatabaseRepository):
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client, **kwargs):
        self._dynamodb_client = dynamodb_client
        self._user_mapper = kwargs["user_mapper"]
        self._username_mapper = kwargs["username_mapper"]
        self._user_email_mapper = kwargs["user_email_mapper"]

    def get_user(self, user_id):
        """Return a user from DynamoDB by id."""
        user_item = self._dynamodb_client.get_item(self._user_mapper.key(user_id, user_id))
        if not user_item:
            return None
        return self._user_mapper.deserialize_to_model(user_item, ["_password_hash"])

    def add_user(self, user):
        """Add a new user to DynamoDB."""
        user_email = UserEmail(user.id, user.email)
        username = Username(user.id, user.username)
        items = {
            "user": self._user_mapper.serialize_from_model(
                user, additional_attributes={"USERS_GSI_SK": user.username}
            ),
            "user_email": self._user_email_mapper.serialize_from_model(user_email),
            "username": self._username_mapper.serialize_from_model(username)
        }
        response = self._dynamodb_client.create_user(items)
        if "error" in response:
            raise UniqueConstraintException(response["error"])

    def update_user(self, old_user, updated_user_data):
        """Update a user item in DynamoDB."""
        updated_user = update_user_model(old_user, updated_user_data)
        items = {"user":self._user_mapper.serialize_from_model(
            updated_user, additional_attributes={"USERS_GSI_SK": updated_user.username})
        }

        if old_user.email != updated_user.email:
            items["updated_user_email"] = self._user_email_mapper.serialize_from_model(
                UserEmail(updated_user.id, updated_user.email)
            )
            items["old_user_email_key"] = self._user_mapper.key(old_user.email, old_user.email)
        if old_user.username != updated_user.username:
            items["updated_username"] = self._username_mapper.serialize_from_model(
                Username(updated_user.id, updated_user.username)
            )
            items["old_username_key"] = self._username_mapper.key(old_user.username, old_user.username)
        response = self._dynamodb_client.update_user(items)
        return response

    def remove_user(self, user):
        """Delete a user item from DynamoDB."""
        keys = {
            "user": self._user_mapper.key(user.id, user.id),
            "username": self._username_mapper.key(user.username, user.username),
            "user_email": self._user_email_mapper.key(user.email, user.email),
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
        users = [
            self._user_mapper.deserialize_to_model(item, ["_password_hash"]) 
            for item in results["Items"]
        ]
        response = {
            "models": users,
            "next": next_cursor,
            "has_next": results["LastEvaluatedKey"] is not None,
            "total": len(users),
        }
        return response


dynamodb_repository = _DynamoDBRepository(
    dynamodb_client, 
    user_mapper=UserMapper(),
    username_mapper=UsernameMapper(),
    user_email_mapper=UserEmailMapper()
)

