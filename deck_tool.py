from enum import Enum
import random

def main():
    card = Card(CardValue.ACE, CardSuit.SPADES)
    print(card)

class CardValue(Enum):
    JOKER = 0
    ACE = 1
    N2 = 2
    N3 = 3
    N4 = 4
    N5 = 5
    N6 = 6
    N7 = 7
    N8 = 8
    N9 = 9
    N10 = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class CardSuit(Enum):
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    BLACK = 4
    RED = 5

class Card:
    def __init__(self, value: CardValue, suit: CardSuit):
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.suit != CardValue.JOKER:
            return f"{self.value.name} of {self.suit.name}"
        else:
            return f"{self.suit} {self.value}"

if __name__ == "__main__":
    main()

class Deck:
    def __init__(self, visible = False):
        self.visible = visible
        self.deck = []

    def fillStandardDeck(self):
        for value_num in range(1, 14):
            for suit_num in range(0, 4):
                value = CardValue(value_num)
                suit = CardSuit(suit_num)
                self.deck.append(Card(value, suit))

    def fillJokerDeck(self):
        self.deck.append(Card(CardValue.JOKER, CardSuit.BLACK))
        self.deck.append(Card(CardValue.JOKER, CardSuit.RED))

    def fillList(self, cards):
        self.deck.extend(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def cut(self):
        if len(self.deck) == 0:
            return Deck()
        
        mid_point = len(self.deck) // 2
        std_dev = len(self.deck) * 0.1
        cut_point = round(random.gauss(mid_point, std_dev))

        cut_point = max(0, min(len(self.deck), cut_point))

        second_deck = Deck()
        second_deck.fillList(self.deck[cut_point:])
        self.deck = self.deck[:cut_point]

        return second_deck

    def draw(self, num = 1):
        if len(self.deck) == 0:
            return []
        
        num = min(num, len(self.deck))
        drawn_cards = self.deck[-num:]
        self.deck = self.deck[:-num]
        return drawn_cards
    
    def is_empty(self):
        return len(self.deck) == 0
