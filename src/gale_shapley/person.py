"""Person module.
Creates the units in the matching environment.
Person class is also the base class for Proposer and Responder classes."""

from __future__ import annotations

import logging


class Person:
    """Person class.
    Base class for Proposer and Responder."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Person class.

        Args:
            name (str): Name of the person
            side (str): Side of the person
        """
        self.name = name
        self.side = side
        self.preferences: tuple[Proposer | Responder, ...] = ()
        self.match: Proposer | Responder | None = None

    def __repr__(self) -> str:
        """Returns a string representation of the person."""
        match self.match:
            case None:
                return f"Name: {self.name}, Side: {self.side}, Match: None"
            case _:
                return f"Name: {self.name}, Side: {self.side}, Match: {self.match.name}"

    def is_acceptable(self, person: Proposer | Responder) -> bool:
        """Checks if person is acceptable to self, self is acceptable.

        Args:
            person (Proposer | Responder)

        Raises:
            ValueError: Raises ValueError if either self or person is not in preferences

        Returns:
            bool: Returns True if person is acceptable to self, False otherwise
        """
        if self == person:
            return True
        if person in self.preferences:
            return self.preferences.index(person) <= self.preferences.index(self)
        raise ValueError(f"Either {self} or {person} is not in preferences.")

    def print_preferences(self) -> None:
        """Prints the preferences of the person, * indicates acceptable."""
        logging.info(
            f"{self.name} has the following preferences, * indicates acceptable:"
        )
        offset_one: int = len(str(len(self.preferences)))
        offset_two: int = max(len(person.name) for person in self.preferences)
        for i, person in enumerate(self.preferences, start=1):
            logging.info(
                f"{i}.{'':{offset_one - len(str(i)) + 1}}{person.name:<{offset_two + 1}}{'*' if self.is_acceptable(person) else ''}"
            )

    @property
    def is_matched(self) -> bool:
        """Returns True if the person is matched to someone or self, False if match is None.

        Returns:
            bool
        """
        return bool(self.match)

    @is_matched.setter
    def is_matched(self, value: bool) -> None:
        """Setter method for is_matched property.

        Args:
            value (bool): If False, sets match to None. If True, raises ValueError

        Raises:
            ValueError: Raises ValueError if value is True, can only be set to False
        """
        match value:
            case False:
                self.match = None
            case True:
                raise ValueError("is_matched attribute can only be set to False")


class Proposer(Person):
    """Proposer class, subclass of Person."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Proposer class, last_proposal is the last person that proposer proposed to.

        Args:
            name (str): Name of the person for super constructor
            side (str): Side of the person for super constructor
        """
        super().__init__(name, side)
        self.last_proposal: Responder | Proposer | None = None

    @property
    def acceptable_to_propose(self) -> tuple[Responder | Proposer, ...]:
        """Returns a tuple of acceptable responders to propose to.

        Returns:
            tuple[Responder | Proposer, ...]: tuple of acceptable to propose to
        """
        return tuple(filter(self.is_acceptable, self.preferences))

    @property
    def next_proposal(self) -> Responder | Proposer:
        """Returns the next acceptable responder to propose to, or self if no acceptable responders.

        Returns:
            Responder | Proposer
        """
        try:
            match self.last_proposal:
                case None:
                    return self.acceptable_to_propose[0]
                case _:
                    return self.acceptable_to_propose[
                        self.acceptable_to_propose.index(self.last_proposal) + 1
                    ]
        except IndexError:
            return self

    def propose(self) -> None:
        """Proposes to the next acceptable responder. If self is next, sets match to self. Updates last_proposal."""
        match self.next_proposal:
            case Proposer():  # meaning self is next
                self.match = self
            case responder:
                responder.current_proposals.append(self)
        self.last_proposal = self.next_proposal


class Responder(Person):
    """Responder class, subclass of Person."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Responder class.

        Args:
            name (str): Name of the person for super constructor
            side (str): Side of the person for super constructor
        """
        super().__init__(name, side)
        self.current_proposals: list[Proposer] = []

    @property
    def awaiting_to_respond(self) -> bool:
        """Returns True if current_proposals is not empty, False otherwise.

        Returns:
            bool
        """
        return bool(self.current_proposals)

    @property
    def acceptable_proposals(self) -> list[Proposer]:
        """Returns a list of acceptable proposals among the current proposals.

        Returns:
            list[Proposer]
        """
        return list(filter(self.is_acceptable, self.current_proposals))

    def _most_preferred(self, proposals: list[Proposer]) -> Proposer:
        """Returns most preferred of the list.

        Args:
            proposals (list[Proposer]): List of proposals to find most preferred from

        Raises:
            ValueError: If preferences or proposals is empty, or proposal not in preferences

        Returns:
            Proposer: Most preferred proposer
        """
        if (
            bool(self.preferences)
            and bool(proposals)
            and all(proposal in self.preferences for proposal in proposals)
        ):
            return min(proposals, key=self.preferences.index)
        raise ValueError(
            "Either preferences or proposals is empty, or one of the proposals is not in preferences."
        )

    def respond(self) -> None:
        """Responds to proposals and clears the current_proposals."""
        if bool(self.acceptable_proposals):
            match self.match:
                case Proposer() as current_match:
                    new_match = self._most_preferred(
                        self.acceptable_proposals + [current_match]
                    )
                    if new_match != current_match:
                        current_match.is_matched = False
                        self.match = new_match
                        new_match.match = self
                case _:
                    new_match = self._most_preferred(self.acceptable_proposals)
                    self.match = new_match
                    new_match.match = self
        self.current_proposals = []
