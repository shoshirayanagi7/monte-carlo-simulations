import random
import itertools
import time
import math

RED = "\033[31m"
RESET = "\033[0m"

suits = ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
ranks = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"]

rank_values = {
"TWO": 2,
"THREE": 3,
"FOUR": 4,
"FIVE": 5,
"SIX": 6,
"SEVEN": 7,
"EIGHT": 8,
"NINE": 9,
"TEN": 10,
"JACK": 11,
"QUEEN": 12,
"KING": 13,
"ACE": 14
}

hand_hierarchy= {
"High Card": 0,
"Pair": 1,
"Two Pair": 2,
"Three of a Kind": 3,
"Straight": 4,
"Flush": 5,
"Full House": 6,
"Four of a Kind": 7,
"Straight Flush": 8,
"Royal Flush": 9
}
def create_deck():
    """
    Creates deck to be used for other functions
    """
    deck = []
    for x in ranks:
        for y in suits:
            card_tuple = (x, y)
            deck.append(card_tuple)
    return deck

def validate_hand(hand1, hand2):
    """
    Makes sure starting hands are possible hands
    """
    starting_hands = [hand1, hand2]
    for hand in starting_hands:
        if hand[0] == hand[1]:
            return False

    if hand1[0] in hand2 or hand1[1] in hand2:
        return False

    for hand in starting_hands:
        if hand[0][0] not in ranks or hand[1][0] not in ranks:
            return False

        if hand[0][1] not in suits or hand[1][1] not in suits:
            return False

    return True

def remove_starting_hand(hand1, hand2):
    """
    removes starting hand from deck so they aren't a part of the draw when the simulation is running
    """
    deck = create_deck()
    deck.remove(hand1[0])
    deck.remove(hand1[1])
    deck.remove(hand2[0])
    deck.remove(hand2[1])

    return deck

def runout(deck):
    """
    Gets a sample of 5 random cards from the remaining deck to act as a run out
    """
    runout_cards = random.sample(deck, 5)

    return runout_cards

def score_hand(five_cards):
    """
    Scores five (value, suit) cards as a tuple: (hand rank, tiebreak values...).
    A bigger tuple is a better hand, so two scores can be compared with > and <.
    """
    values = sorted([card[0] for card in five_cards], reverse=True)

    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    # Five different ranks: the only possible hands are straights, flushes and high card.
    if len(counts) == 5:
        flush = len({card[1] for card in five_cards}) == 1

        straight_high = 0
        if values[0] - values[4] == 4:
            straight_high = values[0]
        elif values == [14, 5, 4, 3, 2]:
            straight_high = 5  # ace-low straight: the ace counts as 1

        if straight_high and flush:
            if straight_high == 14:
                return (hand_hierarchy["Royal Flush"], 14)
            return (hand_hierarchy["Straight Flush"], straight_high)
        elif flush:
            return (hand_hierarchy["Flush"],) + tuple(values)
        elif straight_high:
            return (hand_hierarchy["Straight"], straight_high)
        else:
            return (hand_hierarchy["High Card"],) + tuple(values)

    # A repeated rank: a flush or straight is impossible (one deck has no duplicate cards).
    # Order ranks by how often they appear; values were inserted high to low and sorting is
    # stable, so equal counts stay high to low. Example: K,K,4,4,9 -> (K, 4, 9)
    ordered = tuple(sorted(counts, key=counts.get, reverse=True))
    top_count = counts[ordered[0]]

    if len(counts) == 2:
        if top_count == 4:
            return (hand_hierarchy["Four of a Kind"],) + ordered
        return (hand_hierarchy["Full House"],) + ordered
    elif len(counts) == 3:
        if top_count == 3:
            return (hand_hierarchy["Three of a Kind"],) + ordered
        return (hand_hierarchy["Two Pair"],) + ordered
    else:
        return (hand_hierarchy["Pair"],) + ordered

