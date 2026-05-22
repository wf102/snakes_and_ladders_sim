// #ifndef CALCULATOR_HPP
// #define CALCULATOR_HPP

#include <iostream>
#include <vector>
#include <random>

#include "multigame_core.hpp"

int simulateGame(
    int size,
    const int* transitions
){

    std::random_device rand;
    std::mt19937 gen(rand());
    std::uniform_int_distribution<> dice(1, 6);

    int position = 0;
    int throws = 0;

    while(position < size){

        throws++;

        position += dice(gen);
        
        if (transitions[position] != 0){
            position = transitions[position];
        }
    }
    return throws;
}


std::vector<int> simulateMultigame(
    int size,
    const int* transitions,
    int tot_games
){

    std::vector<int> counts;

    for(int i=0; i<tot_games; i++){

        int n_rolls = simulateGame(size, transitions);
        
        if (n_rolls >= counts.size()) {
            counts.resize(n_rolls + 1, 0);
        }
        
        counts[n_rolls]++;
    }

    return counts;

}