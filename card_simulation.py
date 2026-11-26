import random
import itertools
import sys

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

def runout(hand1, hand2):
    """
    Gets a sample of 5 random cards to act as a run out
    """
    deck = remove_starting_hand(hand1, hand2)
    runout_cards = random.sample(deck, 5)

    return runout_cards

def make_hands(hand1, hand2, board):
    """
    turns 7 cards from run out and starting hand and makes combinations for 5 card hands
    """

    hand_one_cards = [hand1[0], hand1[1]] + list(board)
    hand_two_cards = [hand2[0], hand2[1]] + list(board)

    hand_one_combinations = list(itertools.combinations(hand_one_cards, 5))
    hand_two_combinations = list(itertools.combinations(hand_two_cards, 5))

    return hand_one_combinations, hand_two_combinations
        
def get_rank_counts(hand):
    """
    Turns 5 card hand into counts to make hand_classification easier
    """
    counts = {}
    for card in hand:
        rank = card[0]
        if rank in counts:
            counts[rank] += 1
        else:
            counts[rank] = 1
    return counts

def is_flush(hand):
    """
    Tests whether a hand is a flush
    """
    first_suit = hand[0][1]
    for i in hand:
        if i[1] != first_suit:
            return False
    return True
        
def is_straight(hand):
    """
    Tests whether a hand is a straight
    """
    numbered_hand = []
    for i in hand:
        numbered_hand.append(rank_values[i[0]])

    numbered_hand.sort()

    if numbered_hand == [2, 3, 4, 5, 14]:
        return True
    for i in range(len(numbered_hand)-1):
        if numbered_hand[i] + 1 != numbered_hand[i + 1]:
            return False
    return True


def hand_classification(hand):
    counts = list(get_rank_counts(hand).values())
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
    numbered_hand = []
    for card in hand:
        numbered_hand.append(rank_values[card[0]])
    numbered_hand.sort()
    if is_straight(hand) and is_flush(hand):
        if numbered_hand == [10,11,12,13,14]:
            hand_type = "Royal Flush"
        else:
            hand_type = "Straight Flush"
    elif 4 in counts:
        hand_type = "Four of a Kind"
    elif 3 in counts and 2 in counts:
        hand_type = "Full House"
    elif is_flush(hand):
        hand_type = "Flush"
    elif is_straight(hand):
        hand_type = "Straight"
    elif 3 in counts:
        hand_type = "Three of a Kind"
    elif counts.count(2) == 2:
        hand_type = "Two Pair"
    elif 2 in counts:
        hand_type = "Pair"
    else:
        hand_type = "High Card"
    return hand_type

def get_tiebreak_value(five_card_hand, classification):
    """
    Helper function for get best hand to break ties when hand classification is the same
    """
    counts = get_rank_counts(five_card_hand)

    numeric_counts = {}

    for rank in counts:
        numeric_counts[rank_values[rank]] = counts[rank]

    if classification == "High Card" or classification == "Flush":
        values = sorted(numeric_counts.keys(), reverse=True)
        return tuple(values)

    elif classification == "Pair":
        pair_rank = 0
        kickers = []

        for rank in numeric_counts:
            if numeric_counts[rank] == 2:
                pair_rank = rank
            else:
                kickers.append(rank)

        kickers.sort(reverse=True)

        return (pair_rank,) + tuple(kickers)

    elif classification == "Two Pair":
        pairs = []
        kicker = 0

        for rank in numeric_counts:
            if numeric_counts[rank] == 2:
                pairs.append(rank)
            else:
                kicker = rank

        pairs.sort(reverse=True)

        return (pairs[0], pairs[1], kicker)

    elif classification == "Three of a Kind":
        triple_rank = 0
        kickers = []

        for rank in numeric_counts:
            if numeric_counts[rank] == 3:
                triple_rank = rank
            else:
                kickers.append(rank)

        kickers.sort(reverse=True)

        return (triple_rank,) + tuple(kickers)

    elif classification == "Straight" or classification == "Straight Flush":
        values = sorted(numeric_counts.keys())

        if values == [2, 3, 4, 5, 14]:
            return (5,)

        return (max(values),)

    elif classification == "Full House":
        triple_rank = 0
        pair_rank = 0

        for rank in numeric_counts:
            if numeric_counts[rank] == 3:
                triple_rank = rank
            elif numeric_counts[rank] == 2:
                pair_rank = rank

        return (triple_rank, pair_rank)

    elif classification == "Four of a Kind":
        four_rank = 0
        kicker = 0

        for rank in numeric_counts:
            if numeric_counts[rank] == 4:
                four_rank = rank
            else:
                kicker = rank

        return (four_rank, kicker)

    elif classification == "Royal Flush":
        return (14,)

def best_hand(hand_combinations, hand_classifications):
    """
    Takes hand classifications and narrows it down to a list of best hand
    """
    result_list = []

    for classification in hand_classifications:
        result_list.append(hand_hierarchy[classification])

    highest_rank = max(result_list)

    best_hands = []

    for i in range(len(result_list)):
        if result_list[i] == highest_rank:
            best_hands.append((
            hand_combinations[i],
            hand_classifications[i]
            ))

    if len(best_hands) == 1:
        return best_hands[0]
    else:
        for hand in best_hands:
            best_hand = best_hands[0]
    best_value = get_tiebreak_value(
        best_hand[0],
        best_hand[1]
    )

    for hand, classification in best_hands[1:]:
        current_value = get_tiebreak_value(
            hand,
            classification
        )

        if current_value > best_value:
            best_hand = (hand, classification)
            best_value = current_value

    return best_hand

