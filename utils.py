import numpy as np
from multigame import py_simulate_multigame


rng = np.random.default_rng(seed=42)

def simulate_game(size, jumps):
    position = 0
    throws = 0

    while position < size:
        
        throws += 1

        # Roll dice
        position = position + rng.integers(1,7)
        
        # Apply snakes & ladders
        position = jumps.get(position, position)

    return throws

def build_matrkov_matrix(size, jumps):

    # Trans matrix for rolls on basic board (no snakes & ladders)
    mat_basic = np.zeros((size+1, size+1))
    for i in range(size+1):
        mat_basic[i+1:i+7, i] += 1
    mat_basic = mat_basic/6

    # Handle absorbing state (final square)
    # Assume player does not need to roll exact number to finish
    mat_basic[-1,] = 1.0 - np.sum(mat_basic[:-1,],axis=0)

    # Trans matrix for snakes & ladders
    mat_jumps = np.identity(size+1)
    for k, v in jumps.items():
        mat_jumps[k,k] = 0.0
        mat_jumps[v,k] = 1.0

    # Combined trans matrix
    return np.matmul(mat_jumps, mat_basic)

def finish_prob(m_markov, n, size):
# Calc prob of finish in <=n thows

    initial_state = np.zeros(size+1)
    initial_state[0] = 1

    final_state = np.linalg.matrix_power(m_markov, n) @ initial_state

    return final_state[-1]

def simulate_multigame_py(size, jumps, tot_games, max_count):

    counts = [0] * (max_count+1)
    for i in range(tot_games):
        counts[simulate_game(size, jumps)] += 1

    return counts

def simulate_multigame_cpp(size, jumps, tot_games, max_count):

    jumps_arr = np.zeros(size + 1, dtype=np.int32)
    for k, v in jumps.items():
        jumps_arr[k] = v

    return py_simulate_multigame(size, jumps_arr, tot_games)

