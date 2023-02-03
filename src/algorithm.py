"""Algorithm module."""

from proposer_responder import Proposer, Responder


class Algorithm:
    """Algorithm class. Uses __slots__ instead of __dict__ for memory efficiency."""

    __slots__ = ("proposers", "responders")

    def __init__(self, proposers: list[Proposer], responders: list[Responder]) -> None:
        """Constructor for Algorithm class.

        Args:
            proposers (list[Proposer]): list of proposers, preferences should be already set
            responders (list[Responder]): list of responders, preferences should be already set
        """

        self.proposers = proposers
        self.responders = responders

    @property
    def unmatched_proposers(self) -> list[Proposer]:
        """Returns unmatched proposers, excludes self matches."""
        return [proposer for proposer in self.proposers if not proposer.is_matched]

    @property
    def awaiting_to_respond_responders(self) -> list[Responder]:
        """Returns responders that are awaiting to respond."""
        return [
            responder for responder in self.responders if responder.awaiting_to_respond
        ]

    def proposers_propose(self) -> None:
        """Makes all unmatched proposers propose to their next choice."""
        for proposer in self.unmatched_proposers:
            proposer.propose()

    def responders_respond(self) -> None:
        """Makes all responders that are awaiting to respond respond."""
        for responder in self.awaiting_to_respond_responders:
            responder.respond()

    def terminate(self) -> bool:
        """Returns True if all proposers are matched, False otherwise."""
        return all(proposer.is_matched for proposer in self.proposers)

    def report_matches(self) -> None:
        """Prints all matches, does not print unmatched responders."""
        for proposer in self.proposers:
            print(f"{proposer.name} is matched to {proposer.match.name}")

    def print_all_preferences(self) -> None:
        """Prints the preferences of all proposers and responders."""
        for person in self.proposers + self.responders:
            person.print_preferences()

    def run(self) -> None:
        """Runs the algorithm and prints desired information."""
        self.print_all_preferences()
        while not self.terminate():
            self.proposers_propose()
            self.responders_respond()
        self.report_matches()
