"""Person module."""
from __future__ import annotations

from typing import Union


class Person:
    def __init__(self, name: str, side: str) -> None:
        """Constructor for Person class.

        Args:
            name (str): name of the person, parsed from config.yaml
            side (str): side of the person, parsed from config.yaml
        """
        self.name = name
        self.side = side
        self.preferences: Union[tuple[Person], None] = None
        self.match: Union[Person, None] = None

    def __repr__(self) -> str:
        return f"Name: {self.name}, Side: {self.side}, Match: {self.match}"

    def _is_acceptable(
        self, person: Person
    ) -> bool:  # returns True if person is acceptable, self is not acceptable
        return self.preferences.index(person) < self.preferences.index(self)

    def print_preferences(self) -> None:
        """Prints the preferences of the person, * indicates acceptable."""
        print(f"{self.name} has the following preferences, * indicates acceptable:")
        for i, person in enumerate(self.preferences):
            print(
                f"{i + 1}. {person.name} {'*' if self._is_acceptable(person) else ''}"
            )

    @property
    def is_matched(self) -> bool:
        """Returns True if the person is matched to someone or self, False if match is None.

        Returns:
            bool:
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
