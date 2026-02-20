"""Basic usage of the gale-shapley-algorithm library using the convenience function."""

import gale_shapley_algorithm as gsa

# Define preferences for each side
result = gsa.create_matching(
    proposer_preferences={
        "alice": ["xavier", "yuri", "zeus"],
        "beth": ["yuri", "xavier", "zeus"],
        "cara": ["xavier", "yuri", "zeus"],
    },
    responder_preferences={
        "xavier": ["beth", "alice", "cara"],
        "yuri": ["alice", "beth", "cara"],
        "zeus": ["alice", "beth", "cara"],
    },
)

print(f"Rounds: {result.rounds}")
print(f"Matches: {result.matches}")
print(f"Self-matches: {result.self_matches}")
print(f"All matched: {result.all_matched}")
