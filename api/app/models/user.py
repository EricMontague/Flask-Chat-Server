"""This module contains the user model."""


import jwt
from app.models.token import Token, TokenType
from app.models.role import PermissionsError, RoleName
from app import bcrypt
from dataclasses import dataclass
from datetime import datetime, timedelta


class User:
    """Class to represent a user."""

    def __init__(
        self,
        id,
        username,
        name,
        email,
        role,
        bio="",
        last_seen_at=datetime.now(),
        created_at=datetime.now(),
        location=None,
        avatar=None,
        cover_photo=None,
        is_online=True,
        is_banned=False,
    ):
        self._id = id
        self.username = username
        self.name = name
        self._password_hash = None
        self.email = email
        self.bio = bio
        self.location = location
        self._created_at = created_at
        self.last_seen_at = last_seen_at
        self.avatar = avatar
        self.cover_photo = cover_photo
        self.role = role
        self.is_online = is_online
        self.is_banned = is_banned

    @property
    def id(self):
        """Return the user id."""
        return self._id

    @property
    def joined_on(self):
        """Return the timestamp of when the user was created."""
        return self._created_at

    @property
    def password(self):
        """Raise an AttributeError is an attempt is made to read the
        password attribute.
        """
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Hash and set the user's password."""
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Return True if the given password matches the user's password,
        otherwise return False.
        """
        return bcrypt.check_password_hash(self._password_hash, password)

    def ping(self):
        """Mark the user as recently seen and online."""
        self._last_seen_at = datetime.now()
        self.is_online = True

    def has_permission(self, permission):
        """Return True if the user has the given permission,
        otherwise return False. Permissions are determined by the
        role that the user has.
        """
        if self.is_banned:
            return False
        return self.role.has_permission(permission)

    def add_permission(self, permission):
        """Grant the given permission to the user"""
        if self.is_banned:
            raise PermissionsError("Cannot change the permissions of a banned user")
        self.role.add_permission(permission)

    def remove_permission(self, permission):
        """Remove the given permission from the user."""
        if self.is_banned:
            raise PermissionsError("Cannot change the permissions of a banned user")
        self.role.remove_permission(permission)

    def reset_permissions(self):
        """Remove all of a user's permissions."""
        self.role.reset_permissions()

    def is_admin(self):
        """Return True if the user has admin priveleges, else return False."""
        return self.role.name == RoleName.ADMIN

    @classmethod
    def encode_token(self, claims, secret, expires_in):
        """Return a JWT with the given payload."""
        if "user_id" not in claims:
            raise ValueError("User Id missing from token claims")
        if "token_type" not in claims:
            raise ValueError("Token type missing from token claims")
        utcnow = datetime.utcnow()
        expiration_date = utcnow + timedelta(seconds=expires_in)
        claims.update({"exp": int(expiration_date.timestamp())})
        claims.update({"iat": int(utcnow.timestamp())})
        encoded_token = jwt.encode(claims, secret, algorithm="HS256")
        return Token(
            claims["user_id"],
            encoded_token,
            claims["exp"],
            claims["iat"],
            TokenType[claims["token_type"]],
        )

    @classmethod
    def decode_token(self, encoded_token, secret):
        """Decode an encoded JWT and return the decoded token."""
        decoded_token = None
        try:
            decoded_token = jwt.decode(encoded_token, secret, algorithms="HS256")
        except jwt.InvalidTokenError:
            return None
        return Token(
            decoded_token["user_id"],
            encoded_token,
            decoded_token["exp"],
            decoded_token["iat"],
            TokenType[decoded_token["token_type"]],
        )

    def __repr__(self):
        """Return a representation of a user."""
        return (
            "User(id=%r, username=%r, name=%r,"
            + "email=%r, bio=%r,created_at=%r, last_seen_at=%r,"
            + "avatar=%r, cover_photo=%r, role=%r"
        ) % (
            self._id,
            self.username,
            self.name,
            self.email,
            self.bio,
            self._created_at,
            self.last_seen_at,
            self.avatar,
            self.cover_photo,
            self.role,
        )


@dataclass(frozen=True)
class UserEmail:
    """Class to be used to enforce uniqueness of a user's email
    in DynamoDB.
    """

    user_id: str
    email: str


@dataclass(frozen=True)
class Username:
    """Class be used to enforce uniqueness of a user's username in DynamoDB."""

    user_id: str
    username: str

