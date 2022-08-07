# Gale-Shapley Algorithm

def gs_algorithm(Person):
    print('----- Running Gale-Shapley Algorithm -----')
    proposers = Person.persons[Person.proposer_side]
    responders = Person.persons[proposers[0].get_opposite_gender()]
    round_number = 1
    while any(proposer.is_single() for proposer in proposers):
        print(f'--- Round {round_number} ---')
        print('--- Proposing...')
        for proposer in proposers:
            if proposer.is_single():
                proposer.propose(proposer.next)
        print('--- Responding...')
        for responder in responders:
            responder.respond_to_proposals()
        round_number += 1
    print('----- Run Complete -----')
    Person.print_matches()
    