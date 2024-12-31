from deck import *

class Attribute:    #basic character trait
    def __init__(self, score):
        self.score = score

class Skill:    #character skill representing training
    def __init__(self, score, name):
        self.score = score
        self.name = name

class Character:    #Wild Space RPG character
    def __init__(self, name):
        self.name = name    #character's name

        self.strength = Attribute(0)    #initialize Attributes with 0 temporarily
        self.agility = Attribute(0)
        self.endurance = Attribute(0)
        self.intellect = Attribute(0)
        self.perception = Attribute(0)
        self.will = Attribute(0)

        self.skills = {}    #dictionary of character Skills

        self.activeDeck = Deck() #initialize deck, fill with 52 cards, shuffle, and cut off Dead deck
        self.activeDeck.fillStandardDeck()
        self.activeDeck.shuffle()
        self.deadDeck = self.activeDeck.cut() #deck set aside and rarely used
        self.jokers = Deck() #joker cards
        self.jokers.fillJokerDeck()
        self.stress = Deck(visibility = True) #discard pile
        self.fatigue = Deck(visibility = True)    #exhaustion
        self.wounds = Deck(visibility = True) #physical damage
        self.warp = Deck(visibility = True)   #corruption and madness

    #def generateAttributes(self):

