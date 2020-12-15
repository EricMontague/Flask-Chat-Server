"""This module contains view functions for accessing user resources."""


from http import HTTPStatus
from flask import current_app, url_for
from app.api import api
from app.helpers import handle_request, handle_response
from app.schemas import UserSchema, UrlParamsSchema
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException
from app.models.user_factory import UserFactory


@api.route("/users")
@handle_request(UrlParamsSchema())
@handle_response(UserSchema(many=True))
def get_users(pagination):
    """Return a list of user resources."""
    per_page = pagination.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = pagination.get("next_cursor", {})
    results = dynamodb_repository.get_users(per_page, cursor)
    return results, HTTPStatus.OK


@api.route("/users/<user_id>")
@handle_response(UserSchema())
def get_user(user_id):
    """Return a single user by id."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    return user, HTTPStatus.OK


@api.route("/users", methods=["POST"])
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


@api.route("/users/<user_id>", methods=["PUT"])
@handle_request(UserSchema(partial=["password"]))
@handle_response(None)
def update_user(user_data, user_id):
    """Replace a user resource."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.update_user(user, user_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>", methods=["DELETE"])
@handle_response(None)
def delete_user(user_id):
    """Delete a user resource."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.remove_user(user)
    return {}, HTTPStatus.NO_CONTENT


