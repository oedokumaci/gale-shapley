from __future__ import annotations

from typing import Union

from person import Person


class Proposer(Person):
    def __init__(self, name: str, side: str) -> None:
        super().__init__(name, side)
        self.last_proposal: Union[Responder, None] = None

    @property
    def acceptable_to_propose(self) -> list[Responder]:
        return [
            responder
            for responder in self.preferences
            if self._is_acceptable(responder)
        ]

    @property
    def next_proposal(self) -> Union[Responder, Proposer]:
        try:
            if self.last_proposal is None:
                return self.acceptable_to_propose[0]
            elif self.last_proposal != self:
                return self.acceptable_to_propose[
                    self.acceptable_to_propose.index(self.last_proposal) + 1
                ]
            return self
        except IndexError:
            return self

    def propose(self) -> None:
        if self.next_proposal == self:
            self.match = self
        else:
            try:
                self.next_proposal.current_proposals.append(self)
            except AttributeError:
                self.next_proposal.current_proposals = [self]
        self.last_proposal = self.next_proposal


class Responder(Person):
    def __init__(self, name: str, side: str) -> None:
        super().__init__(name, side)
        self.current_proposals: Union[list(Proposer), None] = None

    @property
    def awaiting_to_respond(self) -> bool:
        return self.current_proposals is not None

    @property
    def acceptable_proposals(self) -> list[Proposer]:
        return [
            proposer
            for proposer in self.current_proposals
            if self._is_acceptable(proposer)
        ]

    def _most_preferred(
        self, proposals_and_current_match: list[Proposer, Responder]
    ) -> Proposer:
        return min(proposals_and_current_match, key=self.preferences.index)

    def respond(self) -> None:
        if self.acceptable_proposals:
            if self.is_matched:
                new_match = self._most_preferred(
                    self.acceptable_proposals + [self.match]
                )
                if new_match != self.match:
                    self.match.is_matched = False
                    self.match = new_match
                    self.match.match = self
                    # print(f"{self.name} is engaged to {self.match.name}")
            else:
                new_match = self._most_preferred(self.acceptable_proposals)
                self.match = new_match
                self.match.match = self
                # print(f"{self.name} is engaged to {self.match.name}")
        self.current_proposals = None
