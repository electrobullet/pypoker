from random import shuffle
from typing import List, Tuple

RANK_POWER = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

HAND_POWER = {
    'royal flush': 9,
    'straight flush': 8,
    'four of a kind': 7,
    'full house': 6,
    'flush': 5,
    'straight': 4,
    'three of a kind': 3,
    'two pairs': 2,
    'pair': 1,
    'high card': 0,
}

Card = Tuple[str, str]


def get_deck() -> List[Card]:
    """
    Gets a shuffled deck of cards

    Returns:
        List[Card]: a list of cards
    """
    deck = []

    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        for suit in ['C', 'D', 'H', 'S']:
            deck.append((rank, suit))

    shuffle(deck)

    return deck


def get_cards(n: int, deck: List[Card]) -> List[Card]:
    """
    Gets n cards from a deck

    Args:
        n (int): a number of cards (0 < n <= len(deck))
        deck (List[Card]): a deck of cards

    Returns:
        List[Card]: a list of cards
    """
    if n <= 0:
        raise ValueError('n must be > 0!')

    if n > len(deck):
        raise ValueError('n must be <= len(deck)!')

    cards = deck[:n]
    deck[:] = deck[n:]
    return cards  # noqa: R504


def sort_cards(cards: List[Card]) -> List[Card]:
    """
    Sorts cards by rank

    Args:
        cards (List[Card]): a list of cards

    Returns:
        List[Card]: a sorted list of cards
    """
    return sorted(cards, key=lambda card: RANK_POWER[card[0]])


def determine_hand(hand: List[Card]) -> str:
    """
    Determines a name of a hand

    Args:
        hand (List[Card]): a list of 5 or more cards

    Returns:
        str: name of a hand
    """
    sorted_hand = sort_cards(hand)[-5:]

    ranks = [card[0] for card in sorted_hand]
    suit_set = {card[1] for card in sorted_hand}

    r1, r2, r3, r4, r5 = ranks
    p1, p2, p3, p4, p5 = [RANK_POWER[rank] for rank in ranks]

    if len(suit_set) == 1:
        if ranks == ['10', 'J', 'Q', 'K', 'A']:
            return 'royal flush'

        elif p2 - p1 == p3 - p2 == p4 - p3 == p5 - p4 == 1:
            return 'straight flush'

        else:
            return 'flush'

    if (r1 == r2 == r3 == r4) or (r2 == r3 == r4 == r5):
        return 'four of a kind'

    elif (r1 == r2 == r3 and r4 == r5) or (r1 == r2 and r3 == r4 == r5):
        return 'full house'

    elif p2 - p1 == p3 - p2 == p4 - p3 == p5 - p4 == 1:
        return 'straight'

    elif (r1 == r2 == r3) or (r2 == r3 == r4) or (r3 == r4 == r5):
        return 'three of a kind'

    elif (r1 == r2 and r3 == r4) or (r2 == r3 and r4 == r5) or (r1 == r2 and r4 == r5):
        return 'two pairs'

    elif (r1 == r2) or (r2 == r3) or (r3 == r4) or (r4 == r5):
        return 'pair'

    else:
        return 'high card'


def print_hand(hand: List[Card], prefix: str) -> None:
    """
    Prints a list of cards in following format:
        '{prefix}{sorted hand} - {name of a hand}{postfix}'

    Args:
        hand (List[Card]): a list of cards
    """
    sorted_hand = sort_cards(hand)[-5:]
    print(f'{prefix}{sorted_hand} - {determine_hand(sorted_hand)}\n')


def replace_card(hand: List[Card], card: Card, new_card: Card) -> None:
    """
    Replaces card in a hand with a new one

    Args:
        hand (List[Card]): a list of cards
        card (Card): a replaceable card
        new_card (Card): a replacement card
    """
    hand[hand.index(card)] = new_card


def compare_hands(hand_1: List[Card], hand_2: List[Card]) -> int:
    """
    Compares 2 hands of cards

    Args:
        hand_1 (List[Card]): a list of cards
        hand_2 (List[Card]): a list of cards

    Returns:
        0: hand_1 is stronger than hand_2
        1: hand_2 is stronger than hand_1
        2: hand_1 is equal to hand_2
    """
    hand_1_power = HAND_POWER[determine_hand(hand_1)]
    hand_2_power = HAND_POWER[determine_hand(hand_2)]

    if hand_1_power > hand_2_power:
        return 0

    elif hand_1_power < hand_2_power:
        return 1

    hand_1_ranks = [card[0] for card in sort_cards(hand_1)[-5:]]
    hand_2_ranks = [card[0] for card in sort_cards(hand_2)[-5:]]
    hand_1_sum = sum([RANK_POWER[hand_1_ranks[i]] * pow(10, i) for i in range(5)])
    hand_2_sum = sum([RANK_POWER[hand_2_ranks[i]] * pow(10, i) for i in range(5)])

    if hand_1_sum > hand_2_sum:
        return 0

    elif hand_1_sum < hand_2_sum:
        return 1

    return 2


def main():
    deck = get_deck()

    computer_hand = get_cards(5, deck)

    user_hand = get_cards(5, deck)
    print_hand(user_hand, 'User hand: ')

    for card in sort_cards(user_hand):

        ans = ''
        while ans not in ['y', 'n']:
            ans = input(f'Replace {card}? [y / n] ')

        if ans == 'y':
            replace_card(user_hand, card, *get_cards(1, deck))

    print_hand(computer_hand, '\nComputer hand: ')
    print_hand(user_hand, 'User hand: ')

    match compare_hands(user_hand, computer_hand):
        case 0:
            print('User wins!')
        case 1:
            print('Computer wins!')
        case 2:
            print('Draw!')


if __name__ == '__main__':
    main()
