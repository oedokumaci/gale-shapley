"""Person module."""

from __future__ import annotations

from typing import Union


class Person:
    """Person class. Represents a side in the matching environment. This class is also the base class for Proposer and Responder."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Person class.

        Args:
            name (str): name of the person, parsed from config.yaml
            side (str): side of the person, parsed from config.yaml
        """
        self.name = name
        self.side = side
        self.preferences: Union[tuple[Person, ...], None] = None
        self.match: Union[Person, None] = None

    def __repr__(self) -> str:
        return f"Name: {self.name}, Side: {self.side}, Match: {self.match}"

    @property
    def better_than_match(self) -> tuple[Person, ...]:
        """Returns a tuple of Persons that are preferred to the match."""
        if self.is_matched and self.preferences is not None:
            return self.preferences[: self.preferences.index(self.match)]
        return tuple()

    def is_acceptable(self, person: Person) -> bool:
        """Checks if person is acceptable to self. Self is acceptable.

        Args:
            person (Person)

        Returns:
            bool: Returns True if person is acceptable to self, False otherwise
        """
        if self.preferences is not None:
            return self.preferences.index(person) <= self.preferences.index(self)
        else:
            raise ValueError("Preferences are not set yet.")

    def print_preferences(self) -> None:
        """Prints the preferences of the person, * indicates acceptable."""
        if self.preferences is not None:
            print(f"{self.name} has the following preferences, * indicates acceptable:")
            for i, person in enumerate(self.preferences):
                print(
                    f"{i + 1}. {person.name} {'*' if self.is_acceptable(person) else ''}"
                )
        else:
            print(f"Preferences for {self.name} are not set yet.")

    @property
    def is_matched(self) -> bool:
        """Returns True if the person is matched to someone or self, False if match is None.

        Returns:
            bool
        """
        return self.match is not None

    @is_matched.setter
    def is_matched(self, value: bool) -> None:
        """Setter method for is_matched property.

        Args:
            value (bool): if False, sets match to None, if True, raises ValueError

        Raises:
            ValueError: Raises ValueError if value is True, can only be set to False
        """
        if not value:
            self.match = None
        else:
            raise ValueError("is_matched attribute can only be set to False")