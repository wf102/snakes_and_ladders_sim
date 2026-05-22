from libcpp.vector cimport vector

cdef extern from "multigame_core.hpp":

    vector[int] simulateMultigame(
        int size,
        const int* transtions,
        int tot_games
    )

def simulate_multigame_pyx(int size, int[:] transitions, int tot_games=1):

    return list(simulateMultigame(size, &transitions[0], tot_games))