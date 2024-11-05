ROULETTE WHEEL SELECTION 

TOURNAMENT SELECTION

def tournament_selection(population, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        # Randomly choose individuals for the tournament
        tournament = random.sample(population, tournament_size)
        # Select the individual with the best fitness score
        winner = max(tournament, key=calculate_fitness)
        selected.append(winner)
    return selected



STOCHASTIC UNIVERSAL SAMPLING (SUS)

def stochastic_universal_sampling(population):
    fitness_scores = [calculate_fitness(chromosome) for chromosome in population]
    total_fitness = sum(fitness_scores)
    num_individuals = len(population)

    cumulative_probabilities = []
    cumulative_sum = 0.0
    for score in fitness_scores:
        cumulative_sum += score
        cumulative_probabilities.append(cumulative_sum)

    random_start = random.uniform(0, total_fitness / num_individuals)
    interval = total_fitness / num_individuals
    selected = []
    pointer = random_start

    for _ in range(num_individuals):
        while pointer > cumulative_probabilities[0]:
            pointer -= cumulative_probabilities[0]

        for index, cumulative_probability in enumerate(cumulative_probabilities):
            if pointer <= cumulative_probability:
                selected.append(population[index])
                break
        
        pointer += interval

    return selected, fitness_scores
