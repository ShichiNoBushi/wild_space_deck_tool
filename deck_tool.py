import tkinter as tk
from tkinter import ttk
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
        self._root = tk.Tk()    #main window
        self._root.title = "Wild Space Deck Tool"

        self.galaxy_a_deck = Deck() #decks independent of characters
        self.galaxy_a_deck.fillStandardDeck()
        self.galaxy_a_deck.shuffle()
        self.galaxy_d_deck = self.galaxy_a_deck.cut()
        self.galaxy_discard = Deck()

        self.characters = {}    #dictionary of characters by name

        self.main_nb = ttk.Notebook(self._root) #tabs for various frames

        self.button_tab = tk.Frame(self.main_nb)    #tab for generic buttons
        self.characters_tab = tk.Frame(self.main_nb)    #tab for list of characters
        self.create_tab = tk.Frame(self.main_nb)    #tab for creating characters
        self.main_nb.add(self.button_tab, text = "Buttons")
        self.main_nb.add(self.characters_tab, text = "Characters")
        self.main_nb.add(self.create_tab, text = "Create")

        self.draw_card_button = tk.Button(self.button_tab, text = "Draw Card", command = self.draw_card)    #button to draw a card
        self.draw_card_button.pack()

        self.draw_hand_frame = tk.Frame(self.button_tab)    #frame to contain button and text box

        self.hand_size = tk.IntVar()    #control variable for hand size
        self.hand_entry = tk.Entry(self.draw_hand_frame, textvariable = self.hand_size, width = 5)  #text box for hand size
        self.hand_entry.pack(side = tk.LEFT)

        self.draw_hand_button = tk.Button(self.draw_hand_frame, text = "Draw Hand", command = self.draw_hand)   #button to draw hand
        self.draw_hand_button.pack(side = tk.RIGHT)
    
        self.draw_hand_frame.pack()

        self.char_list_frame = tk.Frame(self.characters_tab)    #frame list of characters and scroll bar

        self.char_list_scroll = tk.Scrollbar(self.char_list_frame)  #scroll bar for character list
        self.char_list_scroll.pack(side = tk.RIGHT, fill = tk.Y)

        self.lb_characters = tk.StringVar(value = list(self.characters.keys())) #control variable for list of characters
        self.characters_list = tk.Listbox(self.characters_tab, selectmode = tk.SINGLE, listvariable = self.lb_characters, yscrollcommand = self.char_list_scroll.set)
            #list box for characters
        self.characters_list.pack(side = tk.LEFT, fill = tk.Y)

        self.char_list_scroll.config(command = self.characters_list.yview)

        self.char_list_frame.pack(side = tk.LEFT)

        self.char_data_frame1 = tk.Frame(self.characters_tab)   #frame to display characters and button
        self.char_data_frame2 = tk.Frame(self.char_data_frame1) #sub-frame to display characters and scroll bar

        self.char_data_scroll = tk.Scrollbar(self.char_data_frame2) #scroll bar for character data
        self.char_data_scroll.pack(side = tk.RIGHT, fill = tk.Y)

        self.characters_data = tk.Text(self.char_data_frame2, wrap = tk.WORD, yscrollcommand = self.char_data_scroll.set, state = tk.DISABLED)
            #text box to display character data
        self.characters_data.pack(side = tk.LEFT, fill = tk.Y)

        self.char_data_scroll.config(command = self.characters_data.yview)

        self.char_data_frame2.pack(side = tk.TOP)

        self.char_data_button = tk.Button(self.char_data_frame1, text = "Display Character", command = self.display_character)  #button to display data of character selected from list
        self.char_data_button.pack(side = tk.BOTTOM)

        self.char_data_frame1.pack(side = tk.RIGHT)

        self.create_button = tk.Button(self.create_tab, text = "Create Character", command = self.create_character_simple)  #button to create a character
        self.create_button.pack()

        self.main_nb.pack(side = tk.TOP)

        self.log_frame = tk.Frame(self._root)   #frame to display log at bottom of window

        self.log_scroll = tk.Scrollbar(self.log_frame)  #scroll bar for log
        self.log_scroll.pack(side = tk.RIGHT, fill = tk.Y)

        self.log_text = tk.Text(self.log_frame, height = 10, wrap = tk.WORD, yscrollcommand = self.log_scroll.set, state = tk.DISABLED) #text box to display log
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

    def draw_card(self):    #draw a single card, discard, and add to log
        if self.galaxy_a_deck.size() >= 1:  #draw from active deck if any remain, from bottom of dead deck otherwise
            card = self.galaxy_a_deck.draw()[0]
        else:
            card = self.galaxy_d_deck.draw_bottom()[0]

        self.update_log(f"Card drawn: {card}")

        self.galaxy_discard.fillList([card])    #discard cards into discard pile (stress)
        if self.galaxy_a_deck.size() == 0:  #if active deck is empty, shuffle it with dead deck and stress
            self.update_log("Shuffling decks...")

            self.galaxy_a_deck.shuffle(self.galaxy_d_deck, self.galaxy_discard)
            self.galaxy_d_deck = self.galaxy_a_deck.cut()

    def draw_hand(self):    #draw cards designated by value in text box
        try:    #if value is not a positive whole number, update log with error
            num_cards = self.hand_size.get()    #hand size taken from control variable
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

    def display_character(self):    #display character in text box (!not fully implemented!)
        if len(self.characters_list.curselection()) == 0:
            self.update_log("No character selected.")
        else:
            character = self.characters[self.characters_list.get(self.characters_list.curselection()[0])]
            chara_data = ""
            name_line = f"Name: {character.name}\n\n"
            attributes_line = f"Attributes:\nStrength:   {character.strength.score}\nAgility:    {character.agility.score}\nEndurance:  {character.endurance.score}\nIntellect:  {character.intellect.score}\nPerception: {character.perception.score}\nWill:       {character.will.score}\n\n"
            derived_line = f"Derived stats:\nHealth:          {character.health()}\nPain Threshold:  {character.pain_threshold()}\nFocus Threshold: {character.focus_threshold()}\n\n"

            chara_data += name_line + attributes_line + derived_line
            self.characters_data.config(state = tk.NORMAL)
            self.characters_data.delete(1.0, tk.END)
            self.characters_data.insert(tk.END, chara_data)
            self.characters_data.config(state = tk.DISABLED) 

    def create_character_simple(self):  #create a character using simple methods
        new_name = f"Character {len(self.characters) + 1}"
        new_character = Character(new_name)
        self.characters[new_name] = new_character
        self.update_log(f"Character {new_name} added.")
        self.update_listbox()

    def update_log(self, message):  #add message to log
        self.log_text.config(state = tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state = tk.DISABLED)

    def update_listbox(self):
        self.lb_characters.set(list(self.characters.keys()))

    def close(self):
        #self._running = False
        print("window closed...")
        self._root.destroy()

def main():
    win = Window()  #create the program's main window

if __name__ == "__main__":
    main()
