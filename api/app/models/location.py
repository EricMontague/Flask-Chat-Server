"""This module contains the location model."""


from dataclasses import dataclass


@dataclass
class Location:
    """Class to represent a location."""

    city: str
    state: str
    country: str

