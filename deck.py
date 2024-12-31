from enum import Enum
import random

class CardValue(Enum):  #value of card
    Joker = 0
    Ace = 1
    N2 = 2
    N3 = 3
    N4 = 4
    N5 = 5
    N6 = 6
    N7 = 7
    N8 = 8
    N9 = 9
    N10 = 10
    Jack = 11
    Queen = 12
    King = 13

class CardSuit(Enum):   #suit of card
    Spades = 0
    Hearts = 1
    Clubs = 2
    Diamonds = 3
    Black = 4
    Red = 5

class Card:
    def __init__(self, value: CardValue, suit: CardSuit):   #initializes card
        self.value = value
        self.suit = suit

    def __str__(self):  #returns Card as string
        if not self.is_joker():
            if self.is_number():
                return f"{self.value.value} of {self.suit.name}"
            else:
                return f"{self.value.name} of {self.suit.name}"
        else:
            return f"{self.suit.name} Joker"
        
    def __repr__(self): #debug representation
        return f"Card(value = {self.value}, suit = {self.suit})"
        
    def __eq__(self, card): #compare cards to each other
        if not isinstance(card, Card):
            return False
        return self.value == card.value and self.suit == card.suit
    
    def __ne__(self, card):
        if not isinstance(card, Card):
            return True
        return self.value != card.value or self.suit != card.suit
    
    def __lt__(self, card):
        if not isinstance(card, Card):
            return True
        if self.value == card.value:
            return self.suit < card.suit
        return self.value < card.value
    
    def __le__(self, card):
        if not isinstance(card, Card):
            return True
        if self.value == card.value:
            return self.suit <= card.suit
        return self.value <= card.value
    
    def __gt__(self, card):
        if not isinstance(card, Card):
            return False
        if self.value == card.value:
            return self.suit > card.suit
        return self.value > card.value
    
    def __ge__(self, card):
        if not isinstance(card, Card):
            return False
        if self.value == card.value:
            return self.suit >= card.suit
        return self.value >= card.value
        
    def is_face(self):  #if the card is a Jack, Queen, or King
        return self.value in {CardValue.Jack, CardValue.Queen, CardValue.King}
    
    def is_ace(self):   #if the card is an Ace
        return self.value == CardValue.Ace
    
    def is_number(self):    #if the card is a number (2-10)
        return 2 <= self.value.value <= 10
    
    def is_face_or_ace(self):   #if the card is a face or ace
        return self.is_face() or self.is_ace()
    
    def is_joker(self): #if the card is a Joker
        return self.value == CardValue.Joker
        
    def check_value(self):  #value for skill checks: face or ace is 1 (success), number is 0
        if self.is_face_or_ace():
            return 1
        else :
            return 0
        
    def attribute_value(self):  #value for calculating attributes: like Blackjack Ace = 11, face = 10, number = printed value
        if self.is_face():
            return 10
        elif self.is_ace():
            return 11
        else:
            return self.value.value
        
    def experience_value(self): #value for rewarding experience: number = printed value, Ace = 1, face = 0
        if self.is_ace():
            return 1
        elif self.is_number():
            return self.value.value
        else:
            return 0
        
    def damage_value(self): #value when taking damage
        if self.is_ace():
            return 1
        elif self.is_face():
            return 10
        elif self.is_number():
            return self.value.value
        else:
            return 0
        
    @staticmethod
    def total_success(cards):   #return total successes from a list of cards
        if len(cards) == 0:
            return 0
        return sum(card.check_value() for card in cards)
    
    @staticmethod
    def total_attribute(cards): #return total value for attribute from list of cards
        if len(cards) == 0:
            return 0
        return sum(card.attribute_value() for card in cards)
    
    @staticmethod
    def total_experience(cards):
        """
        return experience value rewarded for list of cards
        number cards reward lowest numerical value
        face cards reward 0
        Ace rewards 1 only if no number cards
        """
        if len(cards) == 0:
            return 0
        
        number_cards = (card for card in cards if card.is_number())
        min_number_value = min((card.experience_value() for card in number_cards), default = None)

        if min_number_value is not None:
            return min_number_value
        
        if any(card.is_ace() for card in cards):
            return 1
        
        return 0
        
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

    def shuffle(self, *decks):
        if len(decks) == 0:
            random.shuffle(self.deck)

        for d in decks:
            self.deck.extend(d)

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
    
    def draw_bottom(self, num = 1):
        if len(self.deck) == 0:
            return []
        
        num = min(num, len(self.deck))
        drawn_cards = self.deck[num]
        self.deck = self.deck[:num]
        return drawn_cards
    
    def is_empty(self):
        return len(self.deck) == 0