import random
import matplotlib.pyplot as plt


def run_once():
    money_tracker = money_start

    while money_tracker > 0 and money_tracker < money_goal:
        up_or_down = random.randint(1, 2)

        if up_or_down == 1:
            money_tracker -= 1
        elif up_or_down == 2:
            money_tracker += 1

    if money_tracker == 0:
        return "Loss"
    else:
        return "Win"


def monte_carlo():
    loss_count = 0
    win_count = 0
    estimated_probabilities = []  # Stores the estimate after each game

    for i in range(run_amount):
        run_result = run_once()

        if run_result == "Loss":
            loss_count += 1
        elif run_result == "Win":
            win_count += 1

        # i starts at 0, so i + 1 is the number of completed games.
        current_probability = win_count / (i + 1) * 100
        estimated_probabilities.append(current_probability)

    return win_count, loss_count, estimated_probabilities


def estimated_probability():
    return win_count / run_amount * 100


def theoretical_probability():
    return money_start / money_goal * 100


def plot_convergence(estimated_probabilities, theoretical):
    game_numbers = range(1, len(estimated_probabilities) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        game_numbers,
        estimated_probabilities,
        color="royalblue",
        label="Estimated win probability"
    )

    plt.axhline(
        y=theoretical,
        color="red",
        linestyle="--",
        label=f"Theoretical win probability: {theoretical:.2f}%"
    )

    plt.xlabel("Number of completed games")
    plt.ylabel("Win probability (%)")
    plt.title(
        f"Gambler's Ruin Convergence: "
        f"Start ${money_start}, Goal ${money_goal}"
    )
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


print("This is a Gambler's Ruin Simulation")
print("Estimate the probability of reaching your goal before losing all your money.")

money_goal = int(input("How much money would you like to have in the end: "))
money_start = int(input("How much money would you like to start with: "))
run_amount = int(input("How many games would you like to simulate: "))

if money_goal <= 0:
    print("The goal must be positive.")
elif money_start < 0 or money_start > money_goal:
    print("Starting money must be between 0 and your goal.")
elif run_amount <= 0:
    print("The number of games must be positive.")
else:
    win_count, loss_count, history = monte_carlo()

    estimated_win_percentage = estimated_probability()
    theoretical_win_percentage = theoretical_probability()

    print(f"\nYou won {win_count} times")
    print(f"You lost {loss_count} times")

    print("\nBased on the simulation,")
    print(f"The probability of a win is {estimated_win_percentage:.2f}%")

    print("\nMathematically,")
    print(f"The probability of a win is {theoretical_win_percentage:.2f}%")

    plot_convergence(history, theoretical_win_percentage)