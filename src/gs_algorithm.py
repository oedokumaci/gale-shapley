import concurrent.futures
        
# Gale-Shapley Algorithm

def gs_algorithm(Person):
    print('******************** Running Gale-Shapley Algorithm ********************')
    proposers = Person.persons[Person.proposing_side]
    responders = Person.persons[proposers[0].get_opposite_gender()]
    round_number = 1
    while any(proposer.is_single for proposer in proposers):
        print(f'********** Round {round_number} **********')
        print('--------- Proposals ---------')
        for proposer in proposers:
            if proposer.is_single:
                proposer.propose(proposer.next)
        print('--------- Responses ---------')
        for responder in responders:
            responder.respond_to_proposals()
        if round_number % 5 == 0:
            Person.print_matches()
        round_number += 1
    print('******************** Run Complete ********************')
    Person.print_matches(final=True)
    
# Gale-Shapley Algorithm Multi-Threaded

def proposals_thread(proposer):
    if proposer.is_single:
        proposer.propose(proposer.next)
            
def responses_thread(responder):
    responder.respond_to_proposals()
    
def gs_algorithm_threaded(Person):
    print('******************** Running Gale-Shapley Algorithm ********************')
    proposers = Person.persons[Person.proposing_side]
    responders = Person.persons[proposers[0].get_opposite_gender()]
    round_number = 1
    while any(proposer.is_single for proposer in proposers):
        print(f'********** Round {round_number} **********')
        print('--------- Proposals ---------')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(proposals_thread, proposers)
        print('--------- Responses ---------')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(responses_thread, responders)
        if round_number % 5 == 0:
            Person.print_matches()
        round_number += 1
    print('******************** Run Complete ********************')
    Person.print_matches(final=True)
    