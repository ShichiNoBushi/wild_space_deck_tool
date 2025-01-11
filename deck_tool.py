import tkinter as tk
from tkinter import messagebox

from deck import *
from character import *

"""root = tk.Tk()
root.title("Wild Space Deck Tool")

label = tk.Label(root, text = "Hello world!")
label.pack()

def on_button_click():
    label.config(text = "Button clicked!")

button = tk.Button(root, text = "Click me!", command = on_button_click)
button.pack()"""

class Window:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title = "Wild Space Deck Tool"

        #self._label = tk.Label(self._root, text = "Hello world!")
        #self._label.pack()

        #self._button = tk.Button(self._root, text = "Click me!", command = self.on_button_click)
        #self._button.pack()

        self.galaxy_a_deck = Deck()
        self.galaxy_a_deck.fillStandardDeck()
        self.galaxy_a_deck.shuffle()
        self.galaxy_d_deck = self.galaxy_a_deck.cut()
        self.galaxy_discard = Deck()

        self.draw_card_button = tk.Button(self._root, text = "Draw Card", command = self.draw_card)
        self.draw_card_button.pack()

        self.draw_hand_frame = tk.Frame(self._root)

        self.hand_size = tk.IntVar()
        self.hand_entry = tk.Entry(self.draw_hand_frame, textvariable = self.hand_size, width = 5)
        self.hand_entry.pack(side = tk.LEFT)

        self.draw_hand_button = tk.Button(self.draw_hand_frame, text = "Draw Hand", command = self.draw_hand)
        self.draw_hand_button.pack(side = tk.RIGHT)
    
        self.draw_hand_frame.pack()

        self.log_frame = tk.Frame(self._root)

        self.log_scroll = tk.Scrollbar(self.log_frame)
        self.log_scroll.pack(side = tk.RIGHT, fill = tk.Y)

        self.log_text = tk.Text(self.log_frame, height = 10, wrap = tk.WORD, yscrollcommand = self.log_scroll.set, state = tk.DISABLED)
        self.log_text.pack(side = tk.LEFT, fill = tk.Y)

        self.log_scroll.config(command = self.log_text.yview)

        self.log_frame.pack(side = tk.BOTTOM, fill = tk.X)
    
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._root.mainloop()
    """
    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()
        print("window closed...")
    """
    def on_button_click(self):
        self._label.config(text = "Button clicked!")

    def draw_card(self):
        if self.galaxy_a_deck.size() >= 1:
            card = self.galaxy_a_deck.draw()[0]
        else:
            card = self.galaxy_d_deck.draw_bottom()[0]

        self.update_log(f"Card drawn: {card}")
        self.update_log(f"Cards left in Active Deck: {self.galaxy_a_deck.size()}")
        self.update_log(f"Cards left in Dead Deck: {self.galaxy_d_deck.size()}")
        self.update_log(f"Cards in dicard pile: {self.galaxy_discard.size()}")

        self.galaxy_discard.fillList([card])
        if self.galaxy_a_deck.size() == 0:
            self.update_log("Shuffling decks...")

            self.galaxy_a_deck.shuffle(self.galaxy_d_deck, self.galaxy_discard)
            self.galaxy_d_deck = self.galaxy_a_deck.cut()

    def draw_hand(self):
        try:
            num_cards = self.hand_size.get()
            if num_cards > 0:
                hand = self.galaxy_a_deck.draw(num_cards)
                if self.galaxy_a_deck.size() == 0:
                    hand.extend(self.galaxy_d_deck.draw_bottom(num_cards - len(hand)))
                if len(hand) < num_cards:
                    self.update_log("Insufficient cards left in decks")

                hand_message = " ".join(card.short_hand() for card in hand)
                self.update_log(hand_message)

                self.galaxy_discard.fillList(hand)

                if self.galaxy_a_deck.size() == 0:
                    self.update_log("Shuffling decks...")
                    
                    self.galaxy_a_deck.shuffle(self.galaxy_d_deck, self.galaxy_discard)
                    self.galaxy_d_deck = self.galaxy_a_deck.cut()
            else:
                self.update_log("Invalid entry: enter positive whole number")
        except tk.TclError:
            self.update_log("Invalid entry: enter positive whole number")

    def update_log(self, message):
        self.log_text.config(state = tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state = tk.DISABLED)

    def close(self):
        #self._running = False
        print("window closed...")
        self._root.destroy()

def main():
    win = Window()

if __name__ == "__main__":
    main()
