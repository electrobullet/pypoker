import poker


def main():
    deck = poker.get_deck()

    computer_hand = poker.get_cards(5, deck)

    user_hand = poker.get_cards(5, deck)
    poker.print_hand(user_hand, 'User hand: ')

    for card in poker.sort_cards(user_hand):

        ans = ''
        while ans not in ['y', 'n']:
            ans = input(f'Replace {card}? [y / n] ')

        if ans == 'y':
            poker.replace_card(user_hand, card, *poker.get_cards(1, deck))

    poker.print_hand(computer_hand, '\nComputer hand: ')
    poker.print_hand(user_hand, 'User hand: ')

    match poker.compare_hands(user_hand, computer_hand):
        case 0:
            print('User wins!')
        case 1:
            print('Computer wins!')
        case 2:
            print('Draw!')


if __name__ == '__main__':
    main()
