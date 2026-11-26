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
    rollResultOne = dice_value()
    rollResultTwo = dice_value()
    diceCombinedValue = rollResultOne + rollResultTwo
    return diceCombinedValue


def getMatchCount(target, runAmount):
    """
    Counts matches and saves the estimated probability after each trial.
    """
    matchCount = 0
    estimatedProbabilities = []  # NEW: stores the running estimates
    i = 1

    while i <= runAmount:
        diceCheckValue = simulate_dice_rolls()

        if diceCheckValue == target:
            matchCount += 1

        # Save an estimate after EVERY trial, including non-matches.
        currentProbability = matchCount / i * 100
        estimatedProbabilities.append(currentProbability)

        i += 1

    return matchCount, estimatedProbabilities


def getEstimatedProbability(target, runAmount):
    """
    Returns the final estimated percentage and the running estimates.
    """
    matchCount, estimatedProbabilities = getMatchCount(target, runAmount)
    percentEstimated = matchCount / runAmount * 100

    return percentEstimated, estimatedProbabilities


def getTheoreticalProbability(target):
    """
    Calculates the exact probability as a percentage.
    """
    matchesCount = 0
    totalCombinations = 0

    for d1 in range(1, 7):
        for d2 in range(1, 7):
            diceTotal = d1 + d2
            totalCombinations += 1

            if diceTotal == target:
                matchesCount += 1

    return matchesCount / totalCombinations * 100


def plotConvergence(estimatedProbabilities, theoreticalProbability, target):
    """
    Plots the running estimates against the theoretical probability.
    """
    trialNumbers = range(1, len(estimatedProbabilities) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        trialNumbers,
        estimatedProbabilities,
        label="Estimated probability",
        color="royalblue"
    )

    plt.axhline(
        y=theoreticalProbability,
        color="red",
        linestyle="--",
        label=f"Theoretical probability: {theoreticalProbability:.2f}%"
    )

    plt.xlabel("Number of trials")
    plt.ylabel("Probability (%)")
    plt.title(f"Monte Carlo Convergence: Rolling a Sum of {target}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


print("This is a Monte Carlo Dice Simulation")

target = int(input("Input a number between 2 and 12: "))

if 2 <= target <= 12:
    runAmount = int(input("Input the number of simulations: "))

    if runAmount > 0:
        estimated, history = getEstimatedProbability(target, runAmount)
        theoretical = getTheoreticalProbability(target)

        print(
            f"We ran {runAmount} simulations to calculate "
            f"the probability of rolling a sum of {target}"
        )
        print(f"The Estimated Probability is {estimated:.2f}%")
        print(f"The Theoretical Probability is {theoretical:.2f}%")

        plotConvergence(history, theoretical, target)
    else:
        print("Invalid input, the number of simulations must be positive.")
else:
    print("Invalid input, the number must be between 2 and 12.")