from __future__ import annotations

from typing import Union


class Person:
    def __init__(self, name: str, side: str) -> None:
        self.name = name
        self.side = side
        self.preferences: Union[tuple[Person], None] = None
        self.match: Union[Person, None] = None

    def __repr__(self) -> str:
        return f"Name: {self.name}, Side: {self.side}, Match: {self.match}"

    def _is_acceptable(self, person: Person) -> bool:
        return self.preferences.index(person) < self.preferences.index(self)

    def print_preferences(self) -> None:
        print(f"{self.name} has the following preferences, * indicates acceptable:")
        for i, person in enumerate(self.preferences):
            print(
                f"{i + 1}. {person.name} {'*' if self._is_acceptable(person) else ''}"
            )

    @property
    def is_matched(self) -> bool:
        return self.match is not None

    @is_matched.setter
    def is_matched(self, value: bool) -> None:
        if not value:
            self.match = None
        else:
            raise ValueError("is_matched attribute can only be set to False")
