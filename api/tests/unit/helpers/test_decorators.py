"""This file contains tests for decorators used in the application."""


import pytest
from app.helpers.decorators import (
    handle_request,
    handle_get_request,
    handle_post_and_put_requests,
)
from marshmallow import ValidationError


def test_handle_get_request_invalid_parameters_returns_errors(fake_error_schema_class):
    """Test that when a schema is passed in and its load method raises a ValidationError
    that a dictionary with the error is returned.
    """
    fake_error_schema = fake_error_schema_class()
    url_params = {"next": "next cursor", "per_page": 12}
    error, http_status_code = handle_get_request(fake_error_schema, url_params)
    assert "error" in error
    assert http_status_code == 422


def test_handle_get_request_valid_parameters_returns_data(fake_data_schema):
    """Test that when the load method of a schema doesn't throw an error,
    that data is returned.
    """
    url_params = {"next": "next cursor", "per_page": 12}
    results = handle_get_request(fake_data_schema, url_params)
    assert "next" in results
    assert "per_page" in results


def test_handle_post_put_request_invalid_parameters_schema_error(fake_error_schema_class):
    """Test that when a schema is passed in and its load method raises a ValidationError
    caused by a schema level error that a dictionary with that error is returned.
    """
    fake_error_schema = fake_error_schema_class()
    fake_data = {"username": "Brad12", "age": 12}
    error, http_status_code = handle_post_and_put_requests(fake_error_schema, fake_data)
    assert "error" in error
    assert http_status_code == 422


def test_handle_post_put_request_invalid_parameters_field_errors(fake_error_schema_class):
    """Test that when a schema is passed in and its load method raises a ValidationError
    caused by a field level validator that a dictionary with that error is returned.
    """
    fake_error_schema = fake_error_schema_class("random_field")
    fake_data = {"username": "Brad12", "age": 12}
    errors, http_status_code = handle_post_and_put_requests(fake_error_schema, fake_data)
    assert "errors" in errors
    assert http_status_code == 422


def test_handle_post_put_request_valid_parameters_field_errors(fake_data_schema):
    """Test that when the load method of a schema doesn't throw an error,
    that data is returned.
    """
    fake_data = {"username": "Brad12", "age": 12}
    results = handle_get_request(fake_data_schema, fake_data)
    assert "username" in results
    assert "age" in results


def test_handle_request_decorator_get_request():
    pass

def test_handle_request_decoraotr_post_request():
    pass

def test_handle_request_decorator_put_request():
    pass

def test_handle_request_decorator_post_request_no_json_body_returns_error():
    pass

def test_handle_request_decorator_put_request_no_json_body_returns_error():
    pass

def test_handle_request_decorator_error_with_deserialization():
    pass