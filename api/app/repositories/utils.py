"""This module utility functions for the repository layer"""


import json
import base64
import hashlib


def encode_cursor(value):
    """Return the value as a base 64 encoded JSON string."""
    encoded_json_string = json.dumps(value).encode("utf-8")
    return base64.b64encode(encoded_json_string).decode("utf-8")


def decode_cursor(value):
    """Given a base 64 encoded string, convert and return
    it to its original python primitive value.
    """
    byte_string = base64.b64decode(value)
    return json.loads(byte_string.decode("utf-8"))


def encode_file_contents(file_contents):
    """Create an MD5 hash of the file contents and then return
    the base64 encoded string of the md5 hash.
    """
    md = hashlib.md5(file_contents).digest()
    contents_md5 = base64.b64encode(md).decode("utf-8")
    return contents_md5