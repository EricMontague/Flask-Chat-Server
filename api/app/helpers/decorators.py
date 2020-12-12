"""This module contains decorators to be used through the application."""


import functools
from http import HTTPStatus
from flask import request
from marshmallow import ValidationError


def handle_request(schema):
    """Decorator to handle deserializing the JSON body
    of requests to API routes.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            request_data = request.json
            if not request_data:
                return (
                    {"message": "Missing JSON Body in request"},
                    HTTPStatus.BAD_REQUEST,
                )
            try:
                model_dict = schema.load(request_data)
            except ValidationError as err:
                return {"errors": err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY
            return view_func(model_dict, *args, **kwargs)

        return wrapper

    return decorator


def handle_response(schema):
    """Decorator to handle serializing models to JSON
    responses for API routes.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            model_or_models, http_status_code = view_func(*args, **kwargs)
            return schema.dumps(model_or_models), http_status_code

        return wrapper

    return decorator


def handle_query_params(view_func):
    """Decorator to handle parsing query parameters sent
    during a request to the api. It handles pagination, filtering, and sorting 
    for collections. The expected response from the decorated route is a
    an object that implements the AbstractDatabaseRepository interface."""

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        params = request.args
        return view_func(params, *args, **kwargs)

    return wrapper
