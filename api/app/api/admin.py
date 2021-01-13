"""This module contains routes only accessible by users with admin priveleges."""


from http import HTTPStatus
from flask import request
from app.api import api
from app.repositories import dynamodb_repository
from app.decorators.request_response import handle_request, handle_response
from app.decorators.auth import admin_required
from app.models import RolePermission
from app.models.role import PermissionsError
from app.schemas import RoleSchema


@api.route("/users/<user_id>/role")
@admin_required
@handle_response(RoleSchema())
def get_user_role(user_id):
    """Return a user's role and permissions"""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    return user.role, HTTPStatus.OK


@api.route("/users/<user_id>/permissions", methods=["PUT"])
@admin_required
@handle_request(RoleSchema())
def update_user_permissions(role_data, user_id):
    """Update permissions for a user."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    updated_user_data = {
        "role": {
            "permissions": role_data.get("_permissions", [])
        }
    }
    
    try:
        dynamodb_repository.update_user(user, updated_user_data)
    except PermissionsError as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return {}, HTTPStatus.NO_CONTENT
    

@api.route("/users/<user_id>/ban", methods=["PUT"])
@admin_required
def ban_user(user_id):
    """Ban a user from accessing the api."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    if user.is_banned:
        return {"error": "User is already banned"}, HTTPStatus.BAD_REQUEST
    dynamodb_repository.update_user(user, {"is_banned": True})
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>/ban", methods=["DELETE"])
@admin_required
def unban_user(user_id):
    """Unban a user from accessing the api."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    if not user.is_banned:
        return {"error": "User is not currently banned"}, HTTPStatus.BAD_REQUEST
    dynamodb_repository.update_user(user, {"is_banned": False})
    return {}, HTTPStatus.NO_CONTENT