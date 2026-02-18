"""Checking stability of a matching."""

from gale_shapley import Algorithm, Proposer, Responder, check_stability

# Create a scenario
m1 = Proposer("m1", "men")
m2 = Proposer("m2", "men")
w1 = Responder("w1", "women")
w2 = Responder("w2", "women")

m1.preferences = (w1, w2, m1)
m2.preferences = (w1, w2, m2)
w1.preferences = (m1, m2, w1)
w2.preferences = (m1, m2, w2)

# Run GS algorithm - always produces a stable matching
algo = Algorithm([m1, m2], [w1, w2])
algo.execute()

result = check_stability(algo)
print(f"Is stable: {result.is_stable}")
print(f"Is individually rational: {result.is_individually_rational}")
print(f"Blocking pairs: {result.blocking_pairs}")

# Now create an artificial unstable matching
m1.match = w2
w2.match = m1
m2.match = w1
w1.match = m2

result = check_stability(algo)
print("\nAfter artificial swap:")
print(f"Is stable: {result.is_stable}")
print(f"Blocking pairs: {result.blocking_pairs}")
