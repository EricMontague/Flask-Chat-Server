"""This module contains the role model and related classes/functions"""


from enum import Enum


class Role:
    """Class to represent a user role."""

    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def has_permissions(self, permissions):
        """Return True if this role grants a user
        the given permissions, else return False.
        """
        return permissions in self.permissions

    def add_persmissions(self, permissions):
        """Add the given permissions to the set of
        permissions that the role has.
        """
        self.permissions.add(permissions)

    def remove_permissions(self, permissions):
        """Remove the given permissions from the set
        of permissions that the role has.
        """
        self.permissions.remove(permissions)

    def __repr__(self):
        """Return a representation of a role model."""
        return "Role(name=%r, permissions=%r)" % (self.name, self.permissions)


class RolePermission(Enum):
    """Enum to represent various permissions applied broadly
    to a given role.
    """

    READ_CHAT_MESSAGE = 0
    WRITE_CHAT_MESSAGE = 1
    EDIT_CHAT_MESSAGE = 2
    DELETE_CHAT_MESSAGE = 3
    CREATE_CHAT = 4
    EDIT_CHAT = 5
    DELETE_CHAT = 6
    CREATE_COMMUNITY = 7
    EDIT_COMMUNITY = 8
    DELETE_COMMUNITY = 9


class RoleName:
    """Class thats holds constants of role names."""

    REGULAR_USER = "regular_user"
    MODERATOR = "moderator"
    ADMIN = "admin"

