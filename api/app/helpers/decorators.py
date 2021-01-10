"""This module contains decorators to be used through the application."""


import functools
from http import HTTPStatus
from flask import request, make_response, current_app, g
from marshmallow import ValidationError
from app.helpers.files import is_allowed_file_extension
from app.repositories import dynamodb_repository
from app.repositories.exceptions import NotFoundException, DatabaseException
from app.models import User, TokenType


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
            api_response.headers["Content-Type"] = "application/json"
            return api_response

        return wrapper

    return decorator


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


def is_blacklisted(decoded_token, token_type):
    """Return True if the given token is blacklisted."""
    token = dynamodb_repository.get_token(decoded_token.raw_jwt, token_type)
    if not token:
        return True
    return token.is_blacklisted


def jwt_required(token_type):
    """Decorator used to protect routes that require an authenticated user."""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth_headers = request.headers.get("Authorization")
            if not auth_headers:
                return (
                    {"error": "Missing token in authorization headers"},
                    HTTPStatus.UNAUTHORIZED,
                )
            auth_type = "Bearer"
            bearer_start_index = auth_headers.find(auth_type)
            raw_jwt = auth_headers[bearer_start_index + len(auth_type) :].strip()
            if not raw_jwt:
                return (
                    {"error": "Missing token in authorization headers"},
                    HTTPStatus.UNAUTHORIZED,
                )
            decoded_token = User.decode_token(raw_jwt, current_app.config["SECRET_KEY"])
            if not decoded_token:
                return {"error": f"Invalid {token_type.name.replace('_', ' ').lower()}"}, HTTPStatus.UNAUTHORIZED

            if decoded_token.token_type != token_type:
                return {"error": "Incorrect token type provided"}, HTTPStatus.UNAUTHORIZED

            if is_blacklisted(decoded_token, token_type):
                return {"error": f"Invalid {token_type.name.replace('_', ' ').lower()}"}, HTTPStatus.UNAUTHORIZED
            current_user = dynamodb_repository.get_user(decoded_token.user_id)
            if not current_user:
                return {"error": "User not found"}
            g.current_user = current_user
            g.decoded_token = decoded_token
            return func(*args, **kwargs)

        return wrapper
    return decorator


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

