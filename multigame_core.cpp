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

    std::vector<int> counts(1001, 0);

    // std::cout << "C++!!!!!!!!!!!!!!!!" << std::endl;
    // std::cout << tot_games << std::endl;
    // int throws[50];
    // transitions[10] = 50;
    // transitions[60] = 20;
    // tot_games = 1000000;
    
    int tot_throws = 0;
    for(int i=0; i<tot_games; i++){
        // throws[i] = simulate_game(100, transitions);
        // std::cout << i << std::endl;
        counts[simulateGame(100, transitions)] += 1;
    }

    return counts;

}



 




// std::vector<int> simulate_many_games(
//     int size,
//     const std::vector<int>& transitions,
//     int n_games
// ){
//     for (int i=1; i<n_games+1; i++){

//     }
// }

