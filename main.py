import yaml
import numpy as np
import time
import matplotlib.pyplot as plt

from utils import build_matrkov_matrix, finish_prob, simulate_multigame_py, simulate_multigame_cpp, make_plot

rng = np.random.default_rng(seed=42)

max_count = 1000
tot_games = 100000

with open("board.yaml") as f:
    config = yaml.safe_load(f)

size, snakes, ladders = config.values()
jumps = {**(snakes or {}), **(ladders or {})}


# Use Python --------------------------------------------------

# start = time.time()
counts_py = simulate_multigame_py(size, jumps, tot_games, max_count)
# end = time.time()
# dt_py = end-start




# Use C++ -----------------------------------------------------

# start = time.time()
counts_cpp = simulate_multigame_cpp(size, jumps, tot_games, max_count)
# end = time.time()
# dt_cpp = end-start



# Markov matrix  ----------------------------------------

m_markov = build_matrkov_matrix(size, jumps)

# Cumulative probability of finishing within n rolls
cum_prob = [finish_prob(m_markov, n, size) for n in range(max_count)]

# Probability of finishing after precicely n rolls
prob = np.diff(cum_prob, prepend=0)

# Probability of draw (both players finish on same roll)
prob_draw = sum([p*p for p in prob])
print(f"draw prob {prob_draw}")

# Expected rolls to finish
turns = np.arange(0, len(prob))

expected_turns = np.dot(prob, turns)
print(f"expected turns {expected_turns}")


# Plotting

make_plot("Python", counts_py, tot_games, prob, max_count, expected_turns, prob_draw)
make_plot("C++", counts_cpp, tot_games, prob, max_count, expected_turns, prob_draw)
