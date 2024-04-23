import numpy as np
import random

#Objective function
def F(x):
    return 4 + (2 * x) + (2 * np.sin(20 * x)) - (4 * x**2)

#Mutation operation on the interval [0,1]
def mutate(x, epsilon=0.01):
    mutation_type = np.random.choice(['subtract', 'copy', 'add'], p=[0.3, 0.4, 0.3])
    if mutation_type == 'subtract':
        return max(0, x - epsilon)
    elif mutation_type == 'copy':
        return x
    else:
        return min(1, x + epsilon)

#Crossover operation (Convex combination of 2 individuals for 0 <= a <= 1)
def crossover(x, y, a):
    return (a * x) + ((1 - a) * y) 

#Fitness-proportional selection (roulette selection)
def roulette_selection(population, fitness_values):
    probabilities = fitness_values / np.sum(fitness_values)
    selected_index = np.random.choice(len(population), p=probabilities)
    return population[selected_index]

#Main optimization loop
def optimization(N, epsilon, generations):
    population = np.linspace(0, 1, N)
    for generation in range(generations):
        fitness_values = F(population)
        new_population = []
        for _ in range(N):
            parent1 = roulette_selection(population, fitness_values)
            parent2 = roulette_selection(population, fitness_values)
            a = np.random.rand()  # Crossover parameter
            child = crossover(parent1, parent2, a)
            child = mutate(child, epsilon)
            new_population.append(child)
        population = np.array(new_population)
    best_solution = population[np.argmax(F(population))]
    return best_solution, F(best_solution)

#Code Parameters
N = 10
epsilon = 0.01
generations = [i*0.01 for i in range(1,100)]

# Run optimization to get final results.
best_solution, best_fitness = optimization(N, epsilon, len(generations))
print("Best x:", best_solution)
print("Best F(" + str(best_solution) + "):", best_fitness)