def get_board_winner(hand1, hand2, board):
    hand1_combinations, hand2_combinations = make_hands(hand1, hand2, board)
    hand1_classifications = []
    for hand in hand1_combinations:
        hand1_classifications.append(hand_classification(hand))

    hand2_classifications = []
    for hand in hand2_combinations:
        hand2_classifications.append(hand_classification(hand))

    hand1_best = best_hand(hand1_combinations, hand1_classifications)
    hand2_best = best_hand(hand2_combinations, hand2_classifications)

    hand1_value = hand_hierarchy[hand1_best[1]]
    hand2_value = hand_hierarchy[hand2_best[1]]

    if hand1_value > hand2_value:
        return "Hand 1"
    elif hand1_value < hand2_value:
        return "Hand 2"
    else:
        hand1_tiebreak_value = get_tiebreak_value(*hand1_best)
        hand2_tiebreak_value = get_tiebreak_value(*hand2_best)

        if hand1_tiebreak_value > hand2_tiebreak_value:
            return "Hand 1"
        elif hand1_tiebreak_value < hand2_tiebreak_value:
            return "Hand 2"
        else:
            return "Tie"

def run_once(hand1, hand2):
    """
    Runs simulation one time
    """
    board = runout(hand1, hand2)
    return get_board_winner(hand1, hand2, board)

def monte_carlo(hand1, hand2, run_amount):
    """
    Uses run_amount input to input many times and records wins for each hand
    """
    hand1_wins = 0
    hand2_wins = 0
    ties = 0
    i = 1
    while i <= run_amount:
        result = run_once(hand1, hand2)
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
    deck = remove_starting_hand(hand1, hand2)

    hand1_wins = 0
    hand2_wins = 0
    ties = 0

    for board in itertools.combinations(deck, 5):
        result = get_board_winner(hand1, hand2, board)
        if result == "Hand 1":
            hand1_wins += 1
        if result == "Hand 2":
            hand2_wins += 1
        if result == "Tie":
            ties += 1

    theoretical_hand1_percentage = round((hand1_wins/1712304)*100,2)
    theoretical_hand2_percentage = round((hand2_wins/1712304)*100,2)
    theoretical_ties_percentage = round((ties/1712304)*100,2)

    return theoretical_hand1_percentage, theoretical_hand2_percentage, theoretical_ties_percentage



def main():
    print("This is a poker probability calculator")
    print("Insert a 2 poker hands and this program will predict the chances of each hand winning")

    hand1card1rank = input("What is the rank of the first card of your starting hand (Please enter in letters EX: ACE, TWO, KING):").strip().upper()
    hand1card1suit = input("What is the suit of the first card of your starting hand (Please enter in plural form EX: DIAMONDS, SPADES):").strip().upper()
    hand1card2rank = input("What is the rank of the second card of your starting hand (Please enter in letters EX: ACE, TWO, KING):").strip().upper()
    hand1card2suit = input("What is the suit of the second card of your starting hand (Please enter in plural form EX: DIAMONDS, SPADES):").strip().upper()
    hand2card1rank = input("What is the rank of the first card of your opponent's starting hand (Please enter in letters EX: ACE, TWO, KING):").strip().upper()
    hand2card1suit = input("What is the suit of the first card of your opponent's starting hand (Please enter in plural form EX: DIAMONDS, SPADES):").strip().upper()
    hand2card2rank = input("What is the rank of the second card of your opponent's starting hand (Please enter in letters EX: ACE, TWO, KING):").strip().upper()
    hand2card2suit = input("What is the suit of the second card of your opponent's starting hand (Please enter in plural form EX: DIAMONDS, SPADES):").strip().upper()

    hand1_card1 = (hand1card1rank, hand1card1suit)
    hand1_card2 = (hand1card2rank, hand1card2suit)

    hand2_card1 = (hand2card1rank, hand2card1suit)
    hand2_card2 = (hand2card2rank, hand2card2suit)

    hand1 = (hand1_card1, hand1_card2)
    hand2 = (hand2_card1, hand2_card2)

    if not validate_hand(hand1, hand2):
        print("Invalid hand. Please run the program again and make sure conditions are met.")
        sys.exit()

    run_amount = int(input("How many times would you like to simulate?:"))

    hand1_wins, hand2_wins, ties = monte_carlo(hand1, hand2, run_amount)
    hand1_percentage, hand2_percentage, ties_percentage = estimated_probability(hand1_wins, hand2_wins, ties, run_amount)
    # mathematical_hand1_percentage, mathematical_hand2_percentage, mathematical_ties_percentage = theoretical_probability(hand1, hand2)

    print("After running Hand 1:" + str(hand1) + "and Hand 2:" + str(hand2) + " through " + str(run_amount) + " random runouts,")
    print("Hand 1 won " + str(hand1_wins) + " times")
    print("Hand 2 won " + str(hand2_wins) + " times")
    print("There were " + str(ties) + " ties")
    print("Hand 1: " + str(hand1_percentage) + "% Hand 2: " + str(hand2_percentage) + "% Ties: " + str(ties_percentage) + "%")
    # print(f"Mathematically, Hand 1 should win {mathematical_hand1_percentage}%")
    # print(f"Hand 2 should win {mathematical_hand2_percentage}%")
    # print(f"With {mathematical_ties_percentage}% ties")

    """
    print estimated probability function
    print theoretical probability function
    print difference
    """


if __name__ == "__main__":
    main()