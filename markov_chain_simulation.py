import random

# States
# 0 = Broke
# 1 = Low bankroll
# 2 = Medium bankroll
# 3 = High bankroll
# 4 = Goal reached

def transition(current_state):
    """
    Chooses the next state based only on the current state.
    """ 
    roll = random.random()

    if current_state == 0:
        return 0

    elif current_state == 1:
        if roll < 0.50:
            return 0
        elif roll < 0.80:
            return 1
        else:
            return 2

    elif current_state == 2:
        if roll < 0.20:
            return 1
        elif roll < 0.60:
            return 2
        else:
            return 3

    elif current_state == 3:
        if roll < 0.10:
            return 2
        elif roll < 0.40:
            return 3
        else:
            return 4

    elif current_state == 4:
        return 4


def run_once(starting_state, max_rounds):
    """
    Runs one Markov chain simulation.
    Stops if the player goes broke, reaches the goal,
    or reaches the maximum number of rounds.
    """

    current_state = starting_state
    rounds = 0

    while current_state != 0 and current_state != 4 and rounds < max_rounds:
        current_state = transition(current_state)
        rounds += 1

    return current_state, rounds


def monte_carlo(starting_state, max_rounds, run_amount):
    """
    Repeats the Markov chain many times and records results.
    """

    broke_count = 0
    goal_count = 0
    unfinished_count = 0
    total_rounds = 0

    for i in range(run_amount):
        final_state, rounds = run_once(starting_state, max_rounds)

        total_rounds += rounds

        if final_state == 0:
            broke_count += 1

        elif final_state == 4:
            goal_count += 1

        else:
            unfinished_count += 1

    broke_probability = (broke_count / run_amount) * 100
    goal_probability = (goal_count / run_amount) * 100
    unfinished_probability = (unfinished_count / run_amount) * 100

    average_rounds = total_rounds / run_amount

    return (
        broke_probability,
        goal_probability,
        unfinished_probability,
        average_rounds
    )


print("MARKOV CHAIN CASINO SIMULATION")
print()

print("States:")
print("1 = Low bankroll")
print("2 = Medium bankroll")
print("3 = High bankroll")
print()

starting_state = int(input("Choose starting state (1-3): "))
max_rounds = int(input("Maximum number of rounds per simulation: "))
run_amount = int(input("How many simulations?: "))

broke_probability, goal_probability, unfinished_probability, average_rounds = monte_carlo(
    starting_state,
    max_rounds,
    run_amount
)

print()
print("RESULTS")
print(f"Probability of going broke: {broke_probability:.2f}%")
print(f"Probability of reaching goal: {goal_probability:.2f}%")
print(f"Probability of neither within limit: {unfinished_probability:.2f}%")
print(f"Average rounds played: {average_rounds:.2f}")