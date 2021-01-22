"""This module contains decorators that abstract away common patterns for endpoints."""


import functools
from http import HTTPStatus
from app.repositories import database_repository
from app.repositories.exceptions import NotFoundException, DatabaseException


def get_collection(view_func):
    """Decorator to be used with a view function returns a collection of resources."""

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        repo_method, url_params = view_func(*args, **kwargs)
        return (
            repo_method(url_params["per_page"], cursor=url_params["cursor"]),
            HTTPStatus.OK,
        )

    return wrapper


def get_subcollection(view_func):
    """Decorator to be used with a view function that returns a subcollection."""

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        repo_method, repo_method_args, url_params = view_func(*args, **kwargs)
        try:
            results = repo_method(
                *repo_method_args, url_params["per_page"], cursor=url_params["cursor"]
            )
        except NotFoundException as err:
            return {"error": str(err)}, HTTPStatus.NOT_FOUND
        except DatabaseException as err:
            return {"error": str(err)}, HTTPStatus.BAD_REQUEST
        return results, HTTPStatus.OK

    return wrapper


def get_resource(not_found_message):
    """Decorator to be used with a view function that returns a single resource."""

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            resource = view_func(*args, **kwargs)
            if not resource:
                return {"error": not_found_message}, HTTPStatus.NOT_FOUND
            return resource, HTTPStatus.OK

        return wrapper

    return decorator


def create_resource(view_func):
    """Decorator to be used with a view function that creates a resource."""

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        repo_method, new_resource, new_resource_url = view_func(*args, **kwargs)
        try:
            repo_method(new_resource)
        except DatabaseException as err:
            return {"error": str(err)}, HTTPStatus.BAD_REQUEST
        headers = {"Location": new_resource_url}
        return new_resource, HTTPStatus.CREATED, headers

    return wrapper


def update_resource(not_found_message):
    """Decorator to be used with a view function that updates resources."""

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            resource, updated_resource_data, repo_method = view_func(*args, **kwargs)
            if not resource:
                return {"error": not_found_message}, HTTPStatus.NOT_FOUND
            repo_method(resource, updated_resource_data)
            return {}, HTTPStatus.NO_CONTENT

        return wrapper

    return decorator


def delete_resource(not_found_message):
    """Decorator to be used with a view function that deletes resources."""

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            resource, repo_method = view_func(*args, **kwargs)
            if not resource:
                return {"error": not_found_message}, HTTPStatus.NOT_FOUND
            repo_method(resource)
            return {}, HTTPStatus.NO_CONTENT

        return wrapper

    return decorator

