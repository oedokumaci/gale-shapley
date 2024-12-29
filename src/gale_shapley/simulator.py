"""Simulator module."""

import logging
import random
from dataclasses import dataclass, field
from typing import Final

from gale_shapley.algorithm import Algorithm
from gale_shapley.config import YAMLConfig
from gale_shapley.person import Proposer, Responder
from gale_shapley.utils import timer_decorator


@dataclass
class Simulator:
    """Simulator class. Creates objects and runs the algorithm."""

    config_input: YAMLConfig
    proposers: list[Proposer] = field(default_factory=list)
    responders: list[Responder] = field(default_factory=list)
    results: list[Algorithm] = field(default_factory=list)
    number_of_simulations: int = 100

    @property
    def persons(self) -> list[Proposer | Responder]:
        """Returns all proposers and responders."""
        return self.proposers + self.responders

    def create_objects(self) -> tuple[list[Proposer], list[Responder]]:
        """Creates the objects for the algorithm.

        Returns:
            tuple[list[Proposer], list[Responder]]: created list of proposers and list of responders
        """
        proposers: list[Proposer] = []
        responders: list[Responder] = []

        match self.config_input.preference_type.casefold():
            case "random":
                # Create short names for proposers and responders
                proposer_name_short = self.config_input.proposer_side_name[0].casefold()
                responder_name_short = self.config_input.responder_side_name[
                    0
                ].casefold()

                if proposer_name_short == responder_name_short:
                    # Use full names if first letter is the same
                    proposer_name_short = (
                        self.config_input.proposer_side_name.casefold()
                    )
                    responder_name_short = (
                        self.config_input.responder_side_name.casefold()
                    )

                # Create proposers and responders with no preferences
                proposers = [
                    Proposer(
                        f"{proposer_name_short}_{i + 1}",
                        self.config_input.proposer_side_name,
                    )
                    for i in range(self.config_input.number_of_proposers)
                ]
                responders = [
                    Responder(
                        f"{responder_name_short}_{i + 1}",
                        self.config_input.responder_side_name,
                    )
                    for i in range(self.config_input.number_of_responders)
                ]

                # Randomly assign preferences
                for proposer in proposers:
                    select_from = responders + [proposer]
                    random.shuffle(select_from)
                    proposer.preferences = tuple(select_from)
                for responder in responders:
                    select_from = proposers + [responder]
                    random.shuffle(select_from)
                    responder.preferences = tuple(select_from)

            case "input":
                # Create proposers and responders with no preferences
                proposers = [
                    Proposer(name, self.config_input.proposer_side_name)
                    for name in self.config_input.proposers
                ]
                responders = [
                    Responder(name, self.config_input.responder_side_name)
                    for name in self.config_input.responders
                ]

                # Assign inputted preferences
                for proposer in proposers:
                    preferences: list[Proposer | Responder] = [
                        next(r for r in responders if r.name == responder_name)
                        for responder_name in self.config_input.proposers[proposer.name]
                    ]
                    if len(preferences) < len(responders) + 1:
                        if proposer not in preferences:
                            preferences.append(proposer)
                        missing_responders = [
                            responder
                            for responder in responders
                            if responder.name
                            not in self.config_input.proposers[proposer.name]
                        ]
                        random.shuffle(missing_responders)
                        preferences.extend(missing_responders)
                    proposer.preferences = tuple(preferences)

                for responder in responders:
                    responder_preferences: list[Proposer | Responder] = [
                        next(p for p in proposers if p.name == proposer_name)
                        for proposer_name in self.config_input.responders[
                            responder.name
                        ]
                    ]
                    if len(responder_preferences) < len(proposers) + 1:
                        if responder not in responder_preferences:
                            responder_preferences.append(responder)
                        missing_proposers = [
                            proposer
                            for proposer in proposers
                            if proposer.name
                            not in self.config_input.responders[responder.name]
                        ]
                        random.shuffle(missing_proposers)
                        responder_preferences.extend(missing_proposers)
                    responder.preferences = tuple(responder_preferences)

        return proposers, responders

    def is_individually_rational(self) -> bool:
        """Checks if the matching is individually rational.

        Returns:
            bool: True if individually rational, False otherwise
        """
        return all(
            person.match is None or person.is_acceptable(person.match)
            for person in self.persons
        )

    @property
    def blocking_pairs(self) -> list[tuple[Proposer, Responder]]:
        """Returns all blocking pairs."""
        blocking: list[tuple[Proposer, Responder]] = []
        for proposer in self.proposers:  # looping one side is enough
            if not (bool(proposer.preferences) and proposer.is_matched):
                continue

            better_than_match = proposer.preferences[
                : proposer.preferences.index(proposer.match)
            ]
            for responder in better_than_match:
                if not isinstance(responder, Responder):  # Skip self matches
                    continue

                match responder.is_matched:
                    case False:
                        blocking.append((proposer, responder))
                    case True if (
                        bool(responder.preferences)
                        and all(
                            item in responder.preferences
                            for item in [proposer, responder.match]
                        )
                        and responder.preferences.index(proposer)
                        < responder.preferences.index(responder.match)
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
            print_all_preferences (bool): Prints individual preferences before running. Defaults to True.
            compact (bool): If True prints all in one table. Defaults to True.
            report_matches (bool): Reports the final matching. Defaults to True.
        """
        offset: Final[int] = len(str(self.number_of_simulations))
        logging.info("")
        logging.info("Starting simulations...")

        for i in range(self.number_of_simulations):
            logging.info("")
            logging.info(f"{'*':*>30} SIMULATION {str(i + 1):>{offset}} {'*':*>30}")
            self.proposers, self.responders = self.create_objects()
            algorithm = Algorithm(self.proposers, self.responders)
            algorithm.run(
                print_all_preferences=print_all_preferences,
                compact=compact,
                report_matches=report_matches,
            )
            self.results.append(algorithm)

        logging.info("")
        logging.info("Simulations ended.")
