from deck import *

class Attribute:    #basic character trait
    def __init__(self, score, name):
        self.score = score
        self.name = name

    def __str__(self):
        return f"{self.name}: {self.score}"
    
    def __repr__(self):
        return f"Attribute(name = {self.name}, score = {self.score})"

class Skill:    #character skill representing training
    def __init__(self, score, name, category):
        self.score = score
        self.name = name
        self.category = category

    def __str__(self):
        return f"{self.name}: {self.score}"
    
    def __repr__(self):
        return f"Skill(name = {self.name}, score = {self.score}, category = {self.category})"

class Character:    #Wild Space RPG character
    def __init__(self, name, attributes = None):
        self.name = name    #character's name

        default_attributes = [("Strength", 0), ("Agility", 0), ("Endurance", 0),
                              ("Intellect", 0), ("Perception", 0), ("Will", 0)]
        attributes = attributes or default_attributes
        self.strength, self.agility, self.endurance, self.intellect, self.perception, self.will = [
            Attribute(score, name) for name, score in attributes
        ]

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

    def generate_attributes_array(self, stat_array):
        if len(stat_array) != 6:
            raise Exception("Attribute array needs to be 6 values")
        
        self.strength.score = stat_array[0]
        self.agility.score = stat_array[1]
        self.endurance.score = stat_array[2]
        self.intellect.score = stat_array[3]
        self.perception.score = stat_array[4]
        self.will.score = stat_array[5]

    def set_skill(self, name, score):
        if name not in self.skills:
            self.skills[name] = Skill(score, name)
        else:
            self.skills[name].score = score

    def _draw_hand(self, draw_num):
        hand = self.activeDeck.draw(draw_num)   #draw cards
        if self.activeDeck.size() == 0: #if no more cards in the active deck, draw the rest from the bottom of the dead deck
            hand.extend(self.deadDeck.draw_bottom(draw_num - len(hand)))

        for card in hand:   #for each Ace in the hand, draw an additional card from the dead deck (including extra Aces)
            if card.is_ace():
                hand.extend(self.deadDeck.draw())

        self.stress.fillList(hand)  #discard drawn cards to the stress pile

        if self.activeDeck.size() == 0: #if the active deck is empty, move one card to fatigue then shuffle the dead deck and stress pile into the active deck
            self.fatigue.fillList(self.deadDeck.draw_bottom())
            self.activeDeck.shuffle([self.deadDeck, self.stress])

        return hand

    def check_attribute(self, att):
        draw_num = att.score // 10  #initial number of cards is the tens digit of the attribute score
        hand = self._draw_hand(draw_num)
        return Card.total_success(hand) #number of successes is eaqual to face cards and aces in drawn cards
    
    def check_attribute_2(self, att1, att2):
        draw_num = (att1.score + att2.score) // 10  #initial number of cards is the tens digit of the sum of two attribute scores
        hand = self._draw_hand(draw_num)
        return Card.total_success(hand) #number of successes is eaqual to face cards and aces in drawn cards
    
    def check_attribute_skill(self, att, skill):
        draw_num = (att.score + skill.score) // 10  #initial number of cards is the tens digit of the sum of the attribute score and skill score
        hand = self._draw_hand(draw_num)
        return Card.total_success(hand) #number of successes is eaqual to face cards and aces in drawn cards