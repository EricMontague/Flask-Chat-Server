"""This module contains the community model and related functions/classes"""


from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from app.exceptions import CommunityMemberNotFoundException


class Community:
    """Class to represent a community."""

    def __init__(
        self,
        id,
        name,
        description,
        topic,
        avatar,
        cover_photo,
        location,
        created_at=datetime.now(),
    ):
        self._id = id
        self.name = name
        self.description = description
        self.topic = topic
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.location = location
        self._created_at = created_at
        self._members = {}
        self._group_chats = {}

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
    """Class to represent the relationship between a community
    and a user who is a member of that community.
    """

    community_id: str
    user_id: str
    created_at: datetime = datetime.now()
    is_founder: bool = False


@dataclass(frozen=True)
class CommunityName:
    """Class to be used in DynamoDB to enforce a uniqueness constraint
    on a community's name.
    """

    community_id: str
    name: str


class CommunityPermission(Enum):
    """Enum to represent community permissions."""

    CREATE_COMMUNITY = 1
    EDIT_COMMUNITY = 2
    DELETE_COMMUNITY = 3


@dataclass(frozen=True)
class CommunityGroupChatRelation:
    """Class to represent the relationship between group chats and communities."""

    group_chat_id: str
    community_id: str
    created_at: datetime = datetime.now()


class CommunityTopic(Enum):
    """Class to represent a topic for a community."""

    ANXIETY = 1
    DEPRESSION = 2
    ADDICTION = 3
    PTSD = 4
    OBSESSIVE_COMPULSIVE_DISORDER = 5

