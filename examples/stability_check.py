"""Checking stability of a matching."""

import gale_shapley_algorithm as gsa

# Create a scenario
m1 = gsa.Proposer("m1", "men")
m2 = gsa.Proposer("m2", "men")
w1 = gsa.Responder("w1", "women")
w2 = gsa.Responder("w2", "women")

m1.preferences = (w1, w2, m1)
m2.preferences = (w1, w2, m2)
w1.preferences = (m1, m2, w1)
w2.preferences = (m1, m2, w2)

# Run GS algorithm - always produces a stable matching
algo = gsa.Algorithm([m1, m2], [w1, w2])
algo.execute()

result = gsa.check_stability(algo)
print(f"Is stable: {result.is_stable}")
print(f"Is individually rational: {result.is_individually_rational}")
print(f"Blocking pairs: {result.blocking_pairs}")

# Now create an artificial unstable matching
m1.match = w2
w2.match = m1
m2.match = w1
w1.match = m2

result = gsa.check_stability(algo)
print("\nAfter artificial swap:")
print(f"Is stable: {result.is_stable}")
print(f"Blocking pairs: {result.blocking_pairs}")
