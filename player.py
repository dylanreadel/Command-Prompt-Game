"""import"""
import time
import random
import sys
from collections import Counter

from items import displayitem, random_item, items, consumableitems, weaponitems, tokenitems
from rules import rules
from savegame import savegame
from constants import fightchance, walkchance, HEALTH, ENERGY, randomperc

############## player class initialization & player functions ##############

class Player:
    """Class representing a Player"""

    def __init__(self, name, age, health, energy, inventory,
                 inventory_size, weapon, playerdamage, experience,
                 level, kills, SPEED):
        """player initialization"""
        self.name = name
        self.age = age
        self._health = int(health)
        self._energy = int(energy)
        self.inventory = inventory
        self.inventory_size = int(inventory_size)
        self.weapon = weapon
        self.playerdamage = float(playerdamage)
        self.experience = int(experience)
        self.level = int(level)
        self.kills = int(kills)
        self.SPEED = float(SPEED)

    @property
    def health(self):
        """health getter"""
        return self._health

    @health.setter
    def health(self, health):
        """health setter"""
        if health >= HEALTH:
            self._health = HEALTH
        elif health < 0:
            self._health = 0
        else:
            self._health = health

    def display_health(self):
        """display health function"""
        if self._health % 2 == 0:
            print("Health: " + ("{}" * int(self._health / 10)), str(self._health), "\n")
        else:
            num = self._health - 5
            print("Health: " + ("{}" * int(num / 10)) + "{", str(self._health), "\n")
   
    @property
    def energy(self):
        """energy getter"""
        return self._energy
    
    @energy.setter
    def energy(self, energy):
        """energy setter"""
        if energy >= ENERGY:
            self._energy = ENERGY
        elif energy < 0:
            self._energy = 0
        else:
            self._energy = energy

    def display_energy(self):
        """display energy function"""
        if self._energy % 2 == 0:
            print("Energy: " + ("<>" * int(self._energy / 10)), str(self._energy), "\n")
        else:
            num = self._energy - 5
            print("Energy: " + ("<>" * int(num / 10)) + "<", str(self._energy), "\n")

    def progression(self):
        """level progression function"""
        if self.experience >= 25 * self.level**1.5:
            self.level += 1
            inventory_increase = random.randint(1, 3)
            self.inventory_size += inventory_increase
            levelup_reward = random_item(tokenitems)
            self.inventory.append(random_item(tokenitems))
            print("\n------------------------------------------\n")
            self.delay_print("\nYou leveled up!")
            self.delay_print(f"Level {self.level-1} -----> Level {self.level}")
            self.delay_print(f"XP required to reach Level {self.level + 1}: {int(25 * self.level**1.5)}")
            self.delay_print(f"\nYou received a new token: {levelup_reward}")
            self.delay_print(f"\nInventory capacity increased by {inventory_increase}.")
            print("\n------------------------------------------\n")

    def game_speed(self):
        """game speed function to determine print and sleep times"""
        speedinput = input("\nSet Game Speed: (s)lug | (c)at | (f)alcon \n\n")
        match speedinput:
            case "s" | "S":
                print("\nGame speed set to slug pace.\n")
                self.SPEED = 0.08
            case "c" | "C":
                print("\nGame speed set to cat pace.\n")
                self.SPEED = 0.05
            case "f" | "F":
                print("\nGame speed set to falcon pace.\n")
                self.SPEED = 0
            case other:
                print(f"\n{other} not an option.")
                self.game_speed()

    def welcome(self):
        """welcome message"""
        print("\n------------------------------------------")
        self.game_speed()
        self.delay_print(f"Welcome to the Game, {self.name.title()}!")
        self.delay_print(f"Your character is {self.age} years old.\n")
        startinv = ["apple", "chips", "bandage", "apple"]
        self.inventory.extend(startinv)
        self.playerdamage = float(items[self.weapon].points) + fightchance
        time.sleep(self.SPEED * 40)
        rules()
        time.sleep(self.SPEED * 300)
        self.displaystats()
        time.sleep(self.SPEED * 200)
        self.displayinventory()
        time.sleep(self.SPEED * 40)

    def get_speed(self):
        """return current game speed"""
        return self.SPEED

    # delay print letter by letter function
    def delay_print(self, string):
        """delay print function"""
        sp = self.SPEED
        for char in string:
            print(char, end="", flush=True)
            time.sleep(sp)
        print("\n", end="")

    def displaystats(self):
        """display stats function"""
        print("-------------------------------------------------------------\n")
        print(f"        STATS MENU: {self.name.title()}, {self.age} years old\n")
        print(f"             Level: {self.level}")
        print(f"        Experience: {self.experience}\n")
        print(f"            Health: {self.health}")
        print(f"            Energy: {self.energy}")
        print(f"   Equipped Weapon: {self.weapon}")
        print(f"     Weapon Damage: {items[self.weapon].points}")
        print(f"      Total Damage: {self.playerdamage} (Base {fightchance} Damage + Weapon Damage)\n")
        print("-------------------------------------------------------------\n")

    def displayadvancedstats(self):
        """display advanced stats function"""
        print("\n-------------------------------------------------------------\n")
        print(f"ADVANCED STATS MENU: {self.name.title()}, {self.age} years old\n")
        print(f"   Enemies Executed: {self.kills}\n")
        print("-------------------------------------------------------------\n")

    def stats(self):
        """stats menu function"""
        self.displaystats()
        playerchoice = input("(a)dvanced stats or press enter to return to game\n")
        print("\n")
        if playerchoice == "a":
            self.displayadvancedstats()
        elif playerchoice == "":
            return

    def displayinventory(self):
        """display inventory function"""
        print("-------------------------------------------------------------\n")
        print(f"| INVENTORY MENU | CAPACITY: {len(self.inventory)}/{self.inventory_size} |\n")
        counteditems = dict(Counter(self.inventory))
        for item, count in sorted(counteditems.items()):
            display = displayitem(item)
            print(str(count) + "x " + display)
        print("\n-------------------------------------------------------------\n")

    def playerinventory(self):
        """inventory menu function"""
        self.displayinventory()
        playerchoice = input("Press enter to return to game\n")
        if playerchoice == "":
            return
        
    def healmenu(self):
        """heal menu function"""
        while self.health < HEALTH:
            print("\n------------------------Healing Menu-------------------------\n")
            self.display_health()
            self.displayinventory()
            self.check_heal_item()
            break
        else:
            self.delay_print(f"\nHealth cannot be greater than {HEALTH}.\n")

    def check_heal_item(self):
        """check input item with healing parameters"""
        while self.health < HEALTH:
            print("Type a consumable, healing item from your inventory to heal.")
            inputitem = input("(or press ENTER to return to game) \n\n")
            if inputitem in self.inventory:
                if items[inputitem].use == "heal":
                    self.use_heal_item(inputitem)
                else:
                    self.delay_print("\nItem found in inventory but cannot be consumed for healing.\n")
                    self.check_heal_item()
            elif inputitem == "":
                break
            else:
                self.delay_print("\nItem not found in inventory.\n")
                continue
            choice = input("Do you want to heal again? (y/n) ")
            print("\n")
            match choice:
                case "y" | "Y":
                    continue
                case "n" | "N":
                    break
                case other:
                    print(f"{other} is not an option.\n")
                    break
        else:
            self.delay_print(f"Health cannot be greater than {HEALTH}.\n")

    def use_heal_item(self, item):
        """determine if inventory item can heal"""
        if self.health + int(items[item].points) < HEALTH:
            self.health += int(items[item].points)
            self.delay_print(f"\nYou consumed 1 {item} to increase your health by {items[item].points}.\n")
            self.display_health()
        else:
            self.health = HEALTH
            self.delay_print(f"\nYou consumed 1 {item} to increased your health to max ({HEALTH}).\n")
        index_item = self.inventory.index(item)
        self.inventory.pop(index_item)

    def energymenu(self):
        """energy menu function"""
        while self.energy < ENERGY:
            print("\n----------------------Energizing Menu------------------------\n")
            self.display_energy()
            self.displayinventory()
            self.check_energy_item()
            break
        else:
            self.delay_print(f"\nEnergy cannot be greater than {ENERGY}.\n")

    def check_energy_item(self):
        """check input item with energizing parameters"""
        while self.energy < ENERGY:
            print("Type a consumable, energizing item from your inventory to energize.")
            inputitem = input("(or press ENTER to return to game) \n\n")
            if inputitem in self.inventory:
                if items[inputitem].use == "energize":
                    self.use_energy_item(inputitem)
                else:
                    self.delay_print("\nItem found in inventory but cannot be consumed for energizing.\n")
                    self.check_energy_item()
            elif inputitem == "":
                break
            else:
                self.delay_print("\nItem not found in inventory.\n")
                continue
            choice = input("Do you want to energize again? (y/n) ")
            print("\n")
            match choice:
                case "y" | "Y":
                    continue
                case "n" | "N":
                    break
                case other:
                    print(f"{other} is not an option.\n")
                    break
        else:
            self.delay_print(f"Energy cannot be greater than {ENERGY}.\n")

    def use_energy_item(self, item):
        """determine if inventory item can energize"""
        if self.energy + int(items[item].points) < ENERGY:
            self.energy += int(items[item].points)
            self.delay_print(f"\nYou consumed 1 {item} to increase your energy by {items[item].points}.\n")
            self.display_energy()
        else:
            self.energy = ENERGY
            self.delay_print(f"\nYou consumed 1 {item} to increased your energy to max ({ENERGY}).\n")
        index_item = self.inventory.index(item)
        self.inventory.pop(index_item)

    def quitgame(self):
        """quit game function"""
        while True:
            save = input("\nWould you like to save the game? (y/n) ")
            match save:
                case "y" | "Y":
                    print("\n\n")
                    savegame(self)
                case "n" | "N":
                    print("\nProgress will be lost!\n")
                case other:
                    print(f"\n{other} is not an option.\n")
                    continue
            break
        while True:
            quitgame = input("Are you sure you want to quit the game? (y/n) ")
            match quitgame:
                case "y" | "Y":
                    sys.exit()
                case "n" | "N":
                    break
                case other:
                    print(f"\n{other} is not an option.\n")
                    continue

    def options(self):
        """options menu function"""
        print("Options:\n")
        print("(i)nventory", "(s)tats", "(h)eal", "(e)nergize", "(g)ame speed", "(r)ules", "(q)uit\n", sep="\n")
        while True:
            playerchoice = input("-------> ")
            match playerchoice:
                case "i" | "I":
                    print("\n")
                    self.playerinventory()
                case "s" | "S":
                    print("\n")
                    self.stats()
                case "h" | "H":
                    print("\n")
                    self.healmenu()
                case "e" | "E":
                    print("\n")
                    self.energymenu()
                case "g" | "G":
                    print("\n")
                    self.game_speed()
                case "q" | "Q":
                    print("\n")
                    self.quitgame()
                case "r" | "R":
                    print("\n")
                    rules()
                case other:
                    print(f"\n{other} is not an option.\n")
                    continue
            break

    def walk(self):
        """walk mechanic function"""
        while self.energy > 0:
            if randomperc() <= walkchance:
                experiencegain = random.randint(0, 10)
                self.delay_print(f"You safely walked forward. +{experiencegain} XP")
                self.experience += experiencegain
                self.progression()
                energyuse = random.randint(0, 10)
                self.delay_print(f"Walking consumed {energyuse} energy.\n")
                self.energy -= energyuse
                break
            self.delay_print("You encountered an enemy!\n")
            self.fightretreat()
            break
        else:
            self.delay_print("No energy available...\n")

    def fightretreat(self):
        """fight or retreat sequence"""
        while True:
            playerchoice = input("(f)ight or (r)etreat? \n\n")
            match playerchoice:
                case "f" | "F":
                    self.fight()
                case "r" | "R":
                    self.retreat()
                case other:
                    self.delay_print(f"\n{other} is not an option.\n")
                    continue
            break

    def fight(self):
        """fight mechanic function"""
        self.delay_print("\nYou chose to fight...an enemy approaches.")
        self.delay_print("A battle breaks out!\n")
        print("\n-------------------------------------------------------------\n")
        time.sleep(self.SPEED * 40)
        energyuse = random.randint(5, 15)
        # success if random int is less/equal to total damage chance
        if randomperc() <= self.playerdamage:
            healthgain = random.randint(0, 5)
            xpgain = random.randint(0, 10)
            self.health += healthgain
            self.experience += xpgain
            self.delay_print("You won the fight!")
            self.delay_print(f"+{healthgain} Health")
            self.delay_print(f"+{xpgain} XP\n")
            self.kills += 1
            self.progression()
            self.obtainable_item(weaponitems)
            for _ in range(random.randint(0,3)):
                self.obtainable_item(consumableitems)
        else:
            healthloss = random.randint(5, 10)
            self.delay_print("The enemy beat you this time.")
            self.delay_print(f"-{healthloss} Health")
            self.health -= healthloss
        self.delay_print(f"-{energyuse} Energy\n")
        self.energy -= energyuse
        self.display_health()
        self.display_energy()

    def retreat(self):
        """retreat from fight function"""
        energyuse = random.randint(5, 15)
        while self.energy - energyuse > 0:
            self.delay_print("\nYou have safely retreated from the enemy.")
            self.delay_print(f"Retreating consumed {energyuse} energy.\n")
            self.energy -= energyuse
            break
        else:
            self.delay_print("\nInsufficient energy available to retreat from enemy.\n")
            self.fight()

    def obtainable_item(self, itemcat):
        """function to possibly drop an item and be obtained by player"""
        newitem = random_item(itemcat)
        if randomperc() <= float(items[newitem].rarity):
            if newitem in weaponitems:
                currentweapon = self.weapon
                self.swap_weapon(currentweapon, newitem)
            elif len(self.inventory) < self.inventory_size:
                print(f"You picked up {newitem}.\n")
                self.inventory.append(newitem)
            else:
                self.delay_print(f"Inventory Full! Max items of {self.inventory_size} reached.\n")

    def swap_weapon(self, currentweapon, newweapon):
        """swap weapon upon pickup function"""
        self.delay_print("The enemy dropped something...\n")
        display = displayitem(newweapon)
        print(display)
        currentweapon = self.weapon
        while True:
            playerchoice = input(f"\nDo you want trade your [{currentweapon}] for this? (y/n) \n\n")
            match playerchoice:
                case "y" | "Y":
                    self.delay_print(f"\nNew weapon equipped: [{newweapon}]\n")
                    self.weapon = newweapon
                case "n" | "N":
                    self.delay_print("\nYou decided to leave the weapon with the fallen.\n")
                case other:
                    self.delay_print(f"\n{other} is not an option.")
                    continue
            break
