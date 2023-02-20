"""Simulator module."""

from __future__ import annotations  # needed in 3.9 for | of Python 3.10

import logging
import random

from gale_shapley.algorithm import Algorithm
from gale_shapley.config_parser import YAMLConfig
from gale_shapley.person import Proposer, Responder
from gale_shapley.utils import timer_decorator


class Simulator:
    """Simulator class. Creates objects and runs the algorithm."""

    def __init__(self, config_input: YAMLConfig) -> None:
        """Constructor for Simulator class.

        Args:
            config_input (YAMLConfig): parsed from config file
        """
        self.proposer_name: str = config_input.proposer_side_name
        self.responder_name: str = config_input.responder_side_name
        self.num_proposers: int = config_input.number_of_proposers
        self.num_responders: int = config_input.number_of_responders
        self.preference_type: str = config_input.preference_type
        self.proposers: list[Proposer] = []
        self.responders: list[Responder] = []
        self.results: list[Algorithm] = []
        self.number_of_simulations: int = 100

    @property
    def persons(self) -> list[Proposer | Responder]:
        """Returns all proposers and responders."""
        return self.proposers + self.responders

    def create_objects(self) -> tuple[list[Proposer], list[Responder]]:
        """Creates the objects for the algorithm.

        Returns:
            tuple[list[Proposer], list[Responder]]: created list of proposers and list of responders
        """
        if self.preference_type == "Random":
            proposer_name_short: str
            responder_name_short: str
            if self.proposer_name[0].lower() != self.responder_name[0].lower():
                proposer_name_short = self.proposer_name[0].lower()
                responder_name_short = self.responder_name[0].lower()
            else:  # use full names if first letter is the same
                proposer_name_short = self.proposer_name.lower()
                responder_name_short = self.responder_name.lower()
            proposers: list[Proposer] = [
                Proposer(f"{proposer_name_short}_{i+1}", self.proposer_name)
                for i in range(self.num_proposers)
            ]
            responders: list[Responder] = [
                Responder(f"{responder_name_short}_{i+1}", self.responder_name)
                for i in range(self.num_responders)
            ]

            select_from: list[Proposer | Responder]
            for proposer in proposers:
                select_from = responders + [proposer]
                random.shuffle(select_from)
                proposer.preferences = tuple(select_from)
            for responder in responders:
                select_from = proposers + [responder]
                random.shuffle(select_from)
                responder.preferences = tuple(select_from)

        return proposers, responders

    def is_individually_rational(self) -> bool:
        """Checks if the matching is individually rational.

        Returns:
            bool: True if individually rational, False otherwise
        """
        for person in self.persons:
            if (
                person.match is not None
            ):  # mypy complains if proposer.is_matched is used
                if not person.is_acceptable(person.match):
                    return False
        return True

    @property
    def blocking_pairs(self) -> list[tuple[Proposer, Responder]]:
        """Returns all blocking pairs."""
        blocking: list[tuple[Proposer, Responder]] = []
        for proposer in self.proposers:  # looping one side is enough
            if bool(proposer.preferences) and proposer.is_matched:
                better_than_match_of_proposer: tuple[
                    Proposer | Responder, ...
                ] = proposer.preferences[: proposer.preferences.index(proposer.match)]
                for responder in better_than_match_of_proposer:
                    if isinstance(
                        responder, Responder
                    ):  # do not want (self, self) in blocking
                        if not responder.is_matched:
                            blocking.append((proposer, responder))
                        else:
                            if (
                                (bool(responder.preferences))
                                and (
                                    all(
                                        item in responder.preferences
                                        for item in [proposer, responder.match]
                                    )
                                )
                                and (
                                    responder.preferences.index(proposer)
                                    < responder.preferences.index(responder.match)
                                )
                            ):
                                blocking.append((proposer, responder))
        return blocking

    @timer_decorator
    def is_stable(self) -> bool:
        """Checks if the matching is stable.

        Returns:
            bool: True if stable, False otherwise
        """
        return self.is_individually_rational() and not bool(self.blocking_pairs)

    @timer_decorator
    def simulate(
        self,
        print_all_preferences: bool = True,
        compact: bool = True,
        report_matches: bool = True,
    ) -> None:
        """Simulates the algorithm desired number of times.

        Args:
            print_all_preferences (bool, optional): Prints individual preferences before running, defaults to False
            compact (bool, optional): If True prints all in one table, defaults to True
            report_matches (bool, optional): Reports the final matching, defaults to True
        """
        offset: int = len(str(self.number_of_simulations))  # for formatting print
        logging.info("")
        logging.info("Starting simulations...")
        for i in range(self.number_of_simulations):
            logging.info("")
            logging.info(f"{'*':*>30} SIMULATION {str(i+1):>{offset}} {'*':*>30}")
            self.proposers, self.responders = self.create_objects()
            algorithm = Algorithm(self.proposers, self.responders)
            algorithm.run(
                print_all_preferences=print_all_preferences,
                compact=compact,
                report_matches=report_matches,
            )
            # if self.is_stable():
            #     logging.info("Matching is stable.")
            # else:
            #     logging.info("Matching is not stable.")
            self.results.append(algorithm)
        logging.info("")
        logging.info("Simulations ended.")
