"""This module holds view functions for accessing Community resources."""


from http import HTTPStatus
from flask import url_for, current_app
from app.api import api
from app.helpers.decorators import handle_request, handle_response
from app.schemas import CommunitySchema, UrlParamsSchema, CommunityTopicSchema
from app.models.factories import CommunityFactory
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException


@api.route("/communities")
@handle_request(UrlParamsSchema())
@handle_response(CommunitySchema(many=True))
def get_communities(url_params):
    """Return a list of community resources."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor", {})
    results = dynamodb_repository.get_communities(per_page, cursor)
    return results, HTTPStatus.OK


@api.route("/communities")
@handle_request(CommunityTopicSchema())
@handle_response(CommunitySchema(many=True))
def get_communities_by_topic(url_params):
    """Return a list of communities resources by topic."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    cursor = url_params.get("next_cursor", {})
    topic = url_params["topic"]
    results = dynamodb_repository.get_communities_by_topic(per_page, topic.name, cursor)
    return results, HTTPStatus.OK


@api.route("/communities")
def get_communities_by_location():
    """Return a list of communities resources by location."""
    pass


@api.route("/communities/<community_id>/members")
def get_community_members():
    pass


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


@api.route("/communities/<community_id>", methods=["DELETE"])
@handle_response(None)
def delete_community(community_id):
    """Delete a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.remove_community(community)
    return {}, HTTPStatus.NO_CONTENT


# What method should this be?
@api.route("/communities/<community_id>", methods=["POST"])
def join_community():
    pass


# What method should this be?
@api.route("/communities/<community_id>", methods=["DELETE"])
def leave_community():
    pass
