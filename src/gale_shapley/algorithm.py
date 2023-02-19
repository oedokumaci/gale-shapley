"""Algorithm module."""

from __future__ import annotations  # needed in 3.9 for | of Python 3.10

import logging

from gale_shapley.person import Proposer, Responder
from gale_shapley.utils import timer_decorator


class Algorithm:
    """Gale-Shapley Algorithm class. Uses __slots__ instead of the default __dict__ for memory efficiency."""

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
    def persons(self) -> list[Proposer | Responder]:
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
        logging.info("")
        for proposer in self.proposers:
            if (
                proposer.match is not None
            ):  # mypy complains if proposer.is_matched is used
                logging.info(
                    f"{proposer.name} is matched to {'self' if proposer.name == proposer.match.name else proposer.match.name}."
                )
            else:
                logging.info(f"{proposer.name} is unmatched.")
        for responder in self.responders:
            if responder.match == responder:
                logging.info(f"{responder.name} is matched to self.")
            elif not responder.is_matched:
                logging.info(f"{responder.name} is unmatched.")
        logging.info("")

    def print_all_preferences(self, compact: bool = True) -> None:
        """Prints the preferences of all proposers and responders.

        Args:
            compact (bool, optional): If True prints all in one table. Defaults to True.
        """
        if compact:
            logging.info(
                "Printing preferences in compact format, only showing acceptables:"
            )
            header: list[str] = [p.name for p in self.persons]
            first_column: list[str] = [
                f"{i + 1}."
                for i in range(max(len(self.proposers), len(self.responders)) + 1)
            ]
            data: list[list[str]] = []
            for i in range(len(first_column)):
                data.append(
                    [
                        person.preferences[i].name
                        if person.preferences is not None
                        and i < len(person.preferences)
                        and person.is_acceptable(person.preferences[i])
                        else ""
                        for person in self.persons
                    ]
                )
            format_row: str = "{:>5}" * (
                len(header) + 1
            )  # doing with f-strings could be a pain
            logging.info(format_row.format("", *header))
            logging.info(format_row.format("", *["-" * len(h) for h in header]))
            for pref, row in zip(first_column, data):
                logging.info(format_row.format(pref, *row))
        else:
            for person in self.persons:
                person.print_preferences()

    @timer_decorator
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
        logging.info("")
        logging.info("Running algorithm...")
        while not self.terminate():
            self.proposers_propose()
            self.responders_respond()
            self.round += 1
        for responder in self.responders:  # change None to self matches
            if not responder.is_matched:
                responder.match = responder
        logging.info(f"Algorithm terminated after {self.round} rounds.")
        if report_matches:
            self.report_matches()
