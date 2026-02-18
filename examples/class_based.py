"""Using the Algorithm, Proposer, and Responder classes directly."""

import gale_shapley_algorithm as gsa

# Create persons
m1 = gsa.Proposer("m1", "men")
m2 = gsa.Proposer("m2", "men")
w1 = gsa.Responder("w1", "women")
w2 = gsa.Responder("w2", "women")

# Set preferences (each person includes themselves to mark acceptability threshold)
m1.preferences = (w1, w2, m1)  # m1 prefers w1 > w2 > being unmatched
m2.preferences = (w2, w1, m2)
w1.preferences = (m1, m2, w1)
w2.preferences = (m2, m1, w2)

# Run the algorithm
algo = gsa.Algorithm([m1, m2], [w1, w2])
result = algo.execute()

print(f"Rounds: {result.rounds}")
print(f"Matches: {result.matches}")
print(f"All matched: {result.all_matched}")

# You can also inspect the formatted output
print()
print(algo.format_all_preferences())
print()
print(algo.format_matches())
