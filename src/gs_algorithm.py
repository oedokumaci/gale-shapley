from typing import Type

import person


def gs_algorithm(Person: Type[person.Person]) -> None:
    print("******************** Running Gale-Shapley Algorithm ********************")
    proposers = Person.persons[Person.proposing_side]
    responders = Person.persons[proposers[0].get_opposite_gender()]
    round_number = 1
    while any(proposer.is_single for proposer in proposers):
        print(f"********** Round {round_number} **********")
        print("--------- Proposals ---------")
        for proposer in proposers:
            if proposer.is_single:
                proposer.propose(proposer.next)
        print("--------- Responses ---------")
        for responder in responders:
            responder.respond_to_proposals()
        if round_number % 5 == 0:
            Person.print_matches()
        round_number += 1
    print("******************** Run Complete ********************")
    Person.print_matches(final=True)
