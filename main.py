import yaml
import numpy as np
import time

from utils import build_matrkov_matrix, simulate_multigame_py, simulate_multigame_cpp, calc_cumulative_prob, make_plot

rng = np.random.default_rng(seed=42)

tot_games = 100000
board_file = "board.yaml"


def main():
    
    """
    Import the specific game of Snakes & Ladders specified in the config.
    Play tot_games using Python and C++, and store number of rolls to finish.
    Generate Markov matrix and use it to derive expected values for numbe rof rolls to finish.
    Plot distribution of rolls compared to expected distribution.
    """

    # Import board ------------------------------------------------

    with open(board_file) as f:
        config = yaml.safe_load(f)

    size, snakes, ladders = config.values()
    jumps = {**(snakes or {}), **(ladders or {})}


    # Use Python --------------------------------------------------

    start = time.time()
    counts_py = simulate_multigame_py(size, jumps, tot_games)
    end = time.time()
    dt_py = end-start


    # Use C++ -----------------------------------------------------

    start = time.time()
    counts_cpp = simulate_multigame_cpp(size, jumps, tot_games)
    end = time.time()
    dt_cpp = end-start


    # Markov matrix  ----------------------------------------------

    m_markov = build_matrkov_matrix(size, jumps)

    # Cumulative probability of finishing within n rolls
    cum_prob = calc_cumulative_prob(m_markov)

    # Probability of finishing after precicely n rolls
    probs = np.diff(cum_prob, prepend=0)

    # Probability of draw with two players (both players finish on same roll)
    prob_draw = sum([p*p for p in probs])

    # Expected rolls to finish
    expected_turns = np.dot(probs, np.arange(len(probs)))


    # Plotting ----------------------------------------------------

    make_plot("Python", counts_py, tot_games, probs)
    make_plot("C++", counts_cpp, tot_games, probs)


    # Print summary stats  ----------------------------------------

    text = f"""
    ============ Summary stats ============

    Number of games:           {tot_games}
    Expected rolls to finish:  {expected_turns:.2f}
    Probability of 2p draw:    {prob_draw:.4f}

    Time to play {tot_games} games:
    Python:      {dt_py:.2f} s
    C++:         {dt_cpp:.2f} s
    C++ speedup: {dt_py/dt_cpp:.2f}x

    =======================================
    """

    print(text)


if __name__ == "__main__":
    main()
