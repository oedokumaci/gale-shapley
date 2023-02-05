"""Simulator module."""

import random
from typing import Union

from algorithm import Algorithm
from proposer_responder import Proposer, Responder


class Simulator:
    def __init__(
        self,
        proposer_name: str,
        responder_name: str,
        num_proposers: int,
        num_responders: int,
    ):
        self.proposer_name = proposer_name
        self.responder_name = responder_name
        self.num_proposers = num_proposers
        self.num_responders = num_responders
        self.proposers: Union[list[Proposer], None] = None
        self.responders: Union[list[Responder], None] = None
        self.number_of_simulations: int = 100
        self.results: Union[list[Algorithm], None] = None

    def create_objects(self) -> None:
        """Creates the objects for the algorithm.

        Returns:
            tuple[list[Proposer], list[Responder]]: list of proposers and list of responders
        """
        if self.proposer_name[0] != self.responder_name[0]:
            proposers = [
                Proposer(f"{self.proposer_name[0]}_{i+1}", self.proposer_name)
                for i in range(self.num_proposers)
            ]
            responders = [
                Responder(f"{self.responder_name[0]}_{i+1}", self.responder_name)
                for i in range(self.num_responders)
            ]
        else:
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

        self.proposers, self.responders = proposers, responders

    def run(
        self, print_all_preferences: bool = False, report_matches: bool = True
    ) -> None:
        """Runs the algorithm."""
        self.results = []
        for _ in range(self.number_of_simulations):
            self.create_objects()
            algorithm = Algorithm(self.proposers, self.responders)
            algorithm.run(print_all_preferences, report_matches)
            self.results.append(algorithm)
