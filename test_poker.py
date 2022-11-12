from random import shuffle

import pytest
from pytest_dependency import depends

import poker


def get_requested_tests_by_pattern(request, pattern):
    return [item.name for item in request.session.items if f'{pattern}[' in item.name]


def test_get_deck():
    deck = poker.get_deck()
    rank_set = {card[0] for card in deck}
    suit_set = {card[1] for card in deck}

    assert len(set(deck)) == 52
    assert rank_set == {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
    assert suit_set == {'C', 'D', 'H', 'S'}


@pytest.mark.dependency()
@pytest.mark.parametrize(('n', 'deck', 'expected'), [
    pytest.param(
        1,
        [('2', 'C'), ('A', 'H')],
        [('2', 'C')],
        id='0 < n < len(deck)',
    ),
    pytest.param(
        2,
        [('2', 'C'), ('A', 'H')],
        [('2', 'C'), ('A', 'H')],
        id='n = len(deck)',
    ),
])
def test_get_cards(n, deck, expected):
    reference_deck = deck[n:]
    cards = poker.get_cards(n, deck)

    assert cards == expected
    assert deck == reference_deck


@pytest.mark.parametrize(('n', 'deck', 'expected'), [
    pytest.param(
        0,
        [('2', 'C'), ('A', 'H')],
        ValueError('n must be > 0!'),
        id='n = 0',
    ),
    pytest.param(
        -2,
        [('2', 'C'), ('A', 'H')],
        ValueError('n must be > 0!'),
        id='n < 0',
    ),
    pytest.param(
        10,
        [('2', 'C'), ('A', 'H')],
        ValueError('n must be <= len(deck)!'),
        id='n > len(deck)',
    ),
    pytest.param(
        1,
        [],
        ValueError('n must be <= len(deck)!'),
        id='len(deck) = 0',
    ),
])
def test_get_cards_exception(n, deck, expected, request):
    depends(request, get_requested_tests_by_pattern(request, 'test_get_cards'))

    with pytest.raises(Exception) as exc_info:
        poker.get_cards(n, deck)

    assert exc_info.type == type(expected)
    assert str(exc_info.value) == str(expected)


@pytest.mark.dependency()
@pytest.mark.parametrize(('cards', 'expected'), [
    pytest.param(
        [('2', 'C'), ('5', 'H'), ('9', 'D'), ('10', 'S'), ('K', 'S')],
        [('2', 'C'), ('5', 'H'), ('9', 'D'), ('10', 'S'), ('K', 'S')],
        id='sorted',
    ),
    pytest.param(
        [('K', 'S'), ('10', 'S'), ('9', 'D'), ('5', 'H'), ('2', 'C')],
        [('2', 'C'), ('5', 'H'), ('9', 'D'), ('10', 'S'), ('K', 'S')],
        id='reversed',
    ),
    pytest.param(
        [('9', 'C'), ('2', 'H'), ('4', 'D'), ('Q', 'S'), ('A', 'S')],
        [('2', 'H'), ('4', 'D'), ('9', 'C'), ('Q', 'S'), ('A', 'S')],
        id='shuffled',
    ),
])
def test_sort_cards(cards, expected):
    assert poker.sort_cards(cards) == expected


@pytest.mark.dependency()
@pytest.mark.parametrize(('hand', 'expected'), [
    pytest.param(
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        'royal flush',
        id='royal flush',
    ),
    pytest.param(
        [('4', 'C'), ('5', 'C'), ('6', 'C'), ('7', 'C'), ('8', 'C')],
        'straight flush',
        id='straight flush',
    ),
    pytest.param(
        [('2', 'C'), ('7', 'C'), ('8', 'C'), ('J', 'C'), ('A', 'C')],
        'flush',
        id='flush',
    ),
    pytest.param(
        [('4', 'C'), ('4', 'H'), ('4', 'D'), ('4', 'S'), ('A', 'S')],
        'four of a kind',
        id='four of a kind-1',
    ),
    pytest.param(
        [('2', 'C'), ('A', 'C'), ('A', 'D'), ('A', 'H'), ('A', 'S')],
        'four of a kind',
        id='four of a kind-2',
    ),
    pytest.param(
        [('10', 'D'), ('10', 'C'), ('J', 'D'), ('J', 'H'), ('J', 'S')],
        'full house',
        id='full house-1',
    ),
    pytest.param(
        [('3', 'D'), ('3', 'C'), ('3', 'S'), ('J', 'H'), ('J', 'S')],
        'full house',
        id='full house-2',
    ),
    pytest.param(
        [('4', 'D'), ('5', 'C'), ('6', 'H'), ('7', 'S'), ('8', 'S')],
        'straight',
        id='straight',
    ),
    pytest.param(
        [('5', 'C'), ('5', 'H'), ('5', 'D'), ('6', 'H'), ('A', 'S')],
        'three of a kind',
        id='three of a kind-1',
    ),
    pytest.param(
        [('2', 'C'), ('7', 'C'), ('7', 'D'), ('7', 'H'), ('A', 'S')],
        'three of a kind',
        id='three of a kind-2',
    ),
    pytest.param(
        [('2', 'C'), ('5', 'C'), ('A', 'D'), ('A', 'H'), ('A', 'S')],
        'three of a kind',
        id='three of a kind-3',
    ),
    pytest.param(
        [('7', 'H'), ('7', 'C'), ('10', 'D'), ('10', 'H'), ('K', 'S')],
        'two pairs',
        id='two pairs-1',
    ),
    pytest.param(
        [('3', 'S'), ('7', 'H'), ('7', 'C'), ('10', 'D'), ('10', 'H')],
        'two pairs',
        id='two pairs-2',
    ),
    pytest.param(
        [('7', 'H'), ('7', 'C'), ('9', 'S'), ('10', 'D'), ('10', 'H')],
        'two pairs',
        id='two pairs-3',
    ),
    pytest.param(
        [('8', 'H'), ('8', 'C'), ('9', 'D'), ('J', 'H'), ('Q', 'S')],
        'pair',
        id='pair-1',
    ),
    pytest.param(
        [('8', 'H'), ('9', 'C'), ('9', 'D'), ('J', 'H'), ('Q', 'S')],
        'pair',
        id='pair-2',
    ),
    pytest.param(
        [('8', 'H'), ('9', 'C'), ('J', 'D'), ('J', 'H'), ('Q', 'S')],
        'pair',
        id='pair-3',
    ),
    pytest.param(
        [('8', 'H'), ('9', 'C'), ('10', 'D'), ('Q', 'H'), ('Q', 'S')],
        'pair',
        id='pair-4',
    ),
    pytest.param(
        [('5', 'H'), ('6', 'C'), ('9', 'D'), ('Q', 'H'), ('K', 'S')],
        'high card',
        id='high card',
    ),
])
def test_determine_hand(hand, expected, request):
    depends(request, get_requested_tests_by_pattern(request, 'test_sort_cards'))

    shuffle(hand)
    assert poker.determine_hand(hand) == expected


@pytest.mark.parametrize(('hand', 'prefix', 'expected'), [
    pytest.param(
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        'User hand: ',
        "User hand: [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')] - royal flush\n\n",
        id='User hand with royal flush',
    ),
])
def test_print_hand(hand, prefix, expected, request, capsys):
    depends(request, get_requested_tests_by_pattern(request, 'test_determine_hand'))

    shuffle(hand)
    poker.print_hand(hand, prefix)
    captured = capsys.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize(('hand', 'card', 'new_card', 'expected'), [
    pytest.param(
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        ('Q', 'C'),
        ('K', 'H'),
        [('10', 'C'), ('J', 'C'), ('K', 'H'), ('K', 'C'), ('A', 'C')],
        id="('Q', 'C') -> ('K', 'H')",
    ),
])
def test_replace_card(hand, card, new_card, expected):
    poker.replace_card(hand, card, new_card)
    assert hand == expected


@pytest.mark.parametrize(('hand_1', 'hand_2', 'expected'), [
    pytest.param(
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        [('10', 'C'), ('10', 'D'), ('10', 'H'), ('K', 'H'), ('K', 'S')],
        0,
        id='hand_1 > hand_2',
    ),
    pytest.param(
        [('10', 'C'), ('10', 'D'), ('10', 'H'), ('K', 'H'), ('K', 'S')],
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        1,
        id='hand_1 < hand_2',
    ),
    pytest.param(
        [('10', 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C')],
        [('10', 'H'), ('J', 'H'), ('Q', 'H'), ('K', 'H'), ('A', 'H')],
        2,
        id='hand_1 = hand_2',
    ),
])
def test_compare_hands(hand_1, hand_2, expected, request):
    depends(request, get_requested_tests_by_pattern(request, 'test_determine_hand'))

    assert poker.compare_hands(hand_1, hand_2) == expected
