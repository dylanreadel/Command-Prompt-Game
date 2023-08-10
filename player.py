"""import"""
from delayprint import delay_print
from main import displaystats
from main import displayinventory
from main import allitems
from main import fightchance

class Player:
    """Class representing a Player"""

    def __init__(self, name, age, health, inventory, weapon, playerdamage, experience, level, kills):
        """player initialization"""
        self.name = name
        self.age = age
        self.health = float(health)
        self.inventory = inventory
        self.weapon = weapon
        self.playerdamage = float(playerdamage)
        self.experience = int(experience)
        self.level = int(level)
        self.kills = int(kills)

    def welcome(self):
        """welcome message"""
        print("\n------------------------------------------\n")
        delay_print(f"Welcome to the game, {self.name.title()}!")
        delay_print(f"Your character is {self.age} years old.\n")
        self.inventory.append("apple")
        self.inventory.append("key")
        self.inventory.append("apple")
        self.playerdamage = float(allitems[self.weapon]["points"]) + fightchance
        displaystats(self)
        displayinventory(self)