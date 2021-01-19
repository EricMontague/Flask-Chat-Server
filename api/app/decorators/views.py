"""This module contains decorators to be used to handle arguments sent to the
server endpoints or socketio event handlers
"""


import functools
import json
from http import HTTPStatus
from flask import request, make_response, current_app
from flask_socketio import emit
from marshmallow import ValidationError


def handle_get_request(schema, url_params):
    """Validate query string parameters sent on a GET request."""
    try:
        return schema.load(url_params)
    except ValidationError as err:
        return {"error": err.messages["_schema"][0]}


def handle_post_or_put_request(schema, json_data):
    """Validate and return deserialized JSON body of POST and PUT requests."""
    try:
        return schema.load(json_data)
    except ValidationError as err:
        if "_schema" in err.messages:
            return {"error": err.messages["_schema"]}
        return {"errors": err.messages}


def handle_request(schema):
    """Decorator to handle deserializing the JSON body
    of requests to API routes as well as Url parameters.
    Meant to only be used on GET, PUT, and POST requests
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                view_argument = handle_get_request(schema, request.args)
            elif request.method in {"POST", "PUT", "PATCH"}:
                if not request.json:
                    return (
                        {"error": "Missing JSON Body in request"},
                        HTTPStatus.BAD_REQUEST,
                    )
                view_argument = handle_post_or_put_request(schema, request.json)
            if "error" in view_argument or "errors" in view_argument:
                return view_argument, HTTPStatus.UNPROCESSABLE_ENTITY
            return func(view_argument, *args, **kwargs)

        return wrapper

    return decorator


def serialize_model_or_models(results, schema):
    """Serialize all models present in a dictionary returned
    by a view function and update the dictionary with new
    keys to reflect the model or models' name
    """
    for key in results:
        if key == "model":
            model = results.pop(key)
            results[schema.RESOURCE_NAME] = schema.dump(model)
        elif key == "models":
            models = results.pop(key)
            results[schema.COLLECTION_NAME] = schema.dump(models)


def handle_serialization(results, schema, http_status_code):
    """Serialize the return arguments from a view function and use
    them to create and return a Flask response object.
    """
    if isinstance(results, list):  # attempt to serialize list
        serialized_results = schema.dump(results)
        api_response = make_response(serialized_results or results, http_status_code)
    elif isinstance(results, dict):  # attempt to serialize every item in dict
        serialize_model_or_models(results, schema)
        api_response = make_response(results, http_status_code)
    else:  # assume it's a model
        api_response = make_response(schema.dump(results), http_status_code)
    return api_response


def not_require_serialization(schema, results):
    """Return True if the response from the view function doesn't
    need to be serialized by a marshmallow schema.
    """
    if not schema or isinstance(results, str):
        return True

    if isinstance(results, dict) and (
        not results or "error" in results or "errors" in results
    ):
        return True
    return False


def handle_response(schema):
    """Decorator to handle serializing models to JSON
    responses for API routes.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            view_response = view_func(*args, **kwargs)
            # view_response is a tuple in the form of (results, http_status_code, headers)
            # or (results, http_status_code)
            results = view_response[0]
            http_status_code = view_response[1]

            if not_require_serialization(schema, results):
                api_response = make_response(results, http_status_code)
            else:
                api_response = handle_serialization(results, schema, http_status_code)
            if len(view_response) == 3:  # extra headers are included in the response
                api_response.headers.extend(view_response[2])
            return api_response

        return wrapper

    return decorator


def is_allowed_file_extension(filename, extensions):
    """Return True if the extension of the given file is in the set of
    allowed file extensions.
    """
    if "." not in filename:
        return False
    file_extension = filename.lower().split(".")[-1]
    return file_extension in extensions


def handle_file_request(expected_filename):
    """Decorator to handle uploads of files."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            file = request.files.get(expected_filename)
            if file is None:
                return (
                    {"error": "Could not find an image file in the request"},
                    HTTPStatus.BAD_REQUEST,
                )
            if file.filename == "":
                return {"error": "No selected file"}, HTTPStatus.BAD_REQUEST
            if not is_allowed_file_extension(
                file.filename, current_app.config["ALLOWED_FILE_EXTENSIONS"]
            ):
                return (
                    {
                        "message": f"File extension not allowed. Valid extensions include: {list(current_app.config['ALLOWED_FILE_EXTENSIONS'])}"
                    },
                    HTTPStatus.BAD_REQUEST,
                )
            return func(file, *args, **kwargs)

        return wrapper

    return decorator


def socketio_handle_arguments(schema):
    """Decorator to validate arguments sent to Socketio event handlers."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = request.event["args"][0]
            try:
                deserialized_data = schema.loads(data)
            except ValidationError as err:
                emit("error", json.dumps({"error": err.messages}))
            else:
                return func(deserialized_data, schema)

        return wrapper

    return decorator

