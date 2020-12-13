"""This module contains the role model and related classes/functions"""


from enum import Enum


class Role:
    """Class to represent a user role."""

    def __init__(self, name, permissions):
        self.name = name
        self._permissions = permissions

    def has_permissions(self, permissions):
        """Return True if this role grants a user
        the given permissions, else return False.
        """
        return permissions in self._permissions

    def add_permissions(self, permissions):
        """Add the given permissions to the set of
        permissions that the role has.
        """
        self._permissions.add(permissions)

    def remove_permissions(self, permissions):
        """Remove the given permissions from the set
        of permissions that the role has.
        """
        self._permissions.remove(permissions)

    def to_map(self):
        """Return a representation of a role as stored in DynamoDB."""
        return {
            "M": {
                "name": {"S": self.name.name},
                "permissions": {"SS": [perm.name for perm in self._permissions]},
            }
        }

    def __repr__(self):
        """Return a representation of a role model."""
        return "Role(name=%r, permissions=%r)" % (self.name, self._permissions)


class RolePermission(Enum):
    """Enum to represent various permissions applied broadly
    to a given role.
    """

    READ_CHAT_MESSAGE = 1
    WRITE_CHAT_MESSAGE = 2
    EDIT_CHAT_MESSAGE = 3
    DELETE_CHAT_MESSAGE = 4
    CREATE_CHAT = 5
    EDIT_CHAT = 6
    DELETE_CHAT = 7
    BAN_USERS = 8


class RoleName(Enum):
    """Class thats holds constants of role names."""

    REGULAR_USER = 1
    MODERATOR = 2
    ADMIN = 3

