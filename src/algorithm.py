from proposer_responder import Proposer, Responder


class Algorithm:

    __slots__ = ("proposers", "responders")

    def __init__(self, proposers: list[Proposer], responders: list[Responder]) -> None:
        self.proposers = proposers
        self.responders = responders

    @property
    def unmatched_proposers(self) -> list[Proposer]:
        return [proposer for proposer in self.proposers if not proposer.is_matched]

    def proposers_propose(self) -> None:
        for proposer in self.unmatched_proposers:
            proposer.propose()

    def responders_respond(self) -> None:
        for responder in self.responders:
            responder.respond()

    def terminate(self) -> bool:
        return all(proposer.is_matched for proposer in self.proposers)

    def report_matches(self) -> None:
        for proposer in self.proposers:
            print(f"{proposer.name} is matched to {proposer.match.name}")

    def print_all_preferences(self) -> None:
        for person in self.proposers + self.responders:
            person.print_preferences()

    def run(self) -> None:
        self.print_all_preferences()
        while not self.terminate():
            self.proposers_propose()
            self.responders_respond()
        self.report_matches()
