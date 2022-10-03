# Based on LocalSearch.py

import math
import random
import numpy as np
import copy


def get_probability(delta, x):
    return math.exp((-1*delta) / x)


def column_conflicts(sol):
    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            if (i != j) and (sol[i] == sol[j]):
                conflicts += 1

    return conflicts


def diagonal_conflicts(sol):
    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            deltay = abs(sol[i]-sol[j])
            deltax = abs(i - j)
            if (deltay == deltax and i != j):
                conflicts += 1

    return conflicts


def evalSol(sol):
    return diagonal_conflicts(sol) + column_conflicts(sol)


def swap(sol):
    neighbor = copy.copy(sol)

    index1 = np.random.randint(0, len(sol))
    index2 = np.random.randint(0, len(sol))

    neighbor[index1], neighbor[index2] = neighbor[index2], neighbor[index1]

    return neighbor


def simulatedAnnealing(sol, evalSol, move, max, T0, temperature):
    best_val = evalSol(sol)
    best_sol = copy.deepcopy(sol)
    current_val = evalSol(sol)
    current_sol = copy.deepcopy(sol)
    T = T0

    for i in range(0, max):
        neighbor = move(current_sol)
        newVal = evalSol(neighbor)

        if (newVal - current_val < 0):
            current_sol = copy.deepcopy(neighbor)
            current_val = newVal

            if (current_val < best_val):
                best_sol = copy.deepcopy(current_sol)
                best_val = current_val

        else:
            x = abs(random.random())
            if (x < get_probability(newVal - current_val, T)):
                current_sol = copy.deepcopy(neighbor)
                current_val = newVal
            else:
                neighbor = copy.deepcopy(current_sol)

        T *= temperature
        if (T < 0.1):
            T = T0

    return best_sol, best_val


if __name__ == '__main__':

    sol = [0, 1, 2, 3, 4, 5, 6, 7]

    sol, val = simulatedAnnealing(sol=sol, evalSol=evalSol, move=swap, max=10000, T0=1000, temperature=0.90)

    print(sol)
    print(val)
