import random
import statistics

CARD_VALUES = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def create_hidden_cards():
    """
    Shuffles the 13 club values into unknown positions.
    J, Q, K are represented as 0.
    """
    cards = CARD_VALUES.copy()
    random.shuffle(cards)
    return cards


def no_information_strategy(cards):
    """
    Buy no clues and randomly choose two cards.
    """

    chosen_cards = random.sample(cards, 2)

    payout = chosen_cards[0] * chosen_cards[1]
    information_cost = 0

    return payout - information_cost


def one_clue_strategy(cards):
    """
    Buy one $1 difference clue.

    This is only a simple heuristic strategy,
    NOT necessarily the optimal strategy.
    """

    positions = random.sample(range(13), 4)

    card_a = positions[0]
    card_b = positions[1]
    card_c = positions[2]
    card_d = positions[3]

    difference = abs(cards[card_a] - cards[card_b])

    information_cost = 1

    # Simple rule:
    # A large difference suggests A/B contains
    # very different card values.
    #
    # If difference is small, abandon them and
    # choose two new unknown cards.
    if difference >= 6:
        chosen_1 = card_a
        chosen_2 = card_b

    else:
        chosen_1 = card_c
        chosen_2 = card_d

    payout = cards[chosen_1] * cards[chosen_2]

    return payout - information_cost


def two_clue_strategy(cards):
    """
    Buy two difference clues involving three cards.

    Again, this is a fixed heuristic,
    not a mathematically optimal policy.
    """

    positions = random.sample(range(13), 5)

    a = positions[0]
    b = positions[1]
    c = positions[2]
    d = positions[3]
    e = positions[4]

    difference_ab = abs(cards[a] - cards[b])
    difference_ac = abs(cards[a] - cards[c])

    information_cost = 2

    # Simple information-based rule
    if difference_ab >= 6 and difference_ac >= 6:
        chosen_1 = b
        chosen_2 = c

    elif difference_ab >= 6:
        chosen_1 = a
        chosen_2 = b

    elif difference_ac >= 6:
        chosen_1 = a
        chosen_2 = c

    else:
        chosen_1 = d
        chosen_2 = e

    payout = cards[chosen_1] * cards[chosen_2]

    return payout - information_cost


def run_simulation(strategy, run_amount):
    """
    Runs one strategy many times and calculates
    estimated expected value and variance.
    """

    results = []

    for i in range(run_amount):
        cards = create_hidden_cards()
        result = strategy(cards)

        results.append(result)

    average_profit = sum(results) / run_amount
    variance = statistics.pvariance(results)

    return average_profit, variance


run_amount = int(input("How many simulations?: "))


no_info_ev, no_info_variance = run_simulation(
    no_information_strategy,
    run_amount
)

one_clue_ev, one_clue_variance = run_simulation(
    one_clue_strategy,
    run_amount
)

two_clue_ev, two_clue_variance = run_simulation(
    two_clue_strategy,
    run_amount
)


print()
print("NO INFORMATION")
print(f"Estimated EV: ${no_info_ev:.2f}")
print(f"Variance: {no_info_variance:.2f}")

print()
print("ONE $1 CLUE")
print(f"Estimated net EV: ${one_clue_ev:.2f}")
print(f"Variance: {one_clue_variance:.2f}")

print()
print("TWO $1 CLUES")
print(f"Estimated net EV: ${two_clue_ev:.2f}")
print(f"Variance: {two_clue_variance:.2f}")

print()
print("Theoretical blind-play EV: $16.92")