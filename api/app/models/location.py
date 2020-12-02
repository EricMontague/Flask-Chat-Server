"""This module contains the location model."""


from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Class to represent a location."""

    city: str
    state: str
    country: str

    def to_dict(self):
        """Return a dictionary representation of a location."""
        return {
            "city": self.city,
            "state": self.state,
            "country": self.country
        }
        
