"""This package holds classes that implement the repository pattern
and act as an abstraction over persitent storage.
"""


from app.repositories.dynamodb_repository import database_repository
from app.repositories.s3_repository import file_repository