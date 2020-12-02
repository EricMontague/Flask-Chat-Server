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
        members,
        group_chats,
        founder,
    ):
        self._id = id
        self.name = name
        self.description = description
        self.topic = topic
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.location = location
        self._created_at = datetime.now()
        self._members = members
        self._group_chats = group_chats
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




class Topic(Enum):
    """Class to represent a topic for a community."""

    ANXIETY = 0
    DEPRESSION = 1
    ADDICTION = 2
    PTSD = 3
    OBSESSIVE_COMPULSIVE_DISORDER = 4

