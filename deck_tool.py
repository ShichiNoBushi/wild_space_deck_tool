from enum import Enum

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