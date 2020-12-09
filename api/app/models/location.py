"""This module contains the location model."""


from dataclasses import dataclass


@dataclass
class Location:
    """Class to represent a location."""

    city: str
    state: str
    country: str

    def to_map(self):
        """Return a location as represented in DynamoDB."""
        return {
            "M": {
                "city": {"S": self.city},
                "state": {"S": self.state},
                "country": {"S": self.country}
            }
        }
        
