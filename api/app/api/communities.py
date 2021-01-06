"""This module holds view functions for accessing Community resources."""


from http import HTTPStatus
from uuid import uuid4
from flask import url_for, current_app
from app.api import api
from app.helpers import (
    handle_request,
    handle_response,
    handle_file_request,
    process_image
)
from app.schemas import (
    CommunitySchema,
    UrlParamsSchema,
    CommunityUrlParamsSchema,
    UserSchema,
    GroupChatSchema
)
from app.models.factories import CommunityFactory
from app.models import ImageType, GroupChat
from app.repositories import dynamodb_repository, s3_repository
from app.repositories.exceptions import DatabaseException, NotFoundException
from werkzeug.utils import secure_filename


@api.route("/communities")
@handle_request(CommunityUrlParamsSchema())
@handle_response(CommunitySchema(many=True))
def get_communities(url_params):
    """Return a list of community resources."""
    per_page = url_params.pop("per_page", current_app.config["RESULTS_PER_PAGE"])
    kwargs = {}
    if "next_cursor" in kwargs:
        kwargs["cursor"] = kwargs["next_cursor"]
    if "topic" in url_params:
        kwargs["topic"] = url_params["topic"].name
    else:
        kwargs.update(url_params)
    results = dynamodb_repository.get_communities(per_page, **kwargs)
    return results, HTTPStatus.OK


@api.route("/communities/<community_id>")
@handle_response(CommunitySchema())
def get_community(community_id):
    """Get a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    return community, HTTPStatus.OK


@api.route("/communities", methods=["POST"])
@handle_request(CommunitySchema())
@handle_response(CommunitySchema())
def create_community(community_data):
    """Create a new community resource."""
    community = CommunityFactory.create_community(community_data)
    try:
        dynamodb_repository.add_community(community, "RandomUserIdForNow")
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    headers = {"Location": url_for("api.get_community", community_id=community.id)}
    return (community, HTTPStatus.CREATED, headers)


@api.route("/communities/<community_id>", methods=["PUT"])
@handle_request(CommunitySchema())
@handle_response(None)
def update_community(community_data, community_id):
    """Replace a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.update_community(community, community_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>/members")
@handle_request(UrlParamsSchema())
@handle_response(UserSchema(many=True))
def get_community_members(url_params, community_id):
    """Return a list of users that belong to the given community."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_community_members(community_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


# What method should this be?
@api.route("/communities/<community_id>/members/<user_id>", methods=["PUT"])
@handle_response(None)
def join_community(community_id, user_id):
    """Add a new member to a community."""
    try:
        dynamodb_repository.add_community_member(community_id, user_id)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return {}, HTTPStatus.OK


# What method should this be?
@api.route("/communities/<community_id>/members/<user_id>", methods=["DELETE"])
@handle_response(None)
def leave_community(community_id, user_id):
    try:
        dynamodb_repository.remove_community_member(community_id, user_id)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>/cover_photo", methods=["PUT"])
@handle_file_request("cover_photo")
@handle_response(None)
def upload_community_cover_photo(file, community_id):
    """Add or replace the community's cover photo."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    image_data = process_image(community.id, s3_repository, file, ImageType.COMMUNITY_COVER_PHOTO)
    dynamodb_repository.update_community_image(community, image_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>/profile_photo", methods=["PUT"])
@handle_file_request("profile_photo")
@handle_response(None)
def upload_community_profile_photo(file, community_id):
    """Add or a replace the community's profile photo."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    image_data = process_image(community.id, s3_repository, file, ImageType.COMMUNITY_PROFILE_PHOTO)
    dynamodb_repository.update_community_image(community, image_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>/group_chats")
@handle_request(UrlParamsSchema())
@handle_response(GroupChatSchema(many=True))
def get_community_group_chats(url_params, community_id):
    """Return a list of group chat resources in the given community."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_community_group_chats(community_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


@api.route("/communities/<community_id>/group_chats", methods=["POST"])
@handle_request(GroupChatSchema())
@handle_response(GroupChatSchema())
def create_community_group_chat(group_chat_data, community_id):
    """Create a new group chat resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    user_id = "AWTT"
    # user_id = g.current_user.id
    group_chat = GroupChat(uuid4().hex, community_id, group_chat_data["name"], group_chat_data["description"])
    dynamodb_repository.add_group_chat(user_id, community_id, group_chat)
    headers = {
        "Location": url_for(
            "api.get_community_group_chat", community_id=community_id, group_chat_id=group_chat.id
        )
    }
    return (group_chat, HTTPStatus.CREATED, headers)


@api.route("/communities/<community_id>/group_chats/<group_chat_id>")
@handle_response(GroupChatSchema())
def get_community_group_chat(community_id, group_chat_id):
    """Return a group chat resource."""
    group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
    if not group_chat:
        return {"error": "Group chat not found"}, HTTPStatus.NOT_FOUND
    return group_chat, HTTPStatus.OK


@api.route("/communities/<community_id>/group_chats/<group_chat_id>", methods=["PUT"])
@handle_request(GroupChatSchema())
@handle_response(None)
def update_community_group_chat(group_chat_data, community_id, group_chat_id):
    """Update a group chat resource."""
    group_chat = dynamodb_repository.get_group_chat(community_id, group_chat_id)
    if not group_chat:
        return {"error": "Group chat not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.update_group_chat(group_chat, group_chat_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("communities/<community_id>/group_chats/<group_chat_id>/members")
@handle_request(UrlParamsSchema())
@handle_response(UserSchema(many=True))
def get_community_group_chat_members(url_params,community_id, group_chat_id):
    """Return a list of group chat members."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor")
    try:
        results = dynamodb_repository.get_group_chat_members(community_id, group_chat_id, per_page, cursor=cursor)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK
