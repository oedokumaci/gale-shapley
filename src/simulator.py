"""Simulator module."""

import random
from typing import Union

from algorithm import Algorithm
from proposer_responder import Proposer, Responder
from utils import timer_decorator


class Simulator:
    """Simulator class. Creates objects and runs the algorithm."""

    def __init__(
        self,
        proposer_name: str,
        responder_name: str,
        num_proposers: int,
        num_responders: int,
        preference_type: str,
    ) -> None:
        """Constructor for Simulator class.

        Args:
            proposer_name (str): parsed from config file
            responder_name (str): parsed from config file
            num_proposers (int): parsed from config file
            num_responders (int): parsed from config file
        """
        self.proposer_name = proposer_name
        self.responder_name = responder_name
        self.num_proposers = num_proposers
        self.num_responders = num_responders
        self.preference_type = preference_type
        self.proposers: Union[list[Proposer], None] = None
        self.responders: Union[list[Responder], None] = None
        self.number_of_simulations: int = 100
        self.results: Union[list[Algorithm], None] = None

    @property
    def persons(self) -> list[Proposer, Responder]:
        """Returns all proposers and responders."""
        return self.proposers + self.responders

    @property
    def blocking_pairs(self) -> list[tuple[Proposer, Responder]]:
        """Returns all blocking pairs."""
        blocking = []
        for proposer in self.proposers:
            for responder in proposer.better_than_match:
                if proposer in responder.better_than_match:
                    blocking.append((proposer, responder))
        return blocking

    def create_objects(self) -> tuple[list[Proposer], list[Responder]]:
        """Creates the objects for the algorithm.

        Returns:
            tuple[list[Proposer], list[Responder]]: list of proposers and list of responders
        """
        if self.preference_type == "random":
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

            for proposer in proposers:
                select_from = [proposer] + responders
                random.shuffle(select_from)
                proposer.preferences = tuple(select_from)
            for responder in responders:
                select_from = [responder] + proposers
                random.shuffle(select_from)
                responder.preferences = tuple(select_from)

            return proposers, responders

    def is_individually_rational(self) -> bool:
        """Checks if matching is individually rational.

        Returns:
            bool: True if individually rational, False otherwise
        """
        return all(person.is_acceptable(person.match) for person in self.persons)

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

    def run(
        self, print_all_preferences: bool = True, report_matches: bool = True
    ) -> None:
        """Simulates the algorithm desired number of times.

        Args:
            print_all_preferences (bool, optional): Defaults to True
            report_matches (bool, optional): Defaults to True
        """
        self.results = []
        offset = len(str(self.number_of_simulations))
        for i in range(self.number_of_simulations):
            print(f"{'*':*>30} Simulation {str(i+1):>{offset}} {'*':*>30}")
            self.proposers, self.responders = self.create_objects()
            algorithm = Algorithm(self.proposers, self.responders)
            algorithm.run(print_all_preferences, report_matches)
            if self.is_stable():
                print("Matching is stable.")
            else:
                print("Matching is not stable.")
            self.results.append(algorithm)
