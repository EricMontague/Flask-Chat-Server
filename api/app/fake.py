"""This file contains a class that uses the faker package for
inserted fake data into the database.
"""


import random
import time
from uuid import uuid4
from pprint import pprint
from datetime import datetime
from faker import Faker
from app.clients import dynamodb_client
from app.repositories import dynamodb_repository
from app.dynamodb_mappers import (
    UserMapper,
    UsernameMapper,
    UserEmailMapper,
    CommunityMapper,
    CommunityNameMapper,
    CommunityMembershipMapper,
    NotificationMapper,
    PrivateChatMemberMapper,
    PrivateChatMessageMapper,
    GroupChatMemberMapper,
    GroupChatMapper,
    GroupChatMessageMapper,
)
from app.models.factories import UserFactory, CommunityFactory
from app.models import (
    UserEmail,
    Username,
    CommunityName,
    CommunityMembership,
    CommunityTopic,
    Notification,
    NotificationType,
    PrivateChatMember,
    Message,
    GroupChat,
    GroupChatMember,
)
from app.dynamodb_mappers.constants import PrimaryKeyPrefix


user_mapper = UserMapper()
username_mapper = UsernameMapper()
user_email_mapper = UserEmailMapper()
community_mapper = CommunityMapper()
community_name_mapper = CommunityNameMapper()
community_membership_mapper = CommunityMembershipMapper()
notification_mapper = NotificationMapper()
private_chat_member_mapper = PrivateChatMemberMapper()
private_chat_message_mapper = PrivateChatMessageMapper()
group_chat_member_mapper = GroupChatMemberMapper()
group_chat_mapper = GroupChatMapper()
group_chat_message_mapper = GroupChatMessageMapper()


TOPICS = [topic for topic in CommunityTopic]
LOCATIONS = [
    {"city": "New York", "state": "New York", "country": "United States"},
    {"city": "Philadelphia", "state": "Pennsylvania", "country": "United States"},
    {"city": "Chicago", "state": "Illinois", "country": "United States"},
    {"city": "San Francisco", "state": "California", "country": "United States"},
    {"city": "Miami", "state": "Florida", "country": "United States"},
]


