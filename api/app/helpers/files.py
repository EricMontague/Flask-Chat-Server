"""This module contains helper functions for working with files."""



def is_allowed_file_extension(filename, extensions):
    """Return True if the extension of the given file is in the set of
    allowed file extensions.
    """
    if "." not in filename:
        return False
    file_extension = filename.lower().split(".")[-1]
    return file_extension in extensions