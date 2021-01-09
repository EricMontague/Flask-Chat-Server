"""This module contains models related to JWTs."""


from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Enum to represent different types of JWTs."""

    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2


@dataclass
class Token:
    """Class to represent a JWT."""

    user_id: str
    raw_jwt: str
    expires_on_date: int # In Unix epoch time format
    issued_at: int # In Unix epoch time format
    token_type: Enum
    is_blacklisted: bool = False
    