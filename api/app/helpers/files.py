"""This module contains helper functions for working with files."""


import io
import imghdr
from uuid import uuid4
from PIL import Image
from werkzeug.utils import secure_filename


def is_allowed_file_extension(filename, extensions):
    """Return True if the extension of the given file is in the set of
    allowed file extensions.
    """
    if "." not in filename:
        return False
    file_extension = filename.lower().split(".")[-1]
    return file_extension in extensions


def upload_to_cdn(file, filename):
    """Pretend that this function handles uploading
    the given file to a CDN and returns the CDN url.
    """
    return "https://mycdn.com/us-east/" + filename


def process_image(user_id, repo, file, image_type):
    """Upload the given image to S3 and return the
    data necessary to create an Image model.
    """
    filename = secure_filename(file.filename)
    image_bytes = io.BytesIO(file.read())
    image_id = user_id + "_" + image_type.name
    repo.add(image_id, image_bytes.read())
    image_bytes.seek(0)
    
    pillow_image = Image.open(image_bytes)
    
    image_data = {
        "id": image_id,
        "height": pillow_image.height,
        "width": pillow_image.width,
        "url": upload_to_cdn(image_bytes, filename),
        "image_type": image_type
    }
    return image_data


def validate_image(file):
    """Validate that the given file is an image and
    return its extension if it is.
    """
    header = file.read(512)
    file.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
