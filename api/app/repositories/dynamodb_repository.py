"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.clients import dynamodb_client
from app.models import User, UserEmail, Username, CommunityMembership, Community
from app.dynamodb.mappings import create_user_from_item


class _DynamoDBRepository:
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
            # should I raise an exception here?
            print("Error!")
        return response

    def update_user(self, user, attributes_to_update):
        """Update a user item in DynamoDB."""
        keys, attributes = self._build_user_attributes_and_keys(
            user, attributes_to_update
        )
        response = self._dynamodb_client.update_user(keys, attributes)
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

    def _build_user_attributes_and_keys(self, user, attributes_to_update):
        """Create and return the dictionaries of user attributes to update
        as well as the keys of the items to update in DynamoDB.
        """
        filtered_attributes = self._filter_attributes(
            user.to_item(), attributes_to_update
        )
        final_attributes = {}
        keys = {"user": User.key(user.id)}
        if "email" in filtered_attributes:
            keys["user_email"] = UserEmail.key(user.email)
            final_attributes["user_meail"] = filtered_attributes.pop("email")
        if "username" in filtered_attributes:
            keys["username"] = Username.key(user.username)
            final_attributes["username"] = filtered_attributes.pop("username")
        final_attributes["user"] = filtered_attributes
        return keys, final_attributes

    def _filter_attributes(self, item, attributes):
        """Return a dictionary containing a subset of the
        attributes of the given DynamoDB item.
        """
        filtered_attributes = {attribute: item[attribute] for attribute in attributes}
        return filtered_attributes


dynamodb_repository = _DynamoDBRepository(dynamodb_client)

