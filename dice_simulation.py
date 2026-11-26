import os
import random
import matplotlib.pyplot as plt


def dice_value():
    """
    Creates a random value between 1 and 6.
    """
    return random.randint(1, 6)


def simulate_dice_rolls():
    """
    Simulates rolling two dice and returns their sum.
    """
    roll_result_one = dice_value()
    roll_result_two = dice_value()
    dice_combined_value = roll_result_one + roll_result_two
    return dice_combined_value


def get_match_count(target, run_amount):
    """
    Counts matches and saves the estimated probability after each trial.
    """
    match_count = 0
    estimated_probabilities = []  # stores the running estimates

    # i goes 1, 2, ..., run_amount (range stops just before run_amount + 1).
    for i in range(1, run_amount + 1):
        dice_check_value = simulate_dice_rolls()

        if dice_check_value == target:
            match_count += 1

        # Save an estimate after EVERY trial, including non-matches.
        current_probability = match_count / i * 100
        estimated_probabilities.append(current_probability)

    return match_count, estimated_probabilities


def get_estimated_probability(target, run_amount):
    """
    Returns the final estimated percentage and the running estimates.
    """
    match_count, estimated_probabilities = get_match_count(target, run_amount)
    percent_estimated = match_count / run_amount * 100

    return percent_estimated, estimated_probabilities


def get_theoretical_probability(target):
    """
    Calculates the exact probability as a percentage.
    """
    matches_count = 0
    total_combinations = 0

    for d1 in range(1, 7):
        for d2 in range(1, 7):
            dice_total = d1 + d2
            total_combinations += 1

            if dice_total == target:
                matches_count += 1

    return matches_count / total_combinations * 100


def get_int_input(prompt, min_value, max_value=None):
    """
    Keeps asking until the user types a whole number in the allowed range.
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if value < min_value or (max_value is not None and value > max_value):
            if max_value is None:
                print(f"Please enter a number that is at least {min_value}.")
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
            continue

        return value


def print_error_table(target, theoretical):
    """
    Runs a fresh simulation at several sizes and shows how far
    each estimate is from the theoretical probability.
    """
    trial_sizes = [100, 1_000, 10_000, 100_000]

    print()
    print(f"Error at different simulation sizes (target sum {target}):")
    print(f"{'Trials':>10} | {'Estimated %':>11} | {'Theoretical %':>13} | {'Absolute error':>14}")
    print("-" * 58)

    for trials in trial_sizes:
        estimated, _ = get_estimated_probability(target, trials)
        absolute_error = abs(estimated - theoretical)
        print(f"{trials:>10,} | {estimated:>11.2f} | {theoretical:>13.2f} | {absolute_error:>14.2f}")


def get_yes_no(prompt):
    """
    Keeps asking until the user types y or n. Returns True for yes.
    If there is no more input (for example, piped answers ran out), counts as no.
    """
    while True:
        try:
            answer = input(prompt).strip().lower()
        except EOFError:
            print()
            return False
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def plot_convergence(estimated_probabilities, theoretical_probability, target, show_plot):
    """
    Plots the running estimates against the theoretical probability
    and saves the graph to images/dice_convergence.png.
    """
    trial_numbers = range(1, len(estimated_probabilities) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        trial_numbers,
        estimated_probabilities,
        label="Estimated probability",
        color="royalblue"
    )

    plt.axhline(
        y=theoretical_probability,
        color="red",
        linestyle="--",
        label=f"Theoretical probability: {theoretical_probability:.2f}%"
    )

    plt.xlabel("Number of trials")
    plt.ylabel("Probability (%)")
    plt.title(f"Monte Carlo Convergence: Rolling a Sum of {target}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    os.makedirs("images", exist_ok=True)
    save_path = "images/dice_convergence.png"
    plt.savefig(save_path)
    if show_plot:
        plt.show()
    plt.close()

    print()
    print(f"Convergence plot saved to {save_path}")


def main():
    print("This is a Monte Carlo Dice Simulation")

    target = get_int_input("Input a number between 2 and 12: ", 2, 12)
    run_amount = get_int_input("Input the number of simulations: ", 1)

    estimated, history = get_estimated_probability(target, run_amount)
    theoretical = get_theoretical_probability(target)
    absolute_error = abs(estimated - theoretical)

    print(
        f"We ran {run_amount} simulations to calculate "
        f"the probability of rolling a sum of {target}"
    )
    print(f"The Estimated Probability is {estimated:.2f}%")
    print(f"The Theoretical Probability is {theoretical:.2f}%")
    print(f"Absolute error: {absolute_error:.2f} percentage points")

    print_error_table(target, theoretical)
    show_plot = get_yes_no("Show the plot? (y/n): ")
    plot_convergence(history, theoretical, target, show_plot)


if __name__ == "__main__":
    main()
