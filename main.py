#Get libraries
import random
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def update_progress(current, total, prefix="Simulation progress", bar_width=40):
    progress = current / total
    filled = int(bar_width * progress)
    bar = "#" * filled + "-" * (bar_width - filled)
    print(
        f"\r{prefix}: [{bar}] {progress * 100:6.2f}% ({current}/{total})",
        end="",
        flush=True,
    )
    if current == total:
        print()


class SimulationProgress:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current = 0
        self.progress_interval = max(1, total_steps // 100)
        self.tqdm_bar = None

        if tqdm is not None:
            self.tqdm_bar = tqdm(total=total_steps, desc="Simulation", unit="step")

    def advance(self, step_count=1):
        self.current += step_count
        if self.tqdm_bar is not None:
            self.tqdm_bar.update(step_count)
            return

        if self.current % self.progress_interval == 0 or self.current == self.total_steps:
            update_progress(self.current, self.total_steps)

    def close(self):
        if self.tqdm_bar is not None:
            self.tqdm_bar.close()

#Input
num_trials = int(input("Number of trials: "))
while num_trials <= 0:
    print("Please set the number of trials to a number greater than 0.")
    num_trials = int(input("Number of trials: "))

correctness_start_range = float(input("Predictor Correctness Start Range: "))
correctness_end_range = float(input("Predictor Correctness End Range: "))
while correctness_end_range <= correctness_start_range: 
    print("Please input the start range to be less than the end range.")
    correctness_start_range = float(input("Predictor Correctness Start Range: "))
    correctness_end_range = float(input("Predictor Correctness End Range: "))

while correctness_end_range > 1 or correctness_end_range < 0 or correctness_start_range > 1 or correctness_start_range < 0: 
    print("Please input a range between 0 and 1.")
    correctness_start_range = float(input("Predictor Correctness Start Range: "))
    correctness_end_range = float(input("Predictor Correctness End Range: "))

#Graph Values Input
lowest_value = input("Would you like to include the lowest value in the graph (Y/N)").lower()
while lowest_value != "y" and lowest_value != "n":
    print("Please input Y/N")
    lowest_value = input("Would you like to include the lowest value in the graph (Y/N)").lower()

highest_value = input("Would you like to include the highest value in the graph (Y/N)").lower()
while highest_value != "y" and highest_value != "n":
    print("Please input Y/N")
    highest_value = input("Would you like to include the highest value in the graph (Y/N)").lower()

mean_value = input("Would you like to include the mean value in the graph (Y/N)").lower()
while mean_value != "y" and mean_value != "n":
    print("Please input Y/N")
    mean_value = input("Would you like to include the mean value in the graph (Y/N)").lower()

def newcombs_paradox_simulation(num_trials):
    one_box_min = None
    one_box_max = None
    one_box_sum = 0

    two_box_min = None
    two_box_max = None
    two_box_sum = 0

    total_steps = num_trials * 2
    progress = SimulationProgress(total_steps)

    #For one box
    for _ in range(1, num_trials + 1):
        probability = random.uniform(correctness_start_range, correctness_end_range) # Probabilty of the predictor being correct

        expected_outcome = 1000000 * probability #calculate expected outcome by multiplying the hoped outcome by probability
        expected_outcome_round = round(expected_outcome) #round to whole number

        if one_box_min is None or expected_outcome_round < one_box_min:
            one_box_min = expected_outcome_round
        if one_box_max is None or expected_outcome_round > one_box_max:
            one_box_max = expected_outcome_round
        one_box_sum += expected_outcome_round

        progress.advance()

    #For two box
    for _ in range(1, num_trials + 1):
        probability = 1 - random.uniform(correctness_start_range, correctness_end_range) # Probability of the predictor being incorrect

        expected_outcome = 1001000 * probability #calculate expected outcome by multiplying the hoped outcome by probability
        expected_outcome_round = round(expected_outcome) #round to whole number

        if two_box_min is None or expected_outcome_round < two_box_min:
            two_box_min = expected_outcome_round
        if two_box_max is None or expected_outcome_round > two_box_max:
            two_box_max = expected_outcome_round
        two_box_sum += expected_outcome_round

        progress.advance()

    progress.close()

    #Generate Graph
    categories = [] #initialise categories

    vals_one = []
    vals_two = []

    if lowest_value == "y":
        categories.append("Lowest Value") #Add lowest value to categories
        vals_one.append(one_box_min)
        vals_two.append(two_box_min)

    if highest_value == "y":
        categories.append("Highest Value") #Add highest value to categories
        vals_one.append(one_box_max)
        vals_two.append(two_box_max)

    if mean_value == "y":
        categories.append("Mean Value")

        val_one_mean = one_box_sum / num_trials
        val_one_mean_round = round(val_one_mean)
        vals_one.append(val_one_mean_round)

        val_two_mean = two_box_sum / num_trials
        val_two_mean_round = round(val_two_mean)
        vals_two.append(val_two_mean_round)

    if not categories:
        print("No graph values selected. Please enable at least one of lowest/highest/mean.")
        return

    print("\n\nResults:")
    print("Categories:", categories)
    print("One box values:", vals_one)
    print("Two box values:", vals_two)

    w, x = 0.4, np.arange(len(categories))

    fig, ax = plt.subplots()
    ax.bar(x - w/2, vals_one, width=w, label='One Box')
    ax.bar(x + w/2, vals_two, width=w, label='Two Box')

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('Expected Outcome')
    ax.set_title('One Box vs Two Box Comparison')
    ax.legend()

    plt.show()


newcombs_paradox_simulation(num_trials)
