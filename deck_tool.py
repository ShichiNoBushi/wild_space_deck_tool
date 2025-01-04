from deck import *
from character import *

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

if __name__ == "__main__":
    main()
