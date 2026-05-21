# distutils: language = c++

from libcpp.vector cimport vector

cdef extern from "multigame_core.hpp":
    # int simulate_game(
    #     int size,
    #     const int* transtions
    # )
    vector[int] simulateMultigame(
        int size,
        const int* transtions,
        int tot_games
    )

def py_simulate_multigame(int size, int[:] transitions, int tot_games=1):

    return list(simulateMultigame(size, &transitions[0], tot_games))