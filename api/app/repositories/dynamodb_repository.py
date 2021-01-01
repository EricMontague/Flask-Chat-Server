"""This module contains the DynamoDB repository."""


import os
from uuid import uuid4
from http import HTTPStatus
from pprint import pprint
from app.repositories.abstract_repository import AbstractDatabaseRepository
from app.repositories.exceptions import UniqueConstraintException, NotFoundException
from app.clients import dynamodb_client
from app.models import (
    UserEmail, 
    Username, 
    CommunityMembership, 
    CommunityName, 
    Image, 
    ImageType, 
    PrivateChatMember,
    PrivateChat
)
from app.models.update_models import update_user_model, update_community_model
from app.dynamodb import (
    UserMapper,
    UsernameMapper,
    UserEmailMapper,
    CommunityMapper,
    CommunityMembershipMapper,
    CommunityNameMapper,
    NotificationMapper,
    PrivateChatMemberMapper,
    MessageMapper
)
from app.dynamodb.constants import PrimaryKeyPrefix, ItemType
from app.repositories.utils import encode_cursor, decode_cursor


class _DynamoDBRepository(AbstractDatabaseRepository):
    """Repository class for the DynamoDB backend."""

    def __init__(self, dynamodb_client, **kwargs):
        self._dynamodb_client = dynamodb_client
        self._table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME", "ChatAppTable")
        self._user_mapper = kwargs.get("user_mapper")
        self._username_mapper = kwargs.get("username_mapper")
        self._user_email_mapper = kwargs.get("user_email_mapper")
        self._community_mapper = kwargs.get("community_mapper")
        self._community_name_mapper = kwargs.get("community_name_mapper")
        self._community_membership_mapper = kwargs.get("community_membership_mapper")
        self._notification_mapper = kwargs.get("notification_mapper")
        self._private_chat_member_mapper = kwargs.get("private_chat_member_mapper")
        self._message_mapper = kwargs.get("message_mapper")

    def get_user(self, user_id):
        """Return a user from DynamoDB by id."""
        primary_key = self._user_mapper.key(user_id, user_id)
        user_item = self._dynamodb_client.get_item(primary_key)
        if not user_item:
            return None
        return self._user_mapper.deserialize_to_model(user_item)

    def add_user(self, user):
        """Add a new user to DynamoDB."""
        user_email = UserEmail(user.id, user.email)
        username = Username(user.id, user.username)
        additional_attributes={
            "USERS_GSI_PK": PrimaryKeyPrefix.USER + user.id,
            "USERS_GSI_SK": user.username
        }
        items = {
            "user": self._user_mapper.serialize_from_model(
                user, additional_attributes=additional_attributes
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
        additional_attributes={
            "USERS_GSI_PK": PrimaryKeyPrefix.USER + updated_user.id,
            "USERS_GSI_SK": updated_user.username
        }
        items = {
            "user": self._user_mapper.serialize_from_model(
                updated_user,
                additional_attributes=additional_attributes,
            )
        }

        if old_user.email != updated_user.email:
            items["updated_user_email"] = self._user_email_mapper.serialize_from_model(
                UserEmail(updated_user.id, updated_user.email)
            )
            items["old_user_email_key"] = self._user_email_mapper.key(
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

    def update_user_image(self, user, image_data):
        """Update one of the user's images in DynamoDB."""
        new_image = Image(**image_data)
        if image_data["image_type"] == ImageType.USER_PROFILE_PHOTO:
            user.avatar = new_image
        elif image_data["image_type"] == ImageType.USER_COVER_PHOTO:
            user.cover_photo = new_image
        additional_attributes={
            "USERS_GSI_PK": PrimaryKeyPrefix.USER + user.id,
            "USERS_GSI_SK": user.username
        }
        user_item = self._user_mapper.serialize_from_model(
            user, additional_attributes=additional_attributes,
        )
        
        response = self._dynamodb_client.put_item(user_item)
        return response

    def remove_user(self, user):
        """Delete a user item from DynamoDB."""
        keys = {
            "user": self._user_mapper.key(user.id, user.id),
            "username": self._username_mapper.key(user.username, user.username),
            "user_email": self._user_email_mapper.key(user.email, user.email),
        }
        response = self._dynamodb_client.delete_user(keys)

        # Make use of threading here later so this doesn't block
        user_primary_key = self._user_mapper.key(user.id)
        limit = 25
        cursor = {}
        query_params = [
            limit,
            cursor,
            {
                "pk_name": "USERS_GSI_PK", 
                "pk_value": user_primary_key["PK"], 
                "sk_name": "USERS_GSI_SK",
                "sk_value": {"S":PrimaryKeyPrefix.COMMUNITY},
            }
        ]
        self._delete_community_memberships(query_params, index="UsersIndex")
        return response
    
    def _delete_community_memberships(self, query_params, **kwargs):
        while True:
            query_results = self._dynamodb_client.query(*query_params, **kwargs)
            if not query_results["Items"]:
                break

            # Delete all community membership items
            membership_keys = [
                {
                    "PK": PrimaryKeyPrefix.COMMUNITY + item["community_id"]["S"],
                    "SK": PrimaryKeyPrefix.USER + item["user_id"]["S"]
                }
                for item in query_results["Items"]
            ]

            self._dynamodb_client.batch_delete_items(membership_keys)
            if not query_results["LastEvaluatedKey"]:
                break
         
    def get_users(self, limit, encoded_start_key=None):
        """Return a collection of user models."""
        decoded_start_key = {}
        if encoded_start_key:
            decoded_start_key = decode_cursor(encoded_start_key)
        results = self._dynamodb_client.get_items(
            limit, decoded_start_key, "UsersIndex"
        )
        return self._process_query_or_scan_results(results, self._user_mapper, ItemType.USER.name)          
    
    def get_user_communities(self, user_id, limit, **kwargs):
        """Return a collection of the user's communities."""
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        user = self.get_user(user_id)
        if not user:
            raise NotFoundException("User not found")
        primary_key = self._user_mapper.key(user_id)
        query_results = self._dynamodb_client.query(
            limit,
            cursor,
            {
                "pk_name": "INVERTED_GSI_PK", 
                "pk_value": primary_key["PK"], 
                "sk_name": "INVERTED_GSI_SK",
                "sk_value": {"S":PrimaryKeyPrefix.COMMUNITY},
            },
            index="InvertedIndex"
        )
        
        if not query_results["Items"]:
            response = {
                "models": [],
                "total": 0
            }
        else:
            community_keys = [
                self._community_mapper.key(item["community_id"]["S"], item["community_id"]["S"])
                for item in query_results["Items"]
            ]
            
            batch_results = self._dynamodb_client.batch_get_items(community_keys)
            
            response = self._process_batch_results(
                batch_results, self._community_mapper, ItemType.COMMUNITY.name
            )
        response["has_next"] = query_results["LastEvaluatedKey"] is not None
        response["next"] = encode_cursor(query_results["LastEvaluatedKey"] or {})
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
        membership_additional_attributes={
            "INVERTED_GSI_PK": PrimaryKeyPrefix.USER + founder_id,
            "INVERTED_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community.id
        }
        community_additional_attributes = {
            "COMMUNITIES_BY_TOPIC_GSI_PK": PrimaryKeyPrefix.TOPIC + community.topic.name,
            "COMMUNITIES_BY_TOPIC_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community.id,
            "COMMUNITIES_BY_LOCATION_GSI_PK": PrimaryKeyPrefix.COUNTRY
            + community.location.country,
            "COMMUNITIES_BY_LOCATION_GSI_SK": (
                PrimaryKeyPrefix.STATE
                + community.location.state
                + PrimaryKeyPrefix.CITY
                + community.location.city
            ),
        }
        items = {
            "community": self._community_mapper.serialize_from_model(
                community, additional_attributes=community_additional_attributes
            ),
            "community_name": self._community_name_mapper.serialize_from_model(
                community_name
            ),
            "community_membership": self._community_membership_mapper.serialize_from_model(
                community_membership, additional_attributes=membership_additional_attributes
            ),
        }
        response = self._dynamodb_client.create_community(items)
        if "error" in response:
            raise UniqueConstraintException(response["error"])

    def update_community(self, old_community, updated_community_data):
        """Update a community item in DynamoDB."""
        updated_community = update_community_model(
            old_community, updated_community_data
        )
        additional_attributes = {
            "COMMUNITIES_BY_TOPIC_GSI_PK": PrimaryKeyPrefix.TOPIC
            + updated_community.topic.name,
            "COMMUNITIES_BY_TOPIC_GSI_SK": PrimaryKeyPrefix.COMMUNITY
            + updated_community.id,
            "COMMUNITIES_BY_LOCATION_GSI_PK": PrimaryKeyPrefix.COUNTRY
            + updated_community.location.country,
            "COMMUNITIES_BY_LOCATION_GSI_SK": (
                PrimaryKeyPrefix.STATE
                + updated_community.location.state
                + PrimaryKeyPrefix.CITY
                + updated_community.location.city
            ),
        }
        items = {
            "community": self._community_mapper.serialize_from_model(
                updated_community, additional_attributes=additional_attributes
            )
        }

        if old_community.name != updated_community.name:
            items[
                "updated_community_name"
            ] = self._community_name_mapper.serialize_from_model(
                CommunityName(updated_community.id, updated_community.name)
            )
            items["old_community_name_key"] = self._community_name_mapper.key(
                old_community.name, old_community.name
            )
        response = self._dynamodb_client.update_community(items)
        return response

    def update_community_image(self, community, image_data):
        """Update a community's image data in DynamoDB."""
        new_image = Image(**image_data)
        if image_data["image_type"] == ImageType.COMMUNITY_PROFILE_PHOTO:
            community.avatar = new_image
        elif image_data["image_type"] == ImageType.COMMUNITY_COVER_PHOTO:
            community.cover_photo = new_image
        additional_attributes = {
            "COMMUNITIES_BY_TOPIC_GSI_PK": PrimaryKeyPrefix.TOPIC
            + community.topic.name,
            "COMMUNITIES_BY_TOPIC_GSI_SK": PrimaryKeyPrefix.COMMUNITY
            + community.id,
            "COMMUNITIES_BY_LOCATION_GSI_PK": PrimaryKeyPrefix.COUNTRY
            + community.location.country,
            "COMMUNITIES_BY_LOCATION_GSI_SK": (
                PrimaryKeyPrefix.STATE
                + community.location.state
                + PrimaryKeyPrefix.CITY
                + community.location.city
            ),
        }
        community_item = self._community_mapper.serialize_from_model(
            community, additional_attributes=additional_attributes,
        )
        response = self._dynamodb_client.put_item(community_item)
        return response

    def remove_community(self, community):
        """Delete a community from DynamoDB."""
        keys = {
            "community": self._community_mapper.key(community.id, community.id),
            "community_name": self._community_name_mapper.key(
                community.name, community.name
            ),
        }
        response = self._dynamodb_client.delete_community(keys)
        primary_key = self._community_mapper.key(community.id)
        
        limit = 25
        cursor = {}
        query_params = [
            limit, 
            cursor,
            {
                "pk_name": "PK", 
                "pk_value": primary_key["PK"], 
                "sk_name": "SK",
                "sk_value": {"S":PrimaryKeyPrefix.USER},
            }
        ]
        self._delete_community_memberships(query_params)
        return response

    def get_communities(self, limit, **kwargs):
        """Return a collection of community models."""
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        if "topic" in kwargs:
            return self.get_communities_by_topic(limit, kwargs["topic"], cursor=cursor)
        elif "country" in kwargs:
            return self.get_communities_by_location(limit, kwargs, cursor=cursor)
        else:
            results = self._dynamodb_client.get_items(
                limit, cursor, "CommunitiesByLocation"
            )
            return self._process_query_or_scan_results(
                results, self._community_mapper, ItemType.COMMUNITY.name
            )

    def get_communities_by_topic(self, limit, topic, cursor={}):
        """Return a collection of community models that have the given topic"""
        partition_key = PrimaryKeyPrefix.TOPIC + topic.upper()
        results = self._dynamodb_client.query(
            limit,
            cursor,
            {"pk_name": "COMMUNITIES_BY_TOPIC_GSI_PK", "pk_value": {"S": partition_key}},
            index="CommunitiesByTopic",
        )
        return self._process_query_or_scan_results(
            results, self._community_mapper, ItemType.COMMUNITY.name
        )

    def get_communities_by_location(self, limit, location, cursor={}):
        """Return a collection of community models that are in the given location"""
        partition_key = PrimaryKeyPrefix.COUNTRY + location["country"].title()
        sort_key = ""
        if "state" in location:
            sort_key += PrimaryKeyPrefix.STATE + location["state"].title()
        if "city" in location:
            sort_key += PrimaryKeyPrefix.CITY + location["city"].title()
        primary_key = {
            "pk_name": "COMMUNITIES_BY_LOCATION_GSI_PK",
            "pk_value": {"S": partition_key},
        }
        if sort_key:
            primary_key["sk_name"] = "COMMUNITIES_BY_LOCATION_GSI_SK"
            primary_key["sk_value"] = {"S": sort_key}
            
        results = self._dynamodb_client.query(
            limit, cursor, primary_key, index="CommunitiesByLocation",
        )
        return self._process_query_or_scan_results(
            results, self._community_mapper, ItemType.COMMUNITY.name
        )

    def add_community_member(self, community_id, user_id):
        """Add a user to a community."""
        community_membership = CommunityMembership(community_id, user_id)
        additional_attributes = {
            "INVERTED_GSI_PK": PrimaryKeyPrefix.USER + user_id,
            "INVERTED_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community_id
        }
        item = self._community_membership_mapper.serialize_from_model(
            community_membership, additional_attributes=additional_attributes
        )

        keys = {
            "community_key": self._community_mapper.key(community_id, community_id),
            "user_key": self._user_mapper.key(user_id, user_id),
        }
        response = self._dynamodb_client.add_community_member(keys, item)
        if "error" in response:
            raise NotFoundException(response["error"])
        return True

    def remove_community_member(self, community_id, user_id):
        """Remove a user from a community."""
        key = self._community_membership_mapper.key(community_id, user_id)
        response = self._dynamodb_client.remove_community_member(key)
        if "error" in response:
            raise NotFoundException(response["error"])
        return True

    def get_community_members(self, community_id, limit, **kwargs):
        """Return a collection of users who are in the given community."""
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        community = self.get_community(community_id)
        if not community:
            raise NotFoundException("Community not found")
        primary_key = self._community_mapper.key(community_id)
        query_results = self._dynamodb_client.query(
            limit,
            cursor,
            {
                "pk_name": "PK", 
                "pk_value": primary_key["PK"], 
                "sk_name": "SK",
                "sk_value": {"S":PrimaryKeyPrefix.USER},
            }
        )
        user_keys = [
            self._user_mapper.key(item["user_id"]["S"], item["user_id"]["S"])
            for item in query_results["Items"]
        ]
        batch_results = self._dynamodb_client.batch_get_items(user_keys)
        response = self._process_batch_results(
            batch_results, self._user_mapper, ItemType.USER.name
        )
        response["has_next"] = query_results["LastEvaluatedKey"] is not None
        response["next"] = encode_cursor(query_results["LastEvaluatedKey"] or {})
        return response

    def get_user_notifications(self, user_id, limit, **kwargs):
        """Return a collection of the user's notifications."""
        user = self.get_user(user_id)
        if not user:
            raise NotFoundException("User not found")
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        user_primary_key = self._user_mapper.key(user_id)
        query_results = self._dynamodb_client.query(
            limit,
            cursor,
            {
                "pk_name": "PK", 
                "pk_value": user_primary_key["PK"], 
                "sk_name": "SK",
                "sk_value": {"S":PrimaryKeyPrefix.NOTIFICATION},
            },
            scan_forward=False
        )
        
        if not query_results["Items"]:
            response = {
                "models": [],
                "total": 0
            }
        else:
            response = self._process_query_or_scan_results(
                query_results, self._notification_mapper, ItemType.NOTIFICATION.name
            )
        response["has_next"] = query_results["LastEvaluatedKey"] is not None
        response["next"] = encode_cursor(query_results["LastEvaluatedKey"] or {})
        return response

    def get_user_notification(self, user_id, notification_id):
        """Return an instance of a notification model."""
        primary_key = self._notification_mapper.key(user_id, notification_id)
        notification_item = self._dynamodb_client.get_item(primary_key)
        if not notification_item:
            return None
        return self._notification_mapper.deserialize_to_model(notification_item)

    def add_user_notification(self, notification):
        """Add or replace a notification in DynamoDB."""
        notification_item = self._notification_mapper.serialize_from_model(
            notification
        )
        response = self._dynamodb_client.put_item(notification_item)
        return response
        
    def add_private_chat(self, primary_user_id, secondary_user_id):
        """Create a private chat member items in DynamoDB."""
        private_chat_id = uuid4().hex
        items = {
            "primary_member": self._private_chat_member_mapper.serialize_from_model(
                PrivateChatMember(private_chat_id, primary_user_id, secondary_user_id)
            ),
            "secondary_member": self._private_chat_member_mapper.serialize_from_model(
                PrivateChatMember(private_chat_id, secondary_user_id, primary_user_id)
            )
        }
        response = self._dynamodb_client.create_private_chat(items)
        return response
        
    def get_user_private_chats(self, user_id, limit, **kwargs):
        """Return a collection of users that the given user has DMs with."""
        user = self.get_user(user_id)
        if not user:
            raise NotFoundException("User not found")
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        primary_key = self._user_mapper.key(user_id)
        query_results = self._dynamodb_client.query(
            limit,
            cursor,
            {
                "pk_name": "PK", 
                "pk_value": primary_key["PK"], 
                "sk_name": "SK",
                "sk_value": {"S":PrimaryKeyPrefix.PRIVATE_CHAT},
            }
        )
        
        if not query_results["Items"]:
            response = {
                "models": [],
                "total": 0
            }
        else:
            user_keys = []
            for item in query_results["Items"]:
                user_key = self._user_mapper.key(
                    item["other_user_id"]["S"], item["other_user_id"]["S"]
                )
                user_keys.append(user_key)
            batch_results = self._dynamodb_client.batch_get_items(user_keys)
            response = self._process_batch_results(
                batch_results, 
                self._user_mapper, 
                ItemType.USER.name
            )
            response["models"] = self._create_private_chats(
                user, response["models"], query_results["Items"]
            )
        response["has_next"] = query_results["LastEvaluatedKey"] is not None
        response["next"] = encode_cursor(query_results["LastEvaluatedKey"] or {})
        return response

    def get_private_chat_messages(self, private_chat_id, limit, **kwargs):
        """Return a collection of messages from a private chat."""
        cursor = {}
        if "cursor" in kwargs:
            cursor = decode_cursor(kwargs["cursor"])
        primary_key = {
            "PK": {"S": PrimaryKeyPrefix.PRIVATE_CHAT + private_chat_id}
        }
        query_results = self._dynamodb_client.query(
            limit,
            cursor,
            {
                "pk_name": "PK", 
                "pk_value": primary_key["PK"], 
                "sk_name": "SK",
                "sk_value": {"S": PrimaryKeyPrefix.PRIVATE_CHAT_MESSAGE},
            },
            scan_forward=False
        )
        return self._process_query_or_scan_results(
            query_results, 
            self._message_mapper, 
            ItemType.PRIVATE_CHAT_MESSAGE.name
        )

    def add_private_chat_message(self, message):
        """Create or replace a private chat message in DynamoDB."""
        message_item = self._message_mapper.serialize_from_model(message)
        if not message.has_reactions():
            del message_item["_reactions"]
        response = self._dynamodb_client.put_item(message_item)
        return response
        
    def remove_message(self, message):
        """Delete a message item from DynamoDB."""
        primary_key = self._message_mapper.key(message.chat_id, message.id)
        response = self._dynamodb_client.delete_item(primary_key)
        return response

    def _process_query_or_scan_results(self, results, mapper, item_type):
        next_cursor = encode_cursor(results["LastEvaluatedKey"] or {})
        models = [
            mapper.deserialize_to_model(item) 
            for item in results["Items"]
            if item["type"]["S"] == item_type
        ]
        response = {
            "models": models,
            "next": next_cursor,
            "has_next": results["LastEvaluatedKey"] is not None,
            "total": len(models),
        }
        return response

    def _process_batch_results(self, results, mapper, item_type):
        models = [
            mapper.deserialize_to_model(item) 
            for item in results["Responses"][self._table_name]
            if item["type"]["S"] == item_type
        ]
        response = {
            "models": models,
            "total": len(models)
        }
    
        return response

    def _create_private_chats(self, primary_user, secondary_users, private_chat_member_items):
        user_chat_mapping = {}
        for item in private_chat_member_items:
            other_user_id = item["other_user_id"]["S"]
            chat_id = item["private_chat_id"]["S"]
            user_chat_mapping[other_user_id] = chat_id

        private_chats = []
        for secondary_user in secondary_users:
            private_chat_id = user_chat_mapping[secondary_user.id]
            private_chats.append(PrivateChat(private_chat_id, primary_user, secondary_user))
        return private_chats


dynamodb_repository = _DynamoDBRepository(
    dynamodb_client,
    user_mapper=UserMapper(),
    username_mapper=UsernameMapper(),
    user_email_mapper=UserEmailMapper(),
    community_mapper=CommunityMapper(),
    community_name_mapper=CommunityNameMapper(),
    community_membership_mapper=CommunityMembershipMapper(),
    notification_mapper=NotificationMapper(),
    private_chat_member_mapper=PrivateChatMemberMapper(),
    message_mapper=MessageMapper()
)

