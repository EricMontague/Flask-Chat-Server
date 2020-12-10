"""This module contains view functions for accessing user resources."""


from app.api import api
from app.helpers import handle_request, handle_response
from app.schemas import UserSchema
from app.repositories import dynamodb_repository


@handle_response(UserSchema())
@api.route("/users/<int:user_id>")
def get_user(user_id):
    """Return a single user by id."""
    return dynamodb_repository.get_user(user_id)


@handle_response(UserSchema(many=True))
@api.route("/users")
def get_users():
    """Return a collection of user resources."""
    return dynamodb_repository.get_users()
