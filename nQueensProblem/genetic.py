import numpy as np
import copy
import random
import math

def generate_pop(variables, dom, pop_size):
    pop = []
    dom_size = len(dom)

    for _ in range(pop_size):
        if (dom_size > 1):
            pop.append([random.choice(dom[j]) for j in range(len(variables))])
        else:
            pop.append([random.choice(dom[0]) for _ in range(len(variables))])

    return pop

def mutation(individual, percentage):
    percentage = percentage / 100 if (percentage > 0) else percentage
    neighbor = copy.deepcopy(individual)

    for _ in range(math.ceil(percentage)):
        idx1 = np.random.randint(0, len(individual))
        idx2 = np.random.randint(0, len(individual))
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

    return neighbor

def crossover(parent1, parent2):
    pop_size = len(parent1)
    mask = np.random.randint(2, size=pop_size)

    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for i in range(pop_size):
        if not mask[i]:
            child1[i] = parent2[i]
            child2[i] = parent1[i]

    return child1, child2

def columns_conflicts(sol):
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
            delta_y = abs(sol[i]-sol[j])
            delta_x = abs(i - j)
            if (delta_y == delta_x and i != j):
                conflicts += 1

    return conflicts

def eval_sol(sol):
    return diagonal_conflicts(sol) + columns_conflicts(sol)

def check_constraints(individual, constraints):
    for constraint in constraints:
        if (constraint(individual)):
            return False

    return True

def rand_select(population, iteration, eval_sol):
    while True:
        for individual in population:
            randomN = abs(random.random())

            if (randomN < math.exp(-1 * eval_sol(individual) / iteration)):
                return individual


def get_best_sol(population, constraints):
    best_sol = copy.deepcopy(population[0])
    best_val = diagonal_conflicts(best_sol) + columns_conflicts(best_sol)

    for sol in population:
        val = diagonal_conflicts(sol) + columns_conflicts(sol)

        if (val < best_val and check_constraints(sol, constraints)):
            best_val = val
            best_sol = sol

    return best_sol, best_val

def genetic_search(variables, domains, constraints, max, size, eval_sol):
    pop = generate_pop(variables, domains, size)

    for i in range(1, max+1):
        for individual in pop:
            if (check_constraints(individual, constraints)):
                return get_best_sol(pop, constraints)

        new_pop = []
        for _ in range(math.floor(size / 2)):
            individual1 = rand_select(pop, i, eval_sol)
            individual2 = rand_select(pop, i, eval_sol)

            new_individual1, new_individual2 = crossover(individual1, individual2)
            new_pop.append(mutation(new_individual1, domains, 40))
            new_pop.append(mutation(new_individual2, domains, 40))

        pop = new_pop

    return get_best_sol(pop, constraints)


if __name__ == '__main__':
    n = int(input("Value of N: "))

    variables = [i for i in range(n)]
    domain = [[i for i in range(n)] for j in range(n)]
    constraints = [columns_conflicts, diagonal_conflicts]

    sol, val = genetic_search(variables, domain, constraints, 10000, 1000, eval_sol)
    print(sol)
    print(val)
