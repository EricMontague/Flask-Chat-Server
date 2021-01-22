"""This module contains decorators that deal with authentication and authorization."""


import functools
import base64
import json
from json.decoder import JSONDecodeError
from http import HTTPStatus
from flask import request, current_app, g
from flask_socketio import disconnect, emit, ConnectionRefusedError
from app.repositories import database_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.models import User, TokenType


def permission_required(permission):
    """Decorator to check an authenticated user's permissions."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not g.current_user.has_permission(permission):
                return (
                    {
                        "error": "You do not have the required permissions to access this endpoint"
                    },
                    HTTPStatus.FORBIDDEN,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(func):
    """Decorator to be placed over routes only accessible by an authenticated user with
    admin priveleges.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not g.current_user.is_admin():
            return (
                {
                    "error": "You do not have the required permissions to access this endpoint"
                },
                HTTPStatus.FORBIDDEN,
            )
        return func(*args, **kwargs)

    return wrapper


def socketio_permission_required(permission):
    """Decorator to be used to protect socketio event handlers."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not g.current_user.has_permission(permission):
                emit("error", json.dumps({"error": "You do not have the required permissions to perform this action"}))
                disconnect()
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def is_blacklisted(decoded_token, token_type):
    """Return True if the given token is blacklisted."""
    token = database_repository.get_token(decoded_token.raw_jwt, token_type)
    if not token:
        return True
    return token.is_blacklisted


def jwt_required(token_type):
    """Decorator used to protect routes that require an authenticated user."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return (
                    {"error": "Missing token in authorization header"},
                    HTTPStatus.UNAUTHORIZED,
                )
            auth_type = "Bearer"
            bearer_start_index = auth_header.find(auth_type)
            raw_jwt = auth_header[bearer_start_index + len(auth_type) :].strip()
            if not raw_jwt:
                return (
                    {"error": "Missing token in authorization headers"},
                    HTTPStatus.UNAUTHORIZED,
                )
            decoded_token = User.decode_token(raw_jwt, current_app.config["SECRET_KEY"])
            if not decoded_token:
                return (
                    {"error": f"Invalid {token_type.name.replace('_', ' ').lower()}"},
                    HTTPStatus.UNAUTHORIZED,
                )

            if decoded_token.token_type != token_type:
                return (
                    {"error": "Incorrect token type provided"},
                    HTTPStatus.UNAUTHORIZED,
                )

            if is_blacklisted(decoded_token, token_type):
                return (
                    {"error": f"Token is blacklisted"},
                    HTTPStatus.UNAUTHORIZED,
                )
            current_user = database_repository.get_user(decoded_token.user_id)
            if not current_user:
                return {"error": "User not found"}
            if current_user.is_banned:
                return {"error": "User is banned"}, HTTPStatus.UNAUTHORIZED
            g.current_user = current_user
            g.decoded_token = decoded_token
            return func(*args, **kwargs)

        return wrapper

    return decorator

def socketio_jwt_required(token_type):
    """Decorator used to protect socketio event handlers that require an authenticated user."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raw_jwt = request.args.get("token")
            if not raw_jwt:
                disconnect()
            else:
                decoded_token = User.decode_token(
                    raw_jwt, current_app.config["SECRET_KEY"]
                )
                if not decoded_token:
                    disconnect()
                elif decoded_token.token_type != token_type:
                    disconnect()
                elif is_blacklisted(decoded_token, token_type):
                    disconnect()
                else:
                    current_user = database_repository.get_user(decoded_token.user_id)
                    if not current_user:
                        disconnect()
                    elif current_user.is_banned:
                        disconnect()
                    else:
                        g.current_user = current_user
                        g.decoded_token = decoded_token
                        return func(*args, **kwargs)

        return wrapper

    return decorator


def basic_auth_required(func):
    """Decorator to protect a route that requires authentication via HTTP basic auth."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return (
                {"error": "Missing credentials in authorization header"},
                HTTPStatus.UNAUTHORIZED,
            )
        # get username and password from auth headers
        auth_type, auth_header_value = auth_header.split()
        decoded_header = base64.b64decode(auth_header_value).decode("utf-8")
        username, password = decoded_header.split(":")

        # Verify user credentials
        if not username:
            return {"error": "Missing username"}, HTTPStatus.UNAUTHORIZED
        if not password:
            return (
                {"error": "Missing user password"},
                HTTPStatus.UNAUTHORIZED,
            )
        current_user = database_repository.get_user_by_username(username)
        if not current_user:
            return {"error": "User could not be found"}, HTTPStatus.NOT_FOUND
        if current_user.is_banned:
            return {"error": "User is banned"}, HTTPStatus.UNAUTHORIZED
        if not current_user.verify_password(password):
            return {"error": "Incorrect password provided"}, HTTPStatus.UNAUTHORIZED
        g.current_user = current_user
        return func(*args, **kwargs)

    return wrapper
