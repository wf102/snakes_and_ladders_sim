import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


from multigame import py_simulate_multigame

rng = np.random.default_rng(seed=42)

def simulate_game(size: int, jumps: dict[int, int]) -> int:

    """Simulate a single game of S&L, for a given board (size and set of jumps)"""

    position = 0
    throws = 0

    while position < size:
        
        throws += 1

        # Roll dice
        position = position + rng.integers(1,7)
        
        # Apply snakes & ladders
        position = jumps.get(position, position)

    return throws

def build_matrkov_matrix(size: int, jumps: dict[int, int]) -> np.ndarray:

    """
    Generate Markov matrix for a given board (size and set of jumps)
    Note this includes the zeroth space (off the board).
    """

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


def finish_prob(m_markov: np.ndarray, n: int) -> float:

    """Calculate the probability of finishing in <=n thows, for a given Markov matrix."""

    size = m_markov.shape[0] - 1

    initial_state = np.zeros(size+1)
    initial_state[0] = 1

    final_state = np.linalg.matrix_power(m_markov, n) @ initial_state

    return final_state[-1]

def simulate_multigame_py(size: int, jumps: dict[int, int], tot_games: int) -> list[int]:

    """
    Run multiple S&L games, using python implementation.
    Return a list of counts by index for number of rolls required to finish.
    """

    results = Counter(simulate_game(size, jumps) for _ in range(tot_games))

    return [results[i] for i in range(len(results) + 1)]

def simulate_multigame_cpp(size: int, jumps: dict[int, int], tot_games: int) -> dict[int, int]:

    """
    Run multiple S&L games, using C++ implementation.
    Return a list of counts by index for number of rolls required to finish.
    """

    # Convert jumps dict to array for C++
    jumps_arr = np.zeros(size + 1, dtype=np.int32)
    for k, v in jumps.items():
        jumps_arr[k] = v

    return py_simulate_multigame(size, jumps_arr, tot_games)

def calc_cumulative_prob(m_markov: np.ndarray, threshold: float = 1.0 - 1e-9) -> list[float]:

    """Calculate cumulative probability of finishing after n throws."""

    cum_prob = []
    n = 0
    p = 0

    while p < threshold:
        p = finish_prob(m_markov, n)
        cum_prob.append(p)
        n += 1

    return cum_prob

def make_plot(title: str, counts: list[int], tot_games: int, probs: np.ndarray) -> None:

    """
    Generate and save plot of distribution of number of throw to finish.
    Include expected distribution via Markov matrix.
    """

    expected_n = tot_games * probs

    # Get x upper limit for plot by finding first time prob dips below threshold
    threshold = 1e-4
    peak_idx = np.argmax(probs)
    idx = peak_idx + 1 + np.argmax(probs[peak_idx + 1:] < threshold)

    xlims = (0, idx)
    ylims = (0, 1.1 * expected_n.max())

    plt.style.use('ggplot')

    fig = plt.figure(figsize=(16,10))
    plt.bar(range(len(counts)), counts, width=1.0, alpha=0.75)
    plt.title(f"{title} ({tot_games} games)", loc="left")
    plt.xlabel("Rolls to finish")
    plt.ylabel("Frequency")
    plt.xlim(xlims)
    plt.ylim(ylims)
    plt.plot(expected_n, color = "k", alpha=0.75)
    plt.tight_layout()

    plt.savefig(f"plots/results_{title.lower()}.png")
