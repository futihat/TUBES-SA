import random
from collections import Counter

class Card:
    suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
    values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.value} of {self.suit}'

    def __lt__(self, other):
        if self.value == other.value:
            return Card.suits.index(self.suit) < Card.suits.index(other.suit)
        return Card.values.index(self.value) < Card.values.index(other.value)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)
    
    def deal(self, num_players):
        return [self.cards[i::num_players] for i in range(num_players)]

class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = sorted(cards)
        self.hand_count = Counter((card.value, card.suit) for card in self.cards)

    def play(self, last_play):
        if not last_play:
            # Play the smallest single card
            card_to_play = self.cards.pop(0)
            self.hand_count[(card_to_play.value, card_to_play.suit)] -= 1
            return [card_to_play]
        else:
            # Play the smallest card that can beat the last play
            for i, card in enumerate(self.cards):
                if card > last_play[0]:
                    card_to_play = self.cards.pop(i)
                    self.hand_count[(card_to_play.value, card_to_play.suit)] -= 1
                    return [card_to_play]
        return []

    def has_cards(self):
        return bool(self.cards)

class BigTwoGame:
    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [Player(name, cards) for name, cards in zip(player_names, self.deck.deal(len(player_names)))]
        self.current_player = 0
        self.last_play = []

    def play_game(self):
        while any(player.has_cards() for player in self.players):
            player = self.players[self.current_player]
            play = player.play(self.last_play)
            if play:
                self.last_play = play
                print(f'{player.name} plays {play}')
            else:
                print(f'{player.name} passes')
            self.current_player = (self.current_player + 1) % len(self.players)
        print(f'Game over! {self.players[self.current_player].name} wins!')

if __name__ == '__main__':
    player_names = ['Alice', 'Bob', 'Charlie', 'Diana']
    game = BigTwoGame(player_names)
    game.play_game()