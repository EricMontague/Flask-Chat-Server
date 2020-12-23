"""This module contains the DynamoDB repository."""


from http import HTTPStatus
from app.repositories.abstract_repository import AbstractDatabaseRepository
from app.repositories.exceptions import UniqueConstraintException
from app.clients import dynamodb_client
from app.models import UserEmail, Username, CommunityMembership, CommunityName
from app.models.update_models import update_user_model
from app.dynamodb import (
    UserMapper, 
    UsernameMapper, 
    UserEmailMapper,
    CommunityMapper, 
    CommunityMembershipMapper, 
    CommunityNameMapper
)
from app.dynamodb.constants import PrimaryKeyPrefix
from app.repositories.utils import encode_cursor, decode_cursor


class _DynamoDBRepository(AbstractDatabaseRepository):
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client, **kwargs):
        self._dynamodb_client = dynamodb_client
        self._user_mapper = kwargs.get("user_mapper")
        self._username_mapper = kwargs.get("username_mapper")
        self._user_email_mapper = kwargs.get("user_email_mapper")
        self._community_mapper = kwargs.get("community_mapper")
        self._community_name_mapper = kwargs.get("community_name_mapper")
        self._community_membership_mapper = kwargs.get("community_membership_mapper")

    def get_user(self, user_id):
        """Return a user from DynamoDB by id."""
        primary_key = self._user_mapper.key(user_id, user_id)
        user_item = self._dynamodb_client.get_item(primary_key)
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
            "username": self._username_mapper.serialize_from_model(username),
        }
        response = self._dynamodb_client.create_user(items)
        if "error" in response:
            raise UniqueConstraintException(response["error"])

    def update_user(self, old_user, updated_user_data):
        """Update a user item in DynamoDB."""
        updated_user = update_user_model(old_user, updated_user_data)
        items = {
            "user": self._user_mapper.serialize_from_model(
                updated_user,
                additional_attributes={"USERS_GSI_SK": updated_user.username},
            )
        }

        if old_user.email != updated_user.email:
            items["updated_user_email"] = self._user_email_mapper.serialize_from_model(
                UserEmail(updated_user.id, updated_user.email)
            )
            items["old_user_email_key"] = self._user_mapper.key(
                old_user.email, old_user.email
            )
        if old_user.username != updated_user.username:
            items["updated_username"] = self._username_mapper.serialize_from_model(
                Username(updated_user.id, updated_user.username)
            )
            items["old_username_key"] = self._username_mapper.key(
                old_user.username, old_user.username
            )
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

    def get_community(self, community_id):
        """Return a community from DynamoDB by id."""
        primary_key = self._community_mapper.key(community_id, community_id)
        community_item = self._dynamodb_client.get_item(primary_key)
        if not community_item:
            return None
        return self._community_mapper.deserialize_to_model(community_item)

    def add_community(self, community, founder_id):
        """Add a new community to DynamoDB."""
        community_name = CommunityName(community.id, community.name)
        community_membership = CommunityMembership(community.id, founder_id)
        additional_attributes={
            "COMMUNITY_BY_TOPIC_GSI_PK": PrimaryKeyPrefix.TOPIC + community.topic.name,
            "COMMUNITY_BY_TOPIC_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community.id,
            "COMMUNITY_BY_LOCATION_GSI_PK": PrimaryKeyPrefix.COUNTRY + community.location.country,
            "COMMUNITY_BY_LOCATION_GSI_SK": (
                PrimaryKeyPrefix.STATE + community.location.state 
                + PrimaryKeyPrefix.CITY + community.location.city
            )
        }
        items = {
            "community": self._community_mapper.serialize_from_model(
                community, additional_attributes=additional_attributes
            ),
            "community_name": self._community_name_mapper.serialize_from_model(community_name),
            "community_membership": self._community_membership_mapper.serialize_from_model(community_membership),
        }
        response = self._dynamodb_client.create_community(items)
        if "error" in response:
            raise UniqueConstraintException(response["error"])
        
    def update_community(self):
        pass

    def remove_community(self):
        pass

    def get_communities(self):
        pass
    

dynamodb_repository = _DynamoDBRepository(
    dynamodb_client,
    user_mapper=UserMapper(),
    username_mapper=UsernameMapper(),
    user_email_mapper=UserEmailMapper(),
    community_mapper=CommunityMapper(),
    community_name_mapper=CommunityNameMapper(),
    community_membership_mapper=CommunityMembershipMapper()
)

