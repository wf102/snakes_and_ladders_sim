import yaml
import numpy as np
import time
import matplotlib.pyplot as plt

from utils import build_matrkov_matrix, finish_prob, simulate_multigame_py, simulate_multigame_cpp, make_plot

rng = np.random.default_rng(seed=42)

max_count = 1000
tot_games = 10000

with open("board.yaml") as f:
    config = yaml.safe_load(f)

size, snakes, ladders = config.values()
jumps = {**(snakes or {}), **(ladders or {})}


# Use Python --------------------------------------------------

# start = time.time()

# counts_py = [0] * (max_count+1)
# for i in range(tot_games):
#     counts_py[simulate_game(size, jumps)] += 1
counts_py = simulate_multigame_py(size, jumps, tot_games, max_count)

# end = time.time()

# dt_py = end-start

# print(f"dt = {dt_py}")




# Use C++ -----------------------------------------------------

# Convert jumps dict to array for C++
# jumps_arr = np.zeros(101, dtype=np.int32)
# for k, v in jumps.items():
#     jumps_arr[k] = v

# start = time.time()
# results = []
# counts_cpp = py_simulate_multigame(100, jumps_arr, tot_games)
# end = time.time()

counts_cpp = simulate_multigame_cpp(size, jumps, tot_games, max_count)

# print(counts[:200])

# dt_cpp = end-start
# print(f"dt = {dt_cpp}")

# print(type(counts_cpp))



# Markov matrix  ----------------------------------------

m_markov = build_matrkov_matrix(size, jumps)

# Cumulative probability of finishing within n rolls
cum_prob = [finish_prob(m_markov, n, size) for n in range(max_count)]

# Probability of finishing after precicely n rolls
prob = np.diff(cum_prob)#, prepend=0)

# Probability of draw (both players finish on same roll)
prob_draw = sum([p*p for p in prob])
print(f"draw prob {prob_draw}")

# Expected rolls to finish
turns = np.arange(1, len(prob)+1)
expected_turns = np.dot(prob, turns)
print(f"expected turns {expected_turns}")






# Plotting

make_plot("Python", counts_py, tot_games, prob, max_count, expected_turns, prob_draw)
make_plot("C++", counts_cpp, tot_games, prob, max_count, expected_turns, prob_draw)
