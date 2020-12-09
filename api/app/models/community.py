"""This module contains the community model and related functions/classes"""


from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from app.exceptions import CommunityMemberNotFoundException
from app.dynamodb.constants import PrimaryKeyPrefix, ItemType


class Community:
    """Class to represent a community."""

    def __init__(
        self, id, name, description, topic, avatar, cover_photo, location, founder,
    ):
        self._id = id
        self.name = name
        self.description = description
        self.topic = topic
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.location = location
        self._created_at = datetime.now()
        self._members = {}
        self._group_chats = {}
        self._founder = founder

    @property
    def id(self):
        """Return the community's id."""
        return self._id

    @property
    def founded_on(self):
        """Return the datetime when the community was created."""
        return self._created_at

    @property
    def num_members(self):
        """Return the number of members in the community."""
        return len(self._members)

    @property
    def num_group_chats(self):
        """Return the number of group chats in the community."""
        return len(self._group_chats)

    def num_members_online(self):
        """Return the total number of community members online."""
        total = 0
        for id in self._members:
            if self._members[id].is_online:
                total += 1
        return total

    def add_member(self, member):
        """Add a member to the community."""
        self._members[member.id] = member

    def remove_member(self, member_id):
        """Remove a member from the community."""
        if not self.is_member(member_id):
            raise CommunityMemberNotFoundException(
                "User is not a member of this community"
            )
        self._members.pop(member_id)

    def is_member(self, member_id):
        """Return True if the user is a member of this community,
        otherwise return False.
        """
        return member_id in self._members

    def to_item(self):
        """Return a representation of a community as stored in DynamoDB."""
        return {
            "PK": PrimaryKeyPrefix.COMMUNITY + self._id,
            "SK": PrimaryKeyPrefix.COMMUNITY + self._id,
            "community_id": PrimaryKeyPrefix.COMMUNITY + self._id,
            "name": self.name,
            "description": self.description,
            "topic": self.topic.name,
            "avatar": self.avatar.to_item(),
            "cover_photo": self.cover_photo.to_item(),
            "location": self.location.to_item(),
            "country": PrimaryKeyPrefix.COUNTRY + self.location.country,
            "state_city": (
                PrimaryKeyPrefix.STATE
                + self.location.state
                + PrimaryKeyPrefix.CITY
                + self.location.city
            ),
            "created_at": self._created_at.isoformat(),
            "founder_id": self._founder.id,
        }

    def __repr__(self):
        """Return a representation of a community. Some attributes are not
        shown in order to reduce verbosity.
        """
        return (
            "Community(id=%r, name=%r, description=%r, topic=%r,"
            + "avatar=%r, cover_photo=%r, location=%r)"
        ) % (
            self._id,
            self.name,
            self.description,
            self.topic,
            self.avatar,
            self.cover_photo,
            self.location,
        )


@dataclass(frozen=True)
class CommunityMembership:
    """Class to represent the relationship between users and communities."""

    user_id: str
    community_id: str
    created_at: datetime = datetime.now()

    def key(self):
        """Return the primary key of the community membership model for
        DynamoDB.
        """
        return {
            "PK": PrimaryKeyPrefix.USER + self.user_id,
            "SK": PrimaryKeyPrefix.COMMUNITY + self.community_id,
        }

    def to_item(self):
        """Return the representation of a community membership as stored in
        DynamoDB.
        """
        return {
            **self.key(),
            "community_membership_id": self.user_id + "#" + self.community_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True)
class CommunityGroupChatRelation:
    """Class to represent the relationship between group chats and communities."""

    group_chat_id: str
    community_id: str
    created_at: datetime = datetime.now()

    def to_item(self):
        """Return the representation of a relationship between a group chat
        and a community as stored in DynamoDB.
        """
        return {
            "PK": PrimaryKeyPrefix.GROUP_CHAT + self.group_chat_id,
            "SK": PrimaryKeyPrefix.COMMUNITY + self.community_id,
            "community_group_chat_relation": self.group_chat_id + "#" + self.community_id,
            "created_at": self.created_at.isoformat()
        }



class CommunityTopic(Enum):
    """Class to represent a topic for a community."""

    ANXIETY = 0
    DEPRESSION = 1
    ADDICTION = 2
    PTSD = 3
    OBSESSIVE_COMPULSIVE_DISORDER = 4