# This should only be used with DynamoDB Local due to the high consumption of RCUs and WCUs
# this causes
class FakeDataGenerator:
    """Class to generate fake data for the application."""

    def __init__(
        self,
        num_users=25,
        num_communities=25,
        num_notifications=25,
        num_private_chats=25,
        num_group_chats=25,
        messages_per_chat=5,
    ):
        self._faker = Faker()
        self.num_users = num_users
        self.num_communities = num_communities
        self.num_notifications = num_notifications
        self.num_private_chats = num_private_chats
        self.num_group_chats = num_group_chats
        self.messages_per_chat = messages_per_chat
    
    def add_all(self):
        """Add all data to DynamoDB."""
        print("Adding users...")
        self.add_users()
        time.sleep(1)

        print("Adding communities...")
        self.add_communities()
        time.sleep(1)

        print("Adding private chats...")
        self.add_private_chats()
        time.sleep(1)

        print("Adding private chat messages...")
        self.add_private_chat_messages()
        time.sleep(1)

        print("Adding group chats and messages...")
        self.add_group_chats()

        print("Done!")

    def add_users(self):
        """Add fake user data to the database."""
        remaining_users = self.num_users
        while remaining_users > 0:
            requests = []
            user_data = self._generate_fake_user_data()
            user = UserFactory.create_user(user_data)
            user_email = UserEmail(user.id, user.email)
            username = Username(user.id, user.username)
            additional_attributes = {
                "USERS_GSI_PK": PrimaryKeyPrefix.USER + user.id,
                "USERS_GSI_SK": user.username,
            }
            requests.append(
                (
                    "PutRequest",
                    user_mapper.serialize_from_model(
                        user, additional_attributes=additional_attributes
                    ),
                )
            )
            requests.append(
                ("PutRequest", user_email_mapper.serialize_from_model(user_email))
            )
            requests.append(
                ("PutRequest", username_mapper.serialize_from_model(username))
            )
            dynamodb_client.batch_write_items(requests)
            remaining_users -= 1

    def add_communities(self):
        """Add fake community data to the database."""
        results = dynamodb_repository.get_users(self.num_users)
        users = results["models"]
        remaining_communities = self.num_communities
        while remaining_communities > 0:
            random_user = random.choice(users)
            requests = []
            community_data = self._generate_fake_community_data()
            community = CommunityFactory.create_community(community_data)
            community_name = CommunityName(community.id, community.name)
            community_membership = CommunityMembership(
                community.id, random_user.id, is_founder=True
            )
            membership_additional_attributes = {
                "INVERTED_GSI_PK": PrimaryKeyPrefix.USER + random_user.id,
                "INVERTED_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community.id,
            }
            community_additional_attributes = {
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
            requests.append(
                (
                    "PutRequest",
                    community_mapper.serialize_from_model(
                        community, additional_attributes=community_additional_attributes
                    ),
                )
            )
            requests.append(
                (
                    "PutRequest",
                    community_membership_mapper.serialize_from_model(
                        community_membership,
                        additional_attributes=membership_additional_attributes,
                    ),
                )
            )
            requests.append(
                (
                    "PutRequest",
                    community_name_mapper.serialize_from_model(community_name),
                )
            )
            dynamodb_client.batch_write_items(requests)
            remaining_communities -= 1

    def add_private_chats(self):
        """Add fake private chat data to the database."""
        results = dynamodb_repository.get_users(self.num_users)
        users = results["models"]
        remaining_private_chats = self.num_private_chats

        while remaining_private_chats > 0:
            requests = []
            primary_user, secondary_user = self._pick_private_chat_members(users)
            primary_additional_attributes = {
                "INVERTED_GSI_PK": PrimaryKeyPrefix.PRIVATE_CHAT
                + primary_user.private_chat_id,
                "INVERTED_GSI_SK": PrimaryKeyPrefix.USER + primary_user.user_id,
            }
            secondary_additional_attributes = {
                "INVERTED_GSI_PK": PrimaryKeyPrefix.PRIVATE_CHAT
                + secondary_user.private_chat_id,
                "INVERTED_GSI_SK": PrimaryKeyPrefix.USER + secondary_user.user_id,
            }
            primary_item = private_chat_member_mapper.serialize_from_model(
                primary_user, additional_attributes=primary_additional_attributes
            )
            secondary_item = private_chat_member_mapper.serialize_from_model(
                secondary_user, additional_attributes=secondary_additional_attributes
            )
            requests.append(("PutRequest", primary_item))
            requests.append(("PutRequest", secondary_item))
            dynamodb_client.batch_write_items(requests)
            remaining_private_chats -= 1

    def add_private_chat_messages(self):
        """Add fake private chat message data to the database."""
        requests = []
        results = dynamodb_repository.get_users(self.num_users // 2)
        users = results["models"]
        for user in users:
            results = dynamodb_repository.get_user_private_chats(user.id, 1)
            chats = results["models"]
            if not chats:
                continue
            for i in range(self.messages_per_chat):
                random_chat = random.choice(chats)
                message = self._create_message(random_chat.id, user.id)
                target_url = f"http://127.0.0.1:5000/api/v1/private_chats/{random_chat.id}/messages/{message.id}"
                notification = self._generate_fake_notification(
                    user.id, target_url, NotificationType.NEW_PRIVATE_CHAT_MESSAGE
                )
                notification_item = notification_mapper.serialize_from_model(
                    notification
                )
                message_item = private_chat_message_mapper.serialize_from_model(message)
                if not message.has_reactions():
                    del message_item["_reactions"]
                requests.append(("PutRequest", message_item))
                requests.append(("PutRequest", notification_item))
        
        self._write_batches(requests)

    def add_group_chats(self):
        """Add fake group chat data to the database."""
        requests = []
        group_chats_by_community_id = {}
        user_results = dynamodb_repository.get_users(self.num_users)
        community_results = dynamodb_repository.get_communities(self.num_communities)
        users = user_results["models"]
        communities = community_results["models"]
        remaining_group_chats = self.num_group_chats

        while remaining_group_chats > 0:
            
            members = random.sample(users, 3)
            random_community = random.choice(communities)
            group_chat = GroupChat(
                uuid4().hex,
                random_community.id,
                self._faker.paragraph()[:24],
                self._faker.paragraph()[:80],
            )
            group_chats_by_community_id[random_community.id] = group_chat
            group_chat_item = group_chat_mapper.serialize_from_model(group_chat)
            requests.append(("PutRequest", group_chat_item))
            for member in members:
                membership_additional_attributes = {
                    "INVERTED_GSI_PK": PrimaryKeyPrefix.USER + member.id,
                    "INVERTED_GSI_SK": PrimaryKeyPrefix.GROUP_CHAT + group_chat.id,
                }
                chat_member_item = group_chat_member_mapper.serialize_from_model(
                    GroupChatMember(group_chat.id, member.id, random_community.id),
                    additional_attributes=membership_additional_attributes,
                )
                requests.append(("PutRequest", chat_member_item))
            remaining_group_chats -= 1

        self._write_batches(requests)
        time.sleep(1)
        self.add_group_chat_messages(group_chats_by_community_id)

    def add_group_chat_messages(self, group_chats_by_community_id):
        """Add fake group chat message data to the database."""
        requests = []
        results = dynamodb_repository.get_communities(self.num_communities//2)
        communities = results["models"]
        for community in communities:
            if community.id in group_chats_by_community_id:
                group_chat = group_chats_by_community_id[community.id]
                results = dynamodb_repository.get_group_chat_members(
                    community.id, group_chat.id, self.num_users
                )
                users = results["models"]
                for i in range(self.messages_per_chat):
                    random_user = random.choice(users)
                    message = self._create_message(group_chat.id, random_user.id)
                    target_url = f"http://127.0.0.1:5000/api/v1/group_chats/{group_chat.id}/messages/{message.id}"
                    notification = self._generate_fake_notification(
                        random_user.id, target_url, NotificationType.NEW_GROUP_CHAT_MESSAGE
                    )
                    notification_item = notification_mapper.serialize_from_model(
                        notification
                    )
                    message_item = group_chat_message_mapper.serialize_from_model(
                        message
                    )
                    if not message.has_reactions():
                        del message_item["_reactions"]
                    requests.append(("PutRequest", message_item))
                    requests.append(("PutRequest", notification_item))
        self._write_batches(requests)
        
    def _generate_fake_community_data(self):
        """Return fake community data as a dictionary."""
        fake_community_data = {
            "name": self._faker.name(),
            "description": self._faker.paragraph()[:280],
            "topic": random.choice(TOPICS),
            "location": random.choice(LOCATIONS),
        }
        return fake_community_data

    def _generate_fake_user_data(self):
        """Return fake user data as a dictionary."""
        name = self._faker.name()
        fake_user_data = {
            "name": name,
            "username": name.replace(" ", "") + "123",
            "email": self._faker.email(),
            "password": "password",
            "location": {
                "city": self._faker.city(),
                "state": self._faker.state(),
                "country": "United States",
            },
        }
        return fake_user_data

    def _generate_fake_notification(self, user_id, target_url, notification_type):
        """Return an instance of a notification."""
        created_at = datetime.now()
        return Notification(
            created_at.strftime("%Y-%m-%dT%H:%M:%S.%f") + "-" + uuid4().hex,
            user_id,
            notification_type,
            self._faker.paragraph()[:60],
            target_url,
            created_at=created_at,
        )

    def _pick_private_chat_members(self, users):
        """Choose two random users to form a private chat and
        return a list of two PrivateChatMember instances.
        """
        primary_user, secondary_user = random.sample(users, 2)
        chat_id = sorted([primary_user.id, secondary_user.id])[0]
        primary = PrivateChatMember(chat_id, primary_user.id, secondary_user.id)
        secondary = PrivateChatMember(chat_id, secondary_user.id, primary_user.id)
        return [primary, secondary]

    def _create_message(self, chat_id, user_id):
        """Return an instance of a message model."""
        now = datetime.now()
        return Message(
            now.isoformat() + "-" + uuid4().hex,
            chat_id,
            user_id,
            self._faker.paragraph()[:50],
            created_at=now,
        )
    
    def _write_batches(self, requests):
        """Batch requests to DynamoDB."""
        while requests:
            batch = []
            for i in range(25):
                try:
                    batch.append(requests.pop())
                except IndexError:
                    break
            dynamodb_client.batch_write_items(batch)