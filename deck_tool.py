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

        self._label = tk.Label(self._root, text = "Hello world!")
        self._label.pack()

        self._button = tk.Button(self._root, text = "Click me!", command = self.on_button_click)
        self._button.pack()

        #self._running = False
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

    def close(self):
        #self._running = False
        print("window closed...")
        self._root.destroy()

def main():
    attributes = [("Strength", 20), ("Agility", 18), ("Endurance", 25), ("Intellect, 10"), ("Perception", 15), ("Will", 17)]
    hero = Character("Boris", attributes)
    print(hero.strength)
    print(hero.endurance)

    hero.set_skill("Axe", 15, "Martial")
    print(hero.skills)

    print("Before checks:")
    print(f"Active Deck: {hero.activeDeck}")
    print(f"Dead Deck: {hero.deadDeck}")

    print(f"Strength apptitude: {hero.strength.score}")
    result = hero.check_attribute(hero.strength)
    print(f"Strength check successes: {result}")

    print(f"Strength + Endurance apptitude: {hero.strength.score + hero.endurance.score}")
    result = hero.check_attribute_2(hero.strength, hero.endurance)
    print(f"Strength + Endurance check successes: {result}")

    print(f"Strength + Axe aptitude: {hero.strength.score + hero.skills["Axe"].score}")
    result = hero.check_attribute_skill(hero.strength, hero.skills["Axe"])
    print(f"Strength + Axe check successes: {result}")

    print("After checks:")
    print(f"Active Deck: {hero.activeDeck}")
    print(f"Dead Deck: {hero.deadDeck}")
    print(f"Stress: {hero.stress}")

    #root.mainloop()
    win = Window()

if __name__ == "__main__":
    main()
