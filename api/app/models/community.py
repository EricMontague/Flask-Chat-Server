"""This module contains the community model and related functions/classes"""


from datetime import datetime
from dataclasses import dataclass
from enum import Enum


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
        founder_id,
        created_at=datetime.now(),
    ):
        self._id = id
        self.name = name
        self.description = description
        self.topic = topic
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.location = location
        self._founder_id = founder_id
        self._created_at = created_at

    @property
    def id(self):
        """Return the community's id."""
        return self._id

    @property
    def founded_on(self):
        """Return the datetime when the community was created."""
        return self._created_at

    @property
    def founder_id(self):
        """Return the id of the user who founded this community."""
        return self._founder_id

    def __repr__(self):
        """Return a representation of a community. Some attributes are not
        shown in order to reduce verbosity.
        """
        return (
            "Community(id=%r, name=%r, description=%r, topic=%r,"
            + "avatar=%r, cover_photo=%r, location=%r, founder_id=%r)"
        ) % (
            self._id,
            self.name,
            self.description,
            self.topic,
            self.avatar,
            self.cover_photo,
            self.location,
            self._founder_id
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


class CommunityTopic(Enum):
    """Class to represent a topic for a community."""

    ANXIETY = 1
    DEPRESSION = 2
    ADDICTION = 3
    PTSD = 4
    OBSESSIVE_COMPULSIVE_DISORDER = 5

