"""Proposer and Responder module (subclasses of Person)."""

from __future__ import annotations

from typing import Union

from person import Person


class Proposer(Person):
    """Proposer class, subclass of Person."""

    def __init__(self, name: str, side: str) -> None:
        """Constructor for Proposer class.

        Args:
            name (str): name of the person for super constructor, parsed from config.yaml
            side (str): side of the person for super constructor, parsed from config.yaml
        """
        super().__init__(name, side)
        self.last_proposal: Union[Responder, None] = None  # last responder proposed to

    @property
    def acceptable_to_propose(self) -> list[Responder]:
        """Returns a list of acceptable responders to propose to.

        Returns:
            list[Responder]: list of acceptable responders
        """
        return [
            responder for responder in self.preferences if self.is_acceptable(responder)
        ]

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
        if self.next_proposal == self:
            self.match = self
        else:
            try:
                self.next_proposal.current_proposals.append(self)
            except AttributeError:
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
            list(Proposer), None
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
        return [
            proposer
            for proposer in self.current_proposals
            if self.is_acceptable(proposer)
        ]

    def _most_preferred(
        self, proposals_and_current_match: list[Proposer, Responder]
    ) -> Proposer:  # returns most preferred of the list
        return min(proposals_and_current_match, key=self.preferences.index)

    def respond(self) -> None:
        """Responds to proposals and updates current_proposals to None."""
        if self.acceptable_proposals:
            if self.is_matched:  # if already matched
                new_match = self._most_preferred(
                    self.acceptable_proposals + [self.match]
                )
                if new_match != self.match:  # do nothing if new match is current match
                    self.match.is_matched = False  # unmatch current match
                    self.match = new_match  # current match is set to new match
                    new_match.match = self  # current match of the match is set to self
                    # print(f"{self.name} is engaged to {self.match.name}")
            else:  # if not matched
                new_match = self._most_preferred(self.acceptable_proposals)
                self.match = new_match
                new_match.match = self
                # print(f"{self.name} is engaged to {self.match.name}")
        self.current_proposals = None
