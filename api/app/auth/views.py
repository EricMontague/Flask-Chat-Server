"""This module contains view functions for the auth blueprint."""


from http import HTTPStatus
from flask import current_app, request, url_for
from app.auth import auth
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException
from app.models import User, TokenType
from app.models.factories import UserFactory
from app.helpers import auth_required, handle_request, handle_response
from app.schemas import UserSchema


# TODO - Verify that a user has only one access and refresh token at a time
@auth.route("/login", methods=["POST"])
def login():
    """Log a user into the application and return their JWTs."""
    login_credentials = request.json
    if not login_credentials:
        return {"error": "Missing JSON body in request"}, HTTPStatus.BAD_REQUEST
    email = login_credentials.get("email")
    password = login_credentials.get("password")

    # Verify user credentials
    if not email:
        return {"error": "Email is a required field"}, HTTPStatus.UNPROCESSABLE_ENTITY
    if not password:
        return {"error": "Password is a required field"}, HTTPStatus.UNPROCESSABLE_ENTITY
    user = dynamodb_repository.get_user_by("email", email)
    if not user:
        return {"error": "User could not be found"}, HTTPStatus.NOT_FOUND
    if not user.verify_password(password):
        return {"error": "Incorret password provided"}, HTTPStatus.UNAUTHORIZED

    # Create tokens
    claims = {"user_id": user.id}
    access_token = User.encode_token(
        claims, 
        current_app.config["SECRET_KEY"],
        current_app.config["ACCESS_TOKEN_LIFESPAN"],
        TokenType.ACCESS_TOKEN
    )
    refresh_token = User.encode_token(
        claims,
        current_app.config["SECRET_KEY"],
        current_app.config["REFRESH_TOKEN_LIFESPAN"],
        TokenType.REFRESH_TOKEN
    )

    # Add tokens to database
    dynamodb_repository.add_token(access_token)
    dynamodb_repository.add_token(refresh_token)
    return {
        "access_token": access_token.raw_jwt, 
        "refresh_token": refresh_token.raw_jwt
        }, HTTPStatus.CREATED


@auth.route("/register", methods=["POST"])
@handle_request(UserSchema())
@handle_response(UserSchema())
def create_user(user_data):
    """Create a new user resource."""
    user = UserFactory.create_user(user_data)
    try:
        dynamodb_repository.add_user(user)
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    headers = {"Location": url_for("api.get_user", user_id=user.id)}
    return user, HTTPStatus.CREATED, headers


@auth.route("/refresh_token", methods=["POST"])
def refresh_access_token():
    """Refresh a user's access token."""
    pass


@auth.route("/revoke_tokens", methods=["DELETE"])
def revoke_tokens():
    """Revoke both of a user's access and refresh tokens."""
    login_credentials = request.json
    if not login_credentials:
        return {"error": "Missing JSON body in request"}, HTTPStatus.BAD_REQUEST
    email = login_credentials.get("email")
    password = login_credentials.get("password")

    # Verify user credentials
    if not email:
        return {"error": "Email is a required field"}, HTTPStatus.UNPROCESSABLE_ENTITY
    if not password:
        return {"error": "Password is a required field"}, HTTPStatus.UNPROCESSABLE_ENTITY
    user = dynamodb_repository.get_user("email", email)
    if not user:
        return {"error": "User could not be found"}, HTTPStatus.NOT_FOUND
    if not user.verify_password(password):
        return {"error": "Incorret password provided"}, HTTPStatus.UNAUTHORIZED
    
    # Get user's tokens and blacklist them
    tokens = dynamodb_repository.get_user_tokens(user.id)
    for token in tokens:
        token.is_blacklisted = True
        dynamodb_repository.add_token(token)
    return {}, HTTPStatus.NO_CONTENT