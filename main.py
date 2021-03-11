import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.deck.append(created_card)

    def __str__(self):
        deck_comp = ' '
        for card in self.deck:
            deck_comp += card.__str__() + '\n'
        return f'The deck has: {deck_comp}'

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def __str__(self):
        return f"You have ${self.total} chips to bet"

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Enter how much you'd like to bet: "))

        except ValueError:
            print("Whoops! Must enter a number!")
        else:
            if chips.bet > chips.total:
                print("You don't have enough chips for that!")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input("Would you like to stay or hit? Enter h or s")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing")
            playing = False
        else:
            print("Sorry, please try again")
            continue
        break


def show_some(player, dealer):
    print("Dealer's Hand: ")
    print("<card hidden>")
    print('', dealer.cards[1])
    print(f"Dealer's Hand = {dealer.cards[1].value}")
    print("Player's Hand :", *player.cards, sep="\n")
    print(f"Player's Hand = {player.value}")


def show_all(player, dealer):
    print("Dealer's Hand :", *dealer.cards, sep="\n")
    print(f"Dealer's Hand = {dealer.value}")
    print("Player's Hand:", *player.cards, sep="\n")
    print(f"Player's Hand = {player.value}")


def player_busts(chips):
    print("You bust!")
    chips.lose_bet()


def player_wins(chips):
    print("You win!")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()


def push():
    print("Dealer and Player tie! Its a push!")


player_chips = Chips()
while True:
    # Print an opening statement
    print("Welcome to Blackjack!")

    # Create & shuffle the deck, deal two cards to each player
    playing_deck = Deck()
    playing_deck.shuffle()
    player1 = Hand()
    dealer1 = Hand()
    player1.add_card(playing_deck.deal())
    player1.add_card(playing_deck.deal())
    dealer1.add_card(playing_deck.deal())
    dealer1.add_card(playing_deck.deal())
    # Set up the Player's chips

    print(player_chips)
    # Prompt the Player for their bet
    take_bet(player_chips)
    # Show cards (but keep one dealer card hidden)
    show_some(player1, dealer1)
    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(playing_deck, player1)
        # Show cards (but keep one dealer card hidden)
        show_some(player1, dealer1)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if 21 < player1.value <= 32:
            player1.adjust_for_ace()
            if player1.value <= 21:
                continue
            else:
                player_busts(player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player1.value < 21:
        while dealer1.value < 17:
            hit(playing_deck, dealer1)
        # Show all cards
        show_all(player1, dealer1)
        # Run different winning scenarios
        if dealer1.value > 21:
            dealer_busts(player_chips)
        elif dealer1.value >= player1.value:
            dealer_wins(player_chips)
        elif player1.value > dealer1.value:
            player_wins(player_chips)
        else:
            push()
    # Inform Player of their chips total
    print(f"\nPlayer's chips: ${player_chips.total}")
    # Ask to play again
    choice = input("Would you like to play again? Y/N ")
    if choice[0].upper() == "Y":
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