def best_score(seven_cards):
    """
    Returns the best score among the 21 five-card combinations of seven cards
    """
    return max(score_hand(five_cards) for five_cards in itertools.combinations(seven_cards, 5))

def to_numeric(cards):
    """
    Converts ("ACE", "SPADES") style cards to (14, "SPADES")
    """
    return [(rank_values[rank], suit) for rank, suit in cards]

def get_board_winner(hand1, hand2, board):
    numeric_board = to_numeric(board)
    hand1_score = best_score(to_numeric(hand1) + numeric_board)
    hand2_score = best_score(to_numeric(hand2) + numeric_board)

    if hand1_score > hand2_score:
        return "Hand 1"
    elif hand1_score < hand2_score:
        return "Hand 2"
    else:
        return "Tie"

def run_once(deck, hand1, hand2):
    """
    Runs simulation one time
    """
    board = runout(deck)
    return get_board_winner(hand1, hand2, board)

def monte_carlo(hand1, hand2, run_amount):
    """
    Uses run_amount input to input many times and records wins for each hand
    """
    hand1_wins = 0
    hand2_wins = 0
    ties = 0
    deck = remove_starting_hand(hand1, hand2)  # built once; random.sample never changes it
    i = 1
    while i <= run_amount:
        result = run_once(deck, hand1, hand2)
        if result == "Hand 1":
            hand1_wins+=1
        elif result == "Hand 2":
            hand2_wins +=1
        elif result == "Tie":
            ties+=1
        i += 1
    return hand1_wins, hand2_wins, ties

def estimated_probability(hand1_wins, hand2_wins, ties, run_amount):
    hand1_percentage = round((hand1_wins/run_amount)*100,2)
    hand2_percentage = round((hand2_wins/run_amount)*100,2)
    ties_percent = round((ties/run_amount)*100,2)
    return hand1_percentage, hand2_percentage, ties_percent 

def theoretical_probability(hand1, hand2):
    """
    Checks every possible 5-card board (1,712,304 of them) and returns the exact
    win/tie percentages. Prints a progress update every 10% because it takes about a minute.
    """
    deck = remove_starting_hand(hand1, hand2)
    total_boards = math.comb(len(deck), 5)  # 48 choose 5 = 1,712,304

    hand1_wins = 0
    hand2_wins = 0
    ties = 0
    last_tenth_printed = 0
    start_time = time.perf_counter()

    for board_count, board in enumerate(itertools.combinations(deck, 5), start=1):
        result = get_board_winner(hand1, hand2, board)
        if result == "Hand 1":
            hand1_wins += 1
        if result == "Hand 2":
            hand2_wins += 1
        if result == "Tie":
            ties += 1

        tenth = board_count * 10 // total_boards  # 0..10: how many tenths are done
        if tenth > last_tenth_printed:
            last_tenth_printed = tenth
            elapsed_seconds = time.perf_counter() - start_time
            print(f"  {tenth * 10}% done ({board_count:,} of {total_boards:,} boards, {elapsed_seconds:.1f} s)")

    theoretical_hand1_percentage = round((hand1_wins/1712304)*100,2)
    theoretical_hand2_percentage = round((hand2_wins/1712304)*100,2)
    theoretical_ties_percentage = round((ties/1712304)*100,2)

    return theoretical_hand1_percentage, theoretical_hand2_percentage, theoretical_ties_percentage


