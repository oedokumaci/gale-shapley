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
        self.proposers: list[Proposer] | None = None
        self.responders: list[Responder] | None = None
        self.results: list[Algorithm] | None = None
        self.number_of_simulations: int = 100

    @property
    def persons(self) -> list[Proposer | Responder]:
        """Returns all proposers and responders."""
        if self.proposers is None or self.responders is None:
            raise ValueError("Proposers and responders are not created yet.")
        return self.proposers + self.responders

    @property
    def blocking_pairs(self) -> list[tuple[Proposer, Responder]]:
        """Returns all blocking pairs."""
        blocking: list[tuple[Proposer, Responder]] = []
        if self.proposers is not None and self.responders is not None:
            for proposer in self.proposers:  # looping one side is enough
                if proposer.preferences is not None and proposer.is_matched:
                    better_than_match_of_proposer: tuple[
                        Proposer | Responder, ...
                    ] = proposer.preferences[
                        : proposer.preferences.index(proposer.match)
                    ]
                    for responder in better_than_match_of_proposer:
                        if isinstance(
                            responder, Responder
                        ):  # need for type checking only
                            if not responder.is_matched:
                                blocking.append((proposer, responder))
                            else:
                                if (
                                    responder.preferences is not None
                                    and responder.preferences.index(proposer)
                                    < responder.preferences.index(responder.match)
                                ):
                                    blocking.append((proposer, responder))
        return blocking

    def create_objects(self) -> tuple[list[Proposer], list[Responder]]:
        """Creates the objects for the algorithm.

        Returns:
            tuple[list[Proposer], list[Responder]]: list of proposers and list of responders
        """
        if self.preference_type == "random":
            proposers: list[Proposer]
            responders: list[Responder]
            if self.proposer_name[0] != self.responder_name[0]:
                proposers = [
                    Proposer(f"{self.proposer_name[0]}_{i+1}", self.proposer_name)
                    for i in range(self.num_proposers)
                ]
                responders = [
                    Responder(f"{self.responder_name[0]}_{i+1}", self.responder_name)
                    for i in range(self.num_responders)
                ]
            else:  # use full names if first letter is the same
                proposers = [
                    Proposer(f"{self.proposer_name}_{i+1}", self.proposer_name)
                    for i in range(self.num_proposers)
                ]
                responders = [
                    Responder(f"{self.responder_name}_{i+1}", self.responder_name)
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
        """Checks if matching is individually rational.

        Returns:
            bool: True if individually rational, False otherwise
        """
        for person in self.persons:
            if (
                person.match is not None
            ):  # that is, if person.is_matched but mypy does not know
                if not person.is_acceptable(person.match):
                    return False
        return True

    @timer_decorator
    def is_stable(self) -> bool:
        """Checks if the matching is stable.

        Returns:
            bool: True if stable, False otherwise
        """
        if not self.is_individually_rational():
            return False
        if len(self.blocking_pairs) > 0:
            return False
        return True

    @timer_decorator
    def simulate(
        self, print_all_preferences: bool = True, report_matches: bool = True
    ) -> None:
        """Simulates the algorithm desired number of times.

        Args:
            print_all_preferences (bool, optional): Defaults to True
            report_matches (bool, optional): Defaults to True
        """
        self.results = []
        offset: int = len(str(self.number_of_simulations))  # for formatting print
        for i in range(self.number_of_simulations):
            logging.info("")
            logging.info(f"{'*':*>30} SIMULATION {str(i+1):>{offset}} {'*':*>30}")
            self.proposers, self.responders = self.create_objects()
            algorithm = Algorithm(self.proposers, self.responders)
            algorithm.run(print_all_preferences, report_matches)
            if self.is_stable():
                logging.info("Matching is stable.")
            else:
                logging.info("Matching is not stable.")
            self.results.append(algorithm)
