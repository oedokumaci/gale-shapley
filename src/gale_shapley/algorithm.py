"""Algorithm module."""

import logging
from dataclasses import dataclass
from typing import Final

from gale_shapley.person import Proposer, Responder
from gale_shapley.utils import timer_decorator


@dataclass(slots=True)
class Algorithm:
    """Gale-Shapley Algorithm class.
    Uses slots for memory efficiency."""

    proposers: list[Proposer]
    responders: list[Responder]
    round: int = 0

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
        logging.info("Printing the matching:")
        for proposer in self.proposers:
            match proposer.match:
                case None:
                    logging.info(f"{proposer.name} is unmatched.")
                case match if match.name == proposer.name:
                    logging.info(f"{proposer.name} is matched to self.")
                case match:
                    logging.info(f"{proposer.name} is matched to {match.name}.")

        for responder in self.responders:
            match responder.match:
                case match if match == responder:
                    logging.info(f"{responder.name} is matched to self.")
                case None:
                    logging.info(f"{responder.name} is unmatched.")

    @timer_decorator
    def print_all_preferences(self, compact: bool = True) -> None:
        """Prints the preferences of all proposers and responders.

        Args:
            compact (bool): If True prints all in one table. Defaults to True.
        """
        if compact:
            logging.info(
                "Printing preferences in compact format, only showing acceptables:"
            )
            header: Final[list[str]] = [p.name for p in self.persons]
            first_column: Final[list[str]] = [
                f"{i}."
                for i in range(1, max(len(self.proposers), len(self.responders)) + 2)
            ]
            data: list[list[str]] = []
            for i in range(len(first_column)):
                data.append(
                    [
                        (
                            person.preferences[i].name
                            if bool(person.preferences)
                            and i < len(person.preferences)
                            and person.is_acceptable(person.preferences[i])
                            else ""
                        )
                        for person in self.persons
                    ]
                )
            format_row: Final[str] = "{:8}" * (len(header) + 1)
            logging.info(format_row.format("", *header))
            logging.info(format_row.format("", *["-" * len(h) for h in header]))
            for pref, row in zip(first_column, data):
                logging.info(format_row.format(pref, *row))
        else:
            logging.info("Printing preferences for each person separately:")
            for person in self.persons:
                person.print_preferences()
                if person != self.persons[-1]:
                    logging.info("")

    @timer_decorator
    def run(
        self,
        print_all_preferences: bool = True,
        compact: bool = True,
        report_matches: bool = True,
    ) -> None:
        """Runs the algorithm and prints desired information.

        Args:
            print_all_preferences (bool): Prints individual preferences before running. Defaults to True.
            compact (bool): If True prints all in one table. Defaults to True.
            report_matches (bool): Reports the final matching. Defaults to True.
        """
        if print_all_preferences:
            self.print_all_preferences(compact=compact)
            logging.info("")

        logging.info("Running algorithm...")
        while not self.terminate():
            self.proposers_propose()
            self.responders_respond()
            self.round += 1

        # Change None to self matches for unmatched responders
        for responder in self.responders:
            if not responder.is_matched:
                responder.match = responder

        logging.info(f"Algorithm terminated after {self.round} rounds.")
        if report_matches:
            self.report_matches()