def get_int_input(prompt, min_value, max_value=None):
    """
    Keeps asking until the user types a whole number in the allowed range.
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(f"{RED}Please enter a whole number.{RESET}")
            continue

        if value < min_value or (max_value is not None and value > max_value):
            if max_value is None:
                print(f"{RED}Please enter a number that is at least {min_value}.{RESET}")
            else:
                print(f"{RED}Please enter a number between {min_value} and {max_value}.{RESET}")
            continue

        return value


def get_optional_seed(prompt):
    """
    Asks for a random seed. Pressing Enter returns None (a normal random run).
    """
    while True:
        text = input(prompt).strip()
        if text == "":
            return None
        try:
            return int(text)
        except ValueError:
            print(f"{RED}Please enter a whole number, or press Enter for a random run.{RESET}")


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
        print(f"{RED}Please enter y or n.{RESET}")


def print_comparison_table(simulated, exact):
    """
    Prints simulated %, exact %, and absolute error side by side.
    """
    print(f"{'':<8}{'Simulated %':>13}{'Exact %':>11}{'Abs. error':>13}")
    for label, simulated_percentage, exact_percentage in zip(["Hand 1", "Hand 2", "Ties"], simulated, exact):
        error = abs(simulated_percentage - exact_percentage)
        print(f"{label:<8}{simulated_percentage:>13.2f}{exact_percentage:>11.2f}{error:>13.2f}")


def get_card(position, owner, chosen_cards):
    """
    Asks for one card's rank and suit, re-asking only the part that is invalid.
    If the card was already chosen, asks for the whole card again.
    """
    while True:
        while True:
            rank = input(f"What is the rank of the {position} card of {owner} starting hand (Please enter in letters EX: ACE, TWO, KING):").strip().upper()
            if rank in ranks:
                break
            print(f"{RED}Invalid rank. Please enter one of: {', '.join(ranks)}.{RESET}")

        while True:
            suit = input(f"What is the suit of the {position} card of {owner} starting hand (Please enter in plural form EX: DIAMONDS, SPADES):").strip().upper()
            if suit in suits:
                break
            print(f"{RED}Invalid suit. Please enter one of: {', '.join(suits)}.{RESET}")

        card = (rank, suit)
        if card in chosen_cards:
            print(f"{RED}That card has already been chosen. Please enter a different card.{RESET}")
            continue

        return card


def get_hands():
    """
    Asks for both starting hands one card at a time.
    """
    chosen_cards = []
    for owner in ["your", "your opponent's"]:
        for position in ["first", "second"]:
            chosen_cards.append(get_card(position, owner, chosen_cards))

    hand1 = (chosen_cards[0], chosen_cards[1])
    hand2 = (chosen_cards[2], chosen_cards[3])
    return hand1, hand2


def main():
    print("This is a poker probability calculator")
    print("Insert a 2 poker hands and this program will predict the chances of each hand winning")

    hand1, hand2 = get_hands()

    run_amount = get_int_input("How many times would you like to simulate?: ", 1)
    seed = get_optional_seed("Random seed (press Enter for a random run): ")

    if seed is not None:
        random.seed(seed)
        print(f"Using seed {seed}")

    start_time = time.perf_counter()
    hand1_wins, hand2_wins, ties = monte_carlo(hand1, hand2, run_amount)
    elapsed_seconds = time.perf_counter() - start_time

    hand1_percentage, hand2_percentage, ties_percentage = estimated_probability(hand1_wins, hand2_wins, ties, run_amount)

    print("After running Hand 1:" + str(hand1) + "and Hand 2:" + str(hand2) + " through " + str(run_amount) + " random runouts,")
    print("Hand 1 won " + str(hand1_wins) + " times")
    print("Hand 2 won " + str(hand2_wins) + " times")
    print("There were " + str(ties) + " ties")
    print("Hand 1: " + str(hand1_percentage) + "% Hand 2: " + str(hand2_percentage) + "% Ties: " + str(ties_percentage) + "%")
    print(f"Simulation took {elapsed_seconds:.2f} seconds")

    if get_yes_no("Calculate exact odds? (takes about a minute) (y/n): "):
        print("Checking every possible board...")
        start_time = time.perf_counter()
        exact = theoretical_probability(hand1, hand2)
        exact_seconds = time.perf_counter() - start_time
        print(f"Exact calculation took {exact_seconds:.1f} seconds")
        print()
        print_comparison_table((hand1_percentage, hand2_percentage, ties_percentage), exact)


if __name__ == "__main__":
    main()