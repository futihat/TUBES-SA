import random
from collections import Counter
import time

class Card:
    suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
    values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    #inisiasi
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    #representasi string
    def __repr__(self):
        return f'{self.value} of {self.suit}'

    def __lt__(self, other):
        if self.value == other.value:
            return Card.suits.index(self.suit) < Card.suits.index(other.suit)
        return Card.values.index(self.value) < Card.values.index(other.value)

class Deck:
    #rabdom kartu yang didapat
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)
    #validasi
    def deal(self, num_players):
        return [self.cards[i::num_players] for i in range(num_players)]

class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = sorted(cards)
        self.hand_count = Counter((card.value, card.suit) for card in self.cards)

    def play(self, last_play):
        #pemain terakhir ada
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
    #kartu milik pemain
    def has_cards(self):
        return bool(self.cards)

class BigTwoGame:
    def __init__(self, player_names):
        self.deck = Deck() #mendapat deck pemain
        self.players = [Player(name, cards) for name, cards in zip(player_names, self.deck.deal(len(player_names)))]
        self.current_player = 0
        self.last_play = [] #belum dimulai

    def play_game(self):
        passes = 0
        while True:
            player = self.players[self.current_player]
            play = player.play(self.last_play)
            if play:
                self.last_play = play
                passes = 0  # Reset passes when a play is made
                print(f'{player.name} plays {play}')
            else:
                passes += 1
                print(f'{player.name} passes')
                if passes == 3:
                    # Clear last play when all other players pass
                    self.last_play = []
                    passes = 0

            if not player.has_cards():
                print(f'Game over! {player.name} wins!')
                break

            self.current_player = (self.current_player + 1) % len(self.players)

if __name__ == '__main__':
    start = time.time() #menghitung waktu
    player_names = ['A', 'B', 'C', 'D'] #nama pemain
    game = BigTwoGame(player_names) #persiapan
    game.play_game() #nemulai
    stop = time.time()  # catat waktu selesai
    lama_eksekusi = stop - start  # lama eksekusi dalam satuan detik
    print("Lama eksekusi: ", lama_eksekusi, "detik")
