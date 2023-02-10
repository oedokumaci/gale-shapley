"""Algorithm module."""

from proposer_responder import Proposer, Responder


class Algorithm:
    """Algorithm class. Uses __slots__ instead of the default __dict__ for memory efficiency."""

    __slots__ = ("proposers", "responders", "round")

    def __init__(self, proposers: list[Proposer], responders: list[Responder]) -> None:
        """Constructor for Algorithm class.

        Args:
            proposers (list[Proposer]): list of proposers
            responders (list[Responder]): list of responders
        """
        self.proposers = proposers
        self.responders = responders
        self.round: int = 0

    @property
    def persons(self) -> list[Proposer, Responder]:
        """Returns all proposers and responders."""
        return self.proposers + self.responders

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
        print(f"Algorithm terminated after {self.round} rounds.")
        for proposer in self.proposers:
            if proposer.name == proposer.match.name:
                print(f"{proposer.name} is matched to self.")
            else:
                print(f"{proposer.name} is matched to {proposer.match.name}")
        for responder in self.responders:
            if not responder.is_matched:
                print(f"{responder.name} is matched to self.")

    def print_all_preferences(self, compact: bool = True) -> None:
        """Prints the preferences of all proposers and responders.

        Args:
            compact (bool, optional): If True prints all in one table. Defaults to True.
        """
        if compact:
            print("Printing preferences in compact format, only showing acceptables:")
            header = [p.name for p in self.persons]
            first_column = [
                i + 1 for i in range(max(len(self.proposers), len(self.responders)) + 1)
            ]
            data = []
            for i in range(len(first_column)):
                data.append(
                    [
                        person.preferences[i].name
                        if i < len(person.preferences)
                        and (
                            person.is_acceptable(person.preferences[i])
                            or person.preferences[i] == person
                        )
                        else ""
                        for person in self.persons
                    ]
                )
            format_row = "{:>12}" * (
                len(header) + 1
            )  # doing with f-strings could be a pain
            print(format_row.format("", *header))
            print(format_row.format("", *["-" * len(h) for h in header]))
            for pref, row in zip(first_column, data):
                print(format_row.format(pref, *row))
        else:
            for person in self.persons:
                person.print_preferences()

    def run(
        self, print_all_preferences: bool = True, report_matches: bool = True
    ) -> None:
        """Runs the algorithm and prints desired information.

        Args:
            print_all_preferences (bool, optional): prints individual preferences before running, defaults to False
            report_matches (bool, optional): reports final matching, defaults to True
        """
        if print_all_preferences:
            self.print_all_preferences()
        while not self.terminate():
            self.proposers_propose()
            self.responders_respond()
            self.round += 1
        if report_matches:
            self.report_matches()
