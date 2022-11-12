import pytest
from pytest_dependency import depends

import poker


def get_requested_tests_by_pattern(request, pattern):
    return [item.name for item in request.session.items if f'{pattern}[' in item.name]


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
