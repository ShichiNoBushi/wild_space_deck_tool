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

        self.create_button = tk.Button(self.create_tab, text = "Create Character", command = self.create_character, state = tk.DISABLED)  #button to create a character
        self.create_button.grid(row = 0, column = 0)

        self.create_name_frame = tk.Frame(self.create_tab)

        self.name_label = tk.Label(self.create_name_frame, text = "Name:")
        self.name_label.pack(side = tk.LEFT)

        self.name_cv = tk.StringVar()
        self.name_entry = tk.Entry(self.create_name_frame, textvariable = self.name_cv)
        self.name_entry.pack(side = tk.RIGHT)

        self.create_name_frame.grid(row = 1, column = 0)

        self.create_att_frame = tk.Frame(self.create_tab)

        self.select_att_frame = tk.Frame(self.create_att_frame)

        self.attribute_label = tk.Label(self.select_att_frame, text = "Attributes:")
        self.attribute_label.grid(row = 0, column = 0, columnspan = 2)

        self.select_attribute = tk.StringVar()

        self.strength_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Strength:", value = "Strength", variable = self.select_attribute)
        self.strength_radio.grid(row = 1, column = 0, sticky = "W")

        self.strength_cv = tk.IntVar()
        self.strength_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.strength_cv, width = 3)
        self.strength_entry.grid(row = 1, column = 1)

        self.agility_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Agility:", value = "Agility", variable = self.select_attribute)
        self.agility_radio.grid(row = 2, column = 0, sticky = "W")

        self.agility_cv = tk.IntVar()
        self.agility_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.agility_cv, width = 3)
        self.agility_entry.grid(row = 2, column = 1)

        self.endurance_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Endurance:", value = "Endurance", variable = self.select_attribute)
        self.endurance_radio.grid(row = 3, column = 0, sticky = "W")

        self.endurance_cv = tk.IntVar()
        self.endurance_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.endurance_cv, width = 3)
        self.endurance_entry.grid(row = 3, column = 1)

        self.intellect_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Intellect:", value = "Intellect", variable = self.select_attribute)
        self.intellect_radio.grid(row = 4, column = 0, sticky = "W")

        self.intellect_cv = tk.IntVar()
        self.intellect_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.intellect_cv, width = 3)
        self.intellect_entry.grid(row = 4, column = 1)

        self.perception_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Perception:", value = "Perception", variable = self.select_attribute)
        self.perception_radio.grid(row = 5, column = 0, sticky = "W")

        self.perception_cv = tk.IntVar()
        self.perception_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.perception_cv, width = 3)
        self.perception_entry.grid(row = 5, column = 1)

        self.will_radio = tk.Radiobutton(self.select_att_frame, state = tk.DISABLED, text = "Will:", value = "Will", variable = self.select_attribute)
        self.will_radio.grid(row = 6, column = 0, sticky = "W")

        self.will_cv = tk.IntVar()
        self.will_entry = tk.Entry(self.select_att_frame, state = tk.DISABLED, textvariable = self.will_cv, width = 3)
        self.will_entry.grid(row = 6, column = 1)

        self.att_reset = tk.Button(self.select_att_frame, command = self.reset_attributes, state = tk.DISABLED, text = "Reset")
        self.att_reset.grid(row = 7, column = 1, columnspan = 2)

        self.select_att_frame.pack(side = tk.LEFT)

        self.select_value_frame = tk.Frame(self.create_att_frame)

        self.array_label = tk.Label(self.select_value_frame, text = "Array:")
        self.array_label.grid(row = 0, column = 0, columnspan = 2)

        self.select_value = tk.IntVar()

        self.att1_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 1", value = 1, variable = self.select_value)
        self.att1_radio.grid(row = 1, column = 0)

        self.att1_cv = tk.IntVar()
        self.att1_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att1_cv, width = 3)
        self.att1_entry.grid(row = 1, column = 1)

        self.att2_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 2", value = 2, variable = self.select_value)
        self.att2_radio.grid(row = 2, column = 0)

        self.att2_cv = tk.IntVar()
        self.att2_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att2_cv, width = 3)
        self.att2_entry.grid(row = 2, column = 1)

        self.att3_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 3", value = 3, variable = self.select_value)
        self.att3_radio.grid(row = 3, column = 0)

        self.att3_cv = tk.IntVar()
        self.att3_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att3_cv, width = 3)
        self.att3_entry.grid(row = 3, column = 1)

        self.att4_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 4", value = 4, variable = self.select_value)
        self.att4_radio.grid(row = 4, column = 0)

        self.att4_cv = tk.IntVar()
        self.att4_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att4_cv, width = 3)
        self.att4_entry.grid(row = 4, column = 1)

        self.att5_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 5", value = 5, variable = self.select_value)
        self.att5_radio.grid(row = 5, column = 0)

        self.att5_cv = tk.IntVar()
        self.att5_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att5_cv, width = 3)
        self.att5_entry.grid(row = 5, column = 1)

        self.att6_radio = tk.Radiobutton(self.select_value_frame, state = tk.DISABLED, text = "Attribute 6", value = 6, variable = self.select_value)
        self.att6_radio.grid(row = 6, column = 0)

        self.att6_cv = tk.IntVar()
        self.att6_entry = tk.Entry(self.select_value_frame, state = tk.DISABLED, textvariable = self.att6_cv, width = 3)
        self.att6_entry.grid(row = 6, column = 1)

        self.begin_button = tk.Button(self.select_value_frame, command = self.generate_att_array, text = "Begin")
        self.begin_button.grid(row = 7, column = 0)

        self.assign_button = tk.Button(self.select_value_frame, command = self.assign_attribute, state = tk.DISABLED, text = "Assign")
        self.assign_button.grid(row = 7, column = 1)

        self.select_value_frame.pack(side = tk.RIGHT)

        self.create_att_frame.grid(row = 2, column = 0)

        self.att_black_jack_frame = tk.Frame(self.create_tab)

        self.atts_to_generate = 0
        self.att_array = []

        self.black_jack_hand = []
        self.bj_hand_cv = tk.StringVar()
        self.bj_hand_label = tk.Label(self.att_black_jack_frame, textvariable = self.bj_hand_cv, width = 20)
        self.bj_hand_label.grid(row = 0, column = 0)

        self.bj_att_score_cv = tk.IntVar()
        self.bj_att_score_cv.set(0)
        self.bj_att_score_entry = tk.Entry(self.att_black_jack_frame, state = tk.DISABLED, textvariable = self.bj_att_score_cv, width = 3)
        self.bj_att_score_entry.grid(row = 0, column = 1)

        self.bj_hits_label = tk.Label(self.att_black_jack_frame, text = "Hits remaining:")
        self.bj_hits_label.grid(row = 1, column = 0)

        self.hits_cv = tk.IntVar()
        self.hits_cv.set(0)
        self.hits_entry = tk.Entry(self.att_black_jack_frame, state = tk.DISABLED, textvariable = self.hits_cv, width = 3)
        self.hits_entry.grid(row = 1, column = 1)

        self.bj_hit_button = tk.Button(self.att_black_jack_frame, command = self.att_bj_hit, state = tk.DISABLED, text = "Hit")
        self.bj_hit_button.grid(row = 0, column = 2)

        self.bj_stay_button = tk.Button(self.att_black_jack_frame, command = self.att_bj_stay, state = tk.DISABLED, text = "Stay")
        self.bj_stay_button.grid(row = 1, column = 2)

        self.att_black_jack_frame.grid(row = 3, column = 0)

        self.skill_points_frame = tk.Frame(self.create_tab)

        self.skill_points_label = tk.Label(self.skill_points_frame, text = "Skill Points Remaining:")
        self.skill_points_label.grid(row = 0, column = 0)

        self.skill_points_cv = tk.IntVar()
        self.skill_points_cv.set(0)
        self.skill_points_entry = tk.Entry(self.skill_points_frame, state = tk.DISABLED, textvariable = self.skill_points_cv, width = 3)
        self.skill_points_entry.grid(row = 0, column = 1)

        self.skill_points_frame.grid(row = 0, column = 1)

        self.create_skill_frame = tk.Frame(self.create_tab)

        self.skill_category_cv = tk.StringVar()
        self.skill_category_cv.set(list(SKILL_LIST.keys())[0])
        self.skill_category_om = tk.OptionMenu(self.create_skill_frame, self.skill_category_cv, *list(SKILL_LIST.keys()), command = self.update_skill_list)
        self.skill_category_om.config(width = 10)
        self.skill_category_om.grid(row = 0, column = 0)

        self.skill_name_cv = tk.StringVar()
        self.skill_name_cv.set(SKILL_LIST[self.skill_category_cv.get()][0])
        self.skill_name_om = tk.OptionMenu(self.create_skill_frame, self.skill_name_cv, *SKILL_LIST["Martial"])
        self.skill_name_om.config(width = 10)
        self.skill_name_om.grid(row = 0, column = 1)

        self.skill_create_button = tk.Button(self.create_skill_frame, command = self.create_learn_skill, text = "Learn", state = tk.DISABLED)
        self.skill_create_button.grid(row = 0, column = 2)

        self.create_skill_frame.grid(row = 1, column = 1)

        self.skills_list_frame = tk.Frame(self.create_tab)

        self.skills_list_scroll = tk.Scrollbar(self.skills_list_frame)
        self.skills_list_scroll.pack(side = tk.RIGHT)

        self.skills_array = []
        self.skills_list_cv = tk.StringVar(value = self.skills_array)
        self.skills_list = tk.Listbox(self.skills_list_frame, listvariable = self.skills_list_cv, yscrollcommand = self.skills_list_scroll.set)
        self.skills_list.pack(side = tk.LEFT)

        self.skills_list_scroll.config(command = self.skills_list.yview)

        self.skills_list_frame.grid(row = 2, column = 1, rowspan = 2)

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
            name_line = f"Name: {character.name}\n\n"
            attributes_line = f"Attributes:\nStrength:   {character.strength.score}\nAgility:    {character.agility.score}\nEndurance:  {character.endurance.score}\nIntellect:  {character.intellect.score}\nPerception: {character.perception.score}\nWill:       {character.will.score}\n\n"
            derived_line = f"Derived stats:\nHealth:          {character.health()}\nPain Threshold:  {character.pain_threshold()}\nFocus Threshold: {character.focus_threshold()}\n\n"

            chara_data = name_line + attributes_line + derived_line
            self.characters_data.config(state = tk.NORMAL)
            self.characters_data.delete(1.0, tk.END)
            self.characters_data.insert(tk.END, chara_data)
            self.characters_data.config(state = tk.DISABLED)

    def create_character(self):
        new_name = self.name_cv.get()
        if new_name == "":
            new_name = "(no name)"

        try:
            strength = self.strength_cv.get()
            agility = self.agility_cv.get()
            endurance = self.endurance_cv.get()
            intellect = self.intellect_cv.get()
            perception = self.perception_cv.get()
            will = self.will_cv.get()

            new_character = Character(new_name, [("Strength", strength), ("Agility", agility), ("Endurance", endurance), ("Intellect", intellect), ("Perception", perception), ("Will", will)])

            for s in self.skills_array:
                new_character.set_skill(s.name, s.score, s.category)

            if new_name not in self.characters:
                self.characters[new_name] = new_character
                self.update_log(f"Character {new_name} added.")
                self.update_listbox()

                self.name_cv.set("")

                self.strength_cv.set(0)
                self.agility_cv.set(0)
                self.endurance_cv.set(0)
                self.intellect_cv.set(0)
                self.perception_cv.set(0)
                self.will_cv.set(0)

                self.strength_radio.config(state = tk.DISABLED)
                self.agility_radio.config(state = tk.DISABLED)
                self.endurance_radio.config(state = tk.DISABLED)
                self.intellect_radio.config(state = tk.DISABLED)
                self.perception_radio.config(state = tk.DISABLED)
                self.will_radio.config(state = tk.DISABLED)
                self.select_attribute.set("")

                self.att1_cv.set(0)
                self.att2_cv.set(0)
                self.att3_cv.set(0)
                self.att4_cv.set(0)
                self.att5_cv.set(0)
                self.att6_cv.set(0)

                self.att1_radio.config(state = tk.DISABLED)
                self.att2_radio.config(state = tk.DISABLED)
                self.att3_radio.config(state = tk.DISABLED)
                self.att4_radio.config(state = tk.DISABLED)
                self.att5_radio.config(state = tk.DISABLED)
                self.att6_radio.config(state = tk.DISABLED)
                self.select_value.set(0)

                self.create_button.config(state = tk.DISABLED)
                self.reset_attributes.config(state = tk.DISABLED)
                self.assign_attribute.config(state = tk.DISABLED)

                self.skill_create_button.config(state = tk.DISABLED)
                self.skill_points_cv.set(0)
                self.skills_array = []
            else:
                self.update_log(f"Character with name {new_name} already exists.")
        except tk.TclError:
            self.update_log("Attribute entry error: Attribute values must be whole numbers.")

    def reset_attributes(self):
        self.strength_cv.set(0)
        self.agility_cv.set(0)
        self.endurance_cv.set(0)
        self.intellect_cv.set(0)
        self.perception_cv.set(0)
        self.will_cv.set(0)
        
        self.strength_radio.config(state = tk.NORMAL)
        self.agility_radio.config(state = tk.NORMAL)
        self.endurance_radio.config(state = tk.NORMAL)
        self.intellect_radio.config(state = tk.NORMAL)
        self.perception_radio.config(state = tk.NORMAL)
        self.will_radio.config(state = tk.NORMAL)
        self.select_attribute.set("")

        self.att1_radio.config(state = tk.NORMAL)
        self.att2_radio.config(state = tk.NORMAL)
        self.att3_radio.config(state = tk.NORMAL)
        self.att4_radio.config(state = tk.NORMAL)
        self.att5_radio.config(state = tk.NORMAL)
        self.att6_radio.config(state = tk.NORMAL)
        self.select_value.set(0)

        self.create_button.config(state = tk.DISABLED)

    def generate_att_array(self):
        self.strength_cv.set(0)
        self.agility_cv.set(0)
        self.endurance_cv.set(0)
        self.intellect_cv.set(0)
        self.perception_cv.set(0)
        self.will_cv.set(0)
        
        self.att1_cv.set(0)
        self.att2_cv.set(0)
        self.att3_cv.set(0)
        self.att4_cv.set(0)
        self.att5_cv.set(0)
        self.att6_cv.set(0)

        self.strength_radio.config(state = tk.DISABLED)
        self.agility_radio.config(state = tk.DISABLED)
        self.endurance_radio.config(state = tk.DISABLED)
        self.intellect_radio.config(state = tk.DISABLED)
        self.perception_radio.config(state = tk.DISABLED)
        self.will_radio.config(state = tk.DISABLED)
        self.select_attribute.set("")

        self.att1_radio.config(state = tk.DISABLED)
        self.att2_radio.config(state = tk.DISABLED)
        self.att3_radio.config(state = tk.DISABLED)
        self.att4_radio.config(state = tk.DISABLED)
        self.att5_radio.config(state = tk.DISABLED)
        self.att6_radio.config(state = tk.DISABLED)
        self.select_value.set(0)

        self.att_reset.config(state = tk.DISABLED)
        self.assign_button.config(state = tk.DISABLED)

        self.galaxy_a_deck.shuffle(self.galaxy_d_deck, self.galaxy_discard)
        self.galaxy_d_deck = self.galaxy_a_deck.cut()

        self.black_jack_hand.extend(self.galaxy_a_deck.draw(2))
        self.bj_hand_cv.set(" ".join(card.short_hand() for card in self.black_jack_hand))
        self.bj_att_score_cv.set(sum(card.attribute_value() for card in self.black_jack_hand))
        self.atts_to_generate = 6
        self.att_array = []
        self.hits_cv.set(4)

        self.bj_hit_button.config(state = tk.NORMAL)
        self.bj_stay_button.config(state = tk.NORMAL)

        self.skill_create_button.config(state = tk.NORMAL)
        self.skill_points_cv.set(5)
        self.skills_array = []

    def assign_attribute(self):
        if self.select_attribute.get() == "" or self.select_value.get() == 0:
            self.update_log("Select an attribute and  value in the array to assign.")
        else:
            match self.select_attribute.get():
                case "Strength":
                    selected_att_radio = self.strength_radio
                    selected_att_cv = self.strength_cv
                case "Agility":
                    selected_att_radio = self.agility_radio
                    selected_att_cv = self.agility_cv
                case "Endurance":
                    selected_att_radio = self.endurance_radio
                    selected_att_cv = self.endurance_cv
                case "Intellect":
                    selected_att_radio = self.intellect_radio
                    selected_att_cv = self.intellect_cv
                case "Perception":
                    selected_att_radio = self.perception_radio
                    selected_att_cv = self.perception_cv
                case "Will":
                    selected_att_radio = self.will_radio
                    selected_att_cv = self.will_cv

            match self.select_value.get():
                case 1:
                    selected_value_radio = self.att1_radio
                    selected_value_cv = self.att1_cv
                case 2:
                    selected_value_radio = self.att2_radio
                    selected_value_cv = self.att2_cv
                case 3:
                    selected_value_radio = self.att3_radio
                    selected_value_cv = self.att3_cv
                case 4:
                    selected_value_radio = self.att4_radio
                    selected_value_cv = self.att4_cv
                case 5:
                    selected_value_radio = self.att5_radio
                    selected_value_cv = self.att5_cv
                case 6:
                    selected_value_radio = self.att6_radio
                    selected_value_cv = self.att6_cv

            selected_att_cv.set(selected_value_cv.get())
            selected_att_radio.config(state = tk.DISABLED)
            selected_value_radio.config(state = tk.DISABLED)

            self.update_log(f"{self.select_attribute.get()} set to {selected_value_cv.get()}.")

            self.select_attribute.set("")
            self.select_value.set(0)

            if self.strength_radio.cget("state") == self.agility_radio.cget("state") == self.endurance_radio.cget("state") == self.intellect_radio.cget("state") == self.perception_radio.cget("state") == self.will_radio.cget("state") == tk.DISABLED:
                self.create_button.config(state = tk.NORMAL)
                self.update_log("All attributes assigned. Ready to create character. Don't forget to name them.")

    def att_bj_hit(self):
        if self.galaxy_a_deck.size() > 0:
            self.black_jack_hand.extend(self.galaxy_a_deck.draw())
        else:
            self.black_jack_hand.extend(self.galaxy_d_deck.draw())

        self.bj_hand_cv.set(" ".join(card.short_hand() for card in self.black_jack_hand))
        self.bj_att_score_cv.set(sum(card.attribute_value() for card in self.black_jack_hand))
        self.hits_cv.set(self.hits_cv.get() - 1)

        self.update_log(f"Score: {self.bj_att_score_cv.get()}, Hits: {self.hits_cv.get()}")

        if self.bj_att_score_cv.get() > 21:
            self.update_log("Busted!")
            if self.hits_cv.get() > 0:
                self.update_log("-1 Hit")
                self.hits_cv.set(self.hits_cv.get() - 1)
            else:
                self.update_log("Insufficient hits; -5 Score")
                self.bj_att_score_cv.set(self.bj_att_score_cv.get() - 5)

        if self.bj_att_score_cv.get() > 21 or self.hits_cv.get() == 0:
            self.bj_hit_button.config(state = tk.DISABLED)

    def att_bj_stay(self):
        match self.atts_to_generate:
            case 6:
                self.att1_cv.set(self.bj_att_score_cv.get())
            case 5:
                self.att2_cv.set(self.bj_att_score_cv.get())
            case 4:
                self.att3_cv.set(self.bj_att_score_cv.get())
            case 3:
                self.att4_cv.set(self.bj_att_score_cv.get())
            case 2:
                self.att5_cv.set(self.bj_att_score_cv.get())
            case 1:
                self.att6_cv.set(self.bj_att_score_cv.get())

        self.att_array.append(self.bj_att_score_cv.get())

        self.galaxy_discard.fillList(self.black_jack_hand)
        self.black_jack_hand = []
        
        self.atts_to_generate -= 1
        if len(self.att_array) < 6:
            self.black_jack_hand.extend(self.galaxy_a_deck.draw(2))
            if len(self.black_jack_hand) < 2:
                self.black_jack_hand.extend(self.galaxy_d_deck.draw(2 - len(self.black_jack_hand)))
            self.bj_hand_cv.set(" ".join(card.short_hand() for card in self.black_jack_hand))
            self.bj_att_score_cv.set(sum(card.attribute_value() for card in self.black_jack_hand))
        else:
            self.bj_hit_button.config(state = tk.DISABLED)
            self.bj_stay_button.config(state = tk.DISABLED)
            self.bj_att_score_cv.set(0)

            self.strength_radio.config(state = tk.NORMAL)
            self.agility_radio.config(state = tk.NORMAL)
            self.endurance_radio.config(state = tk.NORMAL)
            self.intellect_radio.config(state = tk.NORMAL)
            self.perception_radio.config(state = tk.NORMAL)
            self.will_radio.config(state = tk.NORMAL)
            self.select_attribute.set("")

            self.att_array.sort(reverse = True)
            self.att1_cv.set(self.att_array[0])
            self.att2_cv.set(self.att_array[1])
            self.att3_cv.set(self.att_array[2])
            self.att4_cv.set(self.att_array[3])
            self.att5_cv.set(self.att_array[4])
            self.att6_cv.set(self.att_array[5])

            self.att1_radio.config(state = tk.NORMAL)
            self.att2_radio.config(state = tk.NORMAL)
            self.att3_radio.config(state = tk.NORMAL)
            self.att4_radio.config(state = tk.NORMAL)
            self.att5_radio.config(state = tk.NORMAL)
            self.att6_radio.config(state = tk.NORMAL)
            self.select_value.set(0)

            self.att_reset.config(state = tk.NORMAL)
            self.assign_button.config(state = tk.NORMAL)

        if self.hits_cv.get() > 0:
            self.bj_hit_button.config(state = tk.NORMAL)

    def update_skill_list(self, selected_category):
        skill_category = SKILL_LIST[selected_category]
        self.skill_name_cv.set(skill_category[0])
        menu = self.skill_name_om["menu"]
        menu.delete(0, "end")
        for skill in skill_category:
            menu.add_command(label = skill, command = lambda s = skill: self.skill_name_cv.set(s))

    def create_learn_skill(self):
        skill_learned = False
        new_skill = None
        for s in self.skills_array:
            if s.name == self.skill_name_cv.get():
                skill_learned = True
                new_skill = s
                break
        
        if not skill_learned:
            new_skill = Skill(10, self.skill_name_cv.get(), self.skill_category_cv.get())
            self.skills_array.append(new_skill)
            self.skill_points_cv.set(self.skill_points_cv.get() - 1)
        else:
            new_skill.score += 5
            self.skill_points_cv.set(self.skill_points_cv.get() - 1)

        self.update_skill_listbox()

        if self.skill_points_cv.get() == 0:
            self.skill_create_button.config(state = tk.DISABLED)

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

    def update_skill_listbox(self):
        self.skills_list_cv.set(self.skills_array)

    def close(self):
        #self._running = False
        print("window closed...")
        self._root.destroy()

def main():
    win = Window()  #create the program's main window

if __name__ == "__main__":
    main()
