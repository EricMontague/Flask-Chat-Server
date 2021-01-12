"""This module contains the role model and related classes/functions"""


from enum import Enum


class Role:
    """Class to represent a user role."""

    def __init__(self, name, permissions):
        self.name = name
        self._permissions = permissions

    def has_permission(self, permission):
        """Return True if this role grants a user
        the given permission, else return False.
        """
        return permission in self._permissions

    def add_permission(self, permission):
        """Add the given permission to the set of
        permissions that the role has.
        """
        self._permissions.add(permission)

    def remove_permission(self, permission):
        """Remove the given permission from the set
        of permissions that the role has.
        """
        self._permissions.remove(permission)

    def reset_permissions(self):
        """Remove all permissions."""
        self._permissions = set()

    @property
    def permissions(self):
        """Return a list of the user's permissions."""
        return list(self._permissions)

    def __repr__(self):
        """Return a representation of a role model."""
        return "Role(name=%r, permissions=%r)" % (self.name, self._permissions)


class RolePermission(Enum):
    """Enum to represent various permissions applied broadly
    to a given role.
    """

    READ_CHAT_MESSAGE = 1
    WRITE_CHAT_MESSAGE = 2
    CREATE_GROUP_CHAT = 3
    JOIN_GROUP_CHAT = 4
    CREATE_PRIVATE_CHAT = 5
    CREATE_COMMUNITY = 6
    JOIN_COMMUNITY = 7
    BAN_USER = 8


class RoleName(Enum):
    """Class thats holds constants of role names."""

    REGULAR_USER = 1
    MODERATOR = 2
    ADMIN = 3


regular_user_role = Role(
    RoleName.REGULAR_USER, 
    {perm for perm in RolePermission if perm != RolePermission.BAN_USER}
)
admin_user_role =  Role(
    RoleName.ADMIN, 
    {perm for perm in RolePermission}
)


class PermissionsError(Exception):
    """Raises when an error occurs involving a user's permissions."""
