from deck import *

def main():
    deck = Deck()
    deck.fillStandardDeck()
    deck.shuffle()

    hand = deck.draw(5)
    print(hand)

if __name__ == "__main__":
    main()
