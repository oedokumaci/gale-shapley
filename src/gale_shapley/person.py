"""Person module. Represents a side in the matching environment.
Person class is also the base class for Proposer and Responder classes."""

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
        self.preferences: Union[tuple[Union[Proposer, Responder], ...], None] = None
        self.match: Union[Proposer, Responder, None] = None

    def __repr__(self) -> str:
        return f"Name: {self.name}, Side: {self.side}, Match: {self.match}"

    def is_acceptable(self, person: Union[Proposer, Responder]) -> bool:
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


class Proposer(Person):
    """Proposer class, subclass of Person."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Proposer class.

        Args:
            name (str): name of the person for super constructor, parsed from config.yaml
            side (str): side of the person for super constructor, parsed from config.yaml
        """
        super().__init__(name, side)
        self.last_proposal: Union[
            Responder, Proposer, None
        ] = None  # last person that proposer proposed to

    @property
    def acceptable_to_propose(self) -> tuple[Union[Responder, Proposer], ...]:
        """Returns a tuple of acceptable responders to propose to.

        Returns:
            tuple[Union[Responder, Proposer], ...]: tuple of acceptable responders
        """
        if self.preferences is not None:
            return tuple(
                (
                    responder_or_self
                    for responder_or_self in self.preferences
                    if self.is_acceptable(responder_or_self)
                )
            )
        else:
            raise ValueError("Preferences are not set.")

    @property
    def next_proposal(self) -> Union[Responder, Proposer]:
        """Returns the next acceptable responder to propose to, or self if no acceptable responders.

        Returns:
            Union[Responder, Proposer]:
        """
        try:
            if self.last_proposal is None:
                return self.acceptable_to_propose[0]
            return self.acceptable_to_propose[
                self.acceptable_to_propose.index(self.last_proposal) + 1
            ]
        except IndexError:
            return self

    def propose(self) -> None:
        """Proposes to the next acceptable responder. If self is next, sets match to self. Updates last_proposal."""
        if isinstance(
            self.next_proposal, Proposer
        ):  # meaning self is next, doing this to pass type check
            self.match = self
        else:
            if self.next_proposal.current_proposals is not None:
                self.next_proposal.current_proposals.append(self)
            else:
                self.next_proposal.current_proposals = [self]
        self.last_proposal = self.next_proposal


class Responder(Person):
    """Responder class, subclass of Person."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Responder class.

        Args:
            name (str): name of the person for super constructor, parsed from config.yaml
            side (str): side of the person for super constructor, parsed from config.yaml
        """
        super().__init__(name, side)
        self.current_proposals: Union[
            list[Proposer], None
        ] = None  # list of current proposals

    @property
    def awaiting_to_respond(self) -> bool:
        """Returns True if current_proposals is not None, False otherwise.

        Returns:
            bool:
        """
        return self.current_proposals is not None

    @property
    def acceptable_proposals(self) -> list[Proposer]:
        """Returns a list of acceptable proposals.

        Returns:
            list[Proposer]:
        """
        if self.current_proposals is not None:
            return [
                proposer
                for proposer in self.current_proposals
                if self.is_acceptable(proposer)
            ]
        return []

    def _most_preferred(
        self, proposals: list[Proposer]
    ) -> Proposer:  # returns most preferred of the list
        if self.preferences is not None:
            return min(proposals, key=self.preferences.index)
        else:
            raise ValueError("Preferences are not set yet.")

    def respond(self) -> None:
        """Responds to proposals and updates current_proposals to None."""
        if self.acceptable_proposals:
            new_match: Proposer
            if self.is_matched and isinstance(
                self.match, Proposer
            ):  # if already matched to a proposer
                new_match = self._most_preferred(
                    self.acceptable_proposals + [self.match]
                )
                if new_match != self.match:  # otherwise if == do nothing
                    self.match.is_matched = False  # make current match unmatched
                    self.match = new_match  # current match is set to new match
                    new_match.match = self  # current match of the match is set to self
                    # print(f"{self.name} is engaged to {self.match.name}")
            else:  # if not matched or matched to self
                new_match = self._most_preferred(self.acceptable_proposals)
                self.match = new_match
                new_match.match = self
                # print(f"{self.name} is engaged to {self.match.name}")
        self.current_proposals = None
