"""This module contains view functions for accessing user resources."""


from http import HTTPStatus
from flask import current_app, url_for, request, g, render_template
from app.api import api
from app.helpers import (
    handle_request,
    handle_response,
    handle_file_request,
    upload_to_cdn,
    process_image,
    jwt_required,
    permission_required
)
from app.schemas import (
    UserSchema, 
    UrlParamsSchema, 
    CommunitySchema, 
    NotificationSchema, 
    GroupChatSchema, 
    PrivateChatSchema
)
from app.repositories import dynamodb_repository, s3_repository
from app.repositories.exceptions import DatabaseException, NotFoundException, UniqueConstraintException
from app.models.factories import UserFactory
from app.models import ImageType, TokenType, RolePermission


@api.route("/testing_chat")
def testing_chat():
    return render_template("chat.html")


@api.route("/users")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(UserSchema(many=True))
def get_users(url_params):
    """Return a list of user resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    results = dynamodb_repository.get_users(per_page, cursor)
    return results, HTTPStatus.OK


@api.route("/users/<user_id>/communities")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(CommunitySchema(many=True))
def get_user_communities(url_params, user_id):
    """Return a list of the user's communities."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_user_communities(
            user_id, per_page, cursor=cursor
        )
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(str)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


@api.route("/users/<user_id>")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_response(UserSchema())
def get_user(user_id):
    """Return a single user by id."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    return user, HTTPStatus.OK


@api.route("/users/username/<username>")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_response(UserSchema())
def get_user_by_username(username):
    """Return a single user by username."""
    user = dynamodb_repository.get_user_by_username(username)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    return user, HTTPStatus.OK


@api.route("/users/email/<email>")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_response(UserSchema())
def get_user_by_email(email):
    """Return a single user by email."""
    user = dynamodb_repository.get_user_by_email(email)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    return user, HTTPStatus.OK


@api.route("/users/<user_id>", methods=["PUT"])
@jwt_required(TokenType.ACCESS_TOKEN)
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
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_response(None)
def delete_user(user_id):
    """Delete a user resource."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.remove_user(user)
    profile_photo_id = user.id + "_" + ImageType.USER_PROFILE_PHOTO.name
    cover_photo_id = user.id + "_" + ImageType.USER_COVER_PHOTO.name
    s3_repository.remove(profile_photo_id)
    s3_repository.remove(cover_photo_id)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>/cover_photo", methods=["PUT"])
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_file_request("cover_photo")
@handle_response(None)
def upload_user_cover_photo(file, user_id):
    """Add or replace the user's cover photo."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    image_data = process_image(user.id, s3_repository, file, ImageType.USER_COVER_PHOTO)
    dynamodb_repository.update_user_image(user, image_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>/profile_photo", methods=["PUT"])
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_file_request("profile_photo")
@handle_response(None)
def upload_user_profile_photo(file, user_id):
    """Add or a replace the user's profile photo."""
    user = dynamodb_repository.get_user(user_id)
    if not user:
        return {"error": "User not found"}, HTTPStatus.NOT_FOUND
    image_data = process_image(
        user.id, s3_repository, file, ImageType.USER_PROFILE_PHOTO
    )
    dynamodb_repository.update_user_image(user, image_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>/notifications")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(NotificationSchema(many=True))
def get_user_notifications(url_params, user_id):
    """Return a list of notification resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_user_notifications(
            user_id, per_page, cursor=cursor
        )
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(str)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


# Socket ?
@api.route("/users/<user_id>/notifications/<notification_id>", methods=["PATCH"])
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(NotificationSchema())
@handle_response(None)
def update_user_notification(notification_data, user_id, notification_id):
    """Update a user's notification. The two attributes to updated are whether the
    notification has been read or whether it has been seen.
    """
    notification = dynamodb_repository.get_user_notification(user_id, notification_id)
    if notification.was_seen() and notification_data.get("_seen") is False:
        return (
            {"error": "Cannot change notification status from seen to unseen"},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    if notification.was_read() and notification_data.get("_read") is False:
        return (
            {"error": "Cannot change notification status from read to unread"},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    if notification_data.get("_seen"):
        notification.mark_as_seen()
    elif notification_data.get("_read"):
        notification.mark_as_read()
    dynamodb_repository.add_user_notification(notification)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/users/<user_id>/private_chats")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(PrivateChatSchema(many=True))
def get_user_private_chats(url_params, user_id):
    """Return a list of private chats the user is a part of."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_user_private_chats(user_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK 


# When authentication is added, the current user will have already been fetched from DynamoDB
# and is guaranteed to exist in the database
@api.route("/users/<user_id>/private_chats/<other_user_id>", methods=["PUT"])
@jwt_required(TokenType.ACCESS_TOKEN)
@permission_required(RolePermission.CREATE_PRIVATE_CHAT)
@handle_response(UserSchema())
def create_user_private_chat(user_id, other_user_id):
    """Create a new private chat between two users."""
    # user_id = g.current_user.id
    other_user = dynamodb_repository.get_user(other_user_id)
    if not other_user:
        return {"error": "Other user could not be found"}, HTTPStatus.NOT_FOUND
    try:
        dynamodb_repository.add_private_chat(user_id, other_user_id)
    except UniqueConstraintException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    headers = {"Location": url_for("api.get_user", user_id=other_user_id)}
    return {}, HTTPStatus.OK, headers
    

@api.route("/users/<user_id>/group_chats")
@jwt_required(TokenType.ACCESS_TOKEN)
@handle_request(UrlParamsSchema())
@handle_response(GroupChatSchema(many=True))
def get_user_group_chats(url_params, user_id):
    """Return a list of group chat resources that the user is a member of."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_user_group_chats(user_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK