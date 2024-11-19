import json
import random

class Selection:
    def _init_(self):
        pass

    def read_weekly_fitness_from_json(self, file_path):
        """
        Reads weekly fitness scores from the JSON file.
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                # Extract weekly fitness scores
                weekly_fitness_scores = data["weekly_fitness_scores"]
                return weekly_fitness_scores
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: The file at {file_path} is not valid JSON.")
            return {}

    def roulette_wheel_selection(self, remaining_scores, num_select):
        """
        Selects num_select items from the remaining scores using roulette wheel selection.
        """
        if not remaining_scores:
            print("Remaining scores are empty. Cannot perform roulette selection.")
            return {}

        # Calculate the total fitness score
        total_fitness = sum(remaining_scores.values())

        # Create a list of (cumulative probability, week) pairs
        cumulative_probabilities = []
        cumulative_sum = 0
        for week, score in remaining_scores.items():
            cumulative_sum += score
            cumulative_probabilities.append((cumulative_sum, week))

        # Select chromosomes based on roulette wheel selection
        selected_weeks = []
        for _ in range(num_select):
            rand_value = random.uniform(0, total_fitness)
            for cumulative_sum, week in cumulative_probabilities:
                if rand_value <= cumulative_sum:
                    selected_weeks.append(week)
                    break

        # Return the selected weeks with their scores
        return {week: remaining_scores[week] for week in selected_weeks}

    def select_chromosomes(self, weekly_fitness_scores, top_percentage=0.20, roulette_percentage=0.10):
        """
        Selects the top weeks based on their weekly fitness scores and also uses roulette wheel selection.
        """
        if not weekly_fitness_scores:
            print("Weekly fitness scores are empty. Ensure data is loaded correctly.")
            return {}

        # Convert weekly fitness scores to a sorted list of tuples (Week, Score)
        sorted_weekly_scores = sorted(weekly_fitness_scores.items(), key=lambda x: x[1], reverse=True)

        # Determine the number of weeks to select for top selection and roulette wheel selection
        total_weeks = len(sorted_weekly_scores)
        num_top = int(total_weeks * top_percentage)
        num_roulette = int(total_weeks * roulette_percentage)

        # Top 20% selection
        top_selected = sorted_weekly_scores[:num_top]
        top_selected_dict = {week: score for week, score in top_selected}

        # Remaining weeks for roulette selection
        remaining_scores = {week: score for week, score in weekly_fitness_scores.items() if week not in top_selected_dict}

        # Roulette wheel selection
        roulette_selected = self.roulette_wheel_selection(remaining_scores, num_roulette)

        # Combine results
        selected_fitness = {**top_selected_dict, **roulette_selected}

        # Print the selected weeks and scores
        print("\n--- Selected Weeks and Fitness Scores ---")
        for week, score in selected_fitness.items():
            print(f"Week: {week}, Score: {score}")

        return selected_fitness


# Main Execution
if _name_ == "_main_":
    selector = Selection()

    # Read weekly fitness data from the provided JSON file path
    weekly_scores = selector.read_weekly_fitness_from_json("GA/Fitness.json")

    # Select top weeks based on the fitness scores if data is valid
    if weekly_scores:
        selected_chromosomes = selector.select_chromosomes(weekly_scores, top_percentage=0.20, roulette_percentage=0.10)