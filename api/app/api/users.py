"""This module contains view functions for accessing user resources."""


from http import HTTPStatus
from flask import current_app
from app.api import api
from app.helpers import handle_request, handle_response
from app.schemas import UserSchema
from app.repositories import dynamodb_repository
from app.models.user_factory import UserFactory
from pprint import pprint


@api.route("/users/<user_id>")
@handle_response(UserSchema())
def get_user(user_id):
    """Return a single user by id."""
    return dynamodb_repository.get_user(user_id), HTTPStatus.OK


@api.route("/users", methods=["POST"])
@handle_request(UserSchema())
@handle_response(UserSchema())
def create_user(user_data):
    """Create a new user resource."""
    user = UserFactory.create_user(user_data)
    response = dynamodb_repository.add_user(user)
    pprint(response)
    return user, HTTPStatus.CREATED

