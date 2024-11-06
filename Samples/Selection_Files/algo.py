#ROULETTE WHEEL SELECTION 
 def roulette_wheel_selection(self, chromosomes, selection_ratio=0.2):
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in chromosomes]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        selection_count = max(1, int(len(chromosomes) * selection_ratio))
        top_chromosomes = [fitness_scores[i][0] for i in range(selection_count)]
        return top_chromosomes



#TOURNAMENT SELECTION
def select_top_20_percent_tournament(self, chromosomes, tournament_size=3, selection_ratio=0.2):
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in chromosomes]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        selected_chromosomes = []
        num_selected = int(len(chromosomes) * selection_ratio)

        for _ in range(num_selected):
            tournament_contestants = random.sample(fitness_scores, tournament_size)
            winner = max(tournament_contestants, key=lambda x: x[1])
            selected_chromosomes.append(winner[0])
        return selected_chromosomes



#STOCHASTIC UNIVERSAL SAMPLING (SUS)
  def select_top_20_percent_sus(self, chromosomes, selection_ratio=0.2):
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in chromosomes]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        total_fitness = sum(score for _, score in fitness_scores)
        pick_size = int(len(chromosomes) * selection_ratio)
        pointers = [random.uniform(0, total_fitness) for _ in range(pick_size)]
        selected_chromosomes = []
        current_index = 0
        cumulative_fitness = 0
        for pointer in pointers:
            while cumulative_fitness < pointer:
                cumulative_fitness += fitness_scores[current_index][1]
                current_index += 1
            selected_chromosomes.append(fitness_scores[current_index - 1][0])

        return selected_chromosomes



#RANK SELECTION
def select_top_20_percent_rank(self, chromosomes, selection_ratio=0.2):
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in chromosomes]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        ranked_chromosomes = [chromosome for chromosome, _ in fitness_scores]
        total_chromosomes = len(ranked_chromosomes)
        num_selected = int(total_chromosomes * selection_ratio)
        # Rank-based selection
        selected_chromosomes = []
        for i in range(num_selected):
            selected_chromosomes.append(ranked_chromosomes[i])

        return selected_chromosomes



#RANDOM SELECTION
 def select_random(self, chromosomes, selection_ratio=0.2):
        num_chromosomes = len(chromosomes)
        num_selected = int(num_chromosomes * selection_ratio)
        # Random selection
        selected_chromosomes = random.sample(chromosomes, num_selected)
        return selected_chromosomes



#ELITISM SELECTION
  def select_elitism(self, chromosomes, fitness_scores, elitism_ratio=0.2):
        num_chromosomes = len(chromosomes)
        num_selected = int(num_chromosomes * elitism_ratio)
        # Get the indices of the chromosomes with the highest fitness
        sorted_indices = sorted(range(num_chromosomes), key=lambda i: fitness_scores[i], reverse=True)
        elite_chromosomes = [chromosomes[i] for i in sorted_indices[:num_selected]]
        return elite_chromosomes

