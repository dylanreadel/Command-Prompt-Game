"""import modules"""
import os

import random
import time
import sys
import csv

from delayprint import delay_print

# set directory to current directory
os.chdir('C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame')

# create dictionary of all items to be used in the game
reader = csv.DictReader(open("items.csv", encoding="UTF-8"))

allitems = {}
for row in reader:
    key = row.pop('itemname')
    if key in allitems:
        pass
    allitems[key] = row

# create blank lists split by item categories for random choices
weaponitems = []
consumableitems = []
tokenitems = []

# assign items to lists based on categories
for i, j in allitems.items():
    if j["category"] == "consumable":
        consumableitems.append(i)
    elif j["category"] == "weapon":
        weaponitems.append(i)
    else:
        tokenitems.append(i)

def randomitem(itemcategory):
    """random item function"""
    return random.choice(itemcategory)

# random int 0 to 100 generator
def randomperc():
    """random percent function"""
    percent = float(random.randint(0, 100))
    return percent

# Global Variables
# starting player health
HEALTH = 100

# 80% chance of safely walking forward
walkchance = float(50)

# 25% chance of winning fight without weapon
fightchance = float(20)

# 50% chance of acquiring item from enemy
itemchance = float(33.33)

############## GAME MECHANIC FUNCTIONS ##############

def walk(mainplayer):
    """walk mechanic function"""
    if randomperc() <= walkchance:
        experiencegain = random.randint(0, 10)
        delay_print(f"You safely walked forward. +{experiencegain} experience")
        mainplayer.experience += experiencegain
        progression(mainplayer)
    else:
        delay_print("You encountered an enemy!\n")
        fightretreat = input("(f)ight or (r)etreat? ")
        if fightretreat == "f":
            fight(mainplayer)
        else:
            retreat()

def fight(mainplayer):
    """fight mechanic function"""
    delay_print("You chose to fight. An enemy approaches.\n")
    delay_print("A battle breaks out!\n")
    print("---------------\n")
    time.sleep(2)
    # success if random int is less/equal to total damage chance
    if randomperc() <= mainplayer.playerdamage:
        delay_print("You won the fight!\n")
        delay_print("+5 Health\n")
        mainplayer.health += 5
        mainplayer.experience += 10
        mainplayer.kills += 1
        progression(mainplayer)
        print(f"Current Health: {mainplayer.health}\n")
        droppeditem(mainplayer)
    else:
        delay_print("The enemy beat you this time.\n")
        delay_print("-10 Health\n")
        mainplayer.health -=10
        print(f"Current Health: {mainplayer.health}\n")

def retreat():
    """retreat from fight function"""
    delay_print("You have safely retreated from the enemy.")

def progression(mainplayer):
    """level progression function"""
    if mainplayer.experience >= 25 * mainplayer.level**1.5:
        mainplayer.level += 1
        print("\n------------------------------------------\n")
        delay_print("\nYou leveled up!")
        delay_print(f"\nLevel {mainplayer.level-1} -----> Level {mainplayer.level}")
        delay_print(f"""\nexperience required to reach Level {mainplayer.level + 1}:
                    {int(25 * mainplayer.level**1.5)}""")
        print("\n------------------------------------------\n")

def quitgame():
    """quit game function"""
    yesno = input("Are you sure you want to quit the game? (y/n) ")
    if yesno == "y":
        sys.exit()
    else:
        print("\n")
        return

def displayinventory(mainplayer):
    """display inventory function"""
    print("-------------------------------------------------------------\n")
    print("INVENTORY MENU\n")
    for item in mainplayer.inventory:
        displayitem(item)
    print("\n-------------------------------------------------------------\n")

def playerinventory(mainplayer):
    """inventory menu function"""
    displayinventory(mainplayer)
    playerchoice = input("Press enter to return to game\n")
    if playerchoice == "":
        return

def displaystats(mainplayer):
    """display stats function"""
    print("-------------------------------------------------------------\n")
    print(f"        STATS MENU: {mainplayer.name.title()}, {mainplayer.age} years old\n")
    print(f"             Level: {mainplayer.level}")
    print(f"        Experience: {mainplayer.experience}\n")
    print(f"    Current Health: {mainplayer.health}")
    print(f"   Equipped Weapon: {mainplayer.weapon}")
    print(f"     Weapon Damage: {allitems[mainplayer.weapon]['points']}")
    print(f"      Total Damage: {mainplayer.playerdamage} (Base {fightchance} Damage + Weapon Damage)\n")
    print("-------------------------------------------------------------\n")

def displayadvancedstats(mainplayer):
    """display advanced stats function"""
    print("-------------------------------------------------------------\n")
    print(f"ADVANCED STATS MENU: {mainplayer.name.title()}, {mainplayer.age} years old\n")
    print(f"   Enemies Executed: {mainplayer.kills}\n")
    print("-------------------------------------------------------------\n")

def stats(mainplayer):
    """stats menu function"""
    displaystats(mainplayer)
    playerchoice = input("(a)dvanced stats or press enter to return to game\n")
    print("\n")
    if playerchoice == "a":
        displayadvancedstats(mainplayer)
    elif playerchoice == "":
        return

def heal(mainplayer):
    """heal menu function"""
    print("-----------Healing Menu-----------\n")
    displayinventory(mainplayer)
    inputitem = input("Type a consumable, healing item from your inventory: ")
    invitems = mainplayer.inventory
    if inputitem in invitems:
        if allitems[inputitem]["use"] == "heal":
            if mainplayer.health + float(allitems[inputitem]["points"]) <= HEALTH:
                index_item = invitems.index(inputitem)
                mainplayer.health += float(allitems[inputitem]["points"])
                mainplayer.inventory.pop(index_item)
                delay_print(f"""\nYou consumed 1 {inputitem} to increase your health
                            by {float(allitems[inputitem]['points'])} to {mainplayer.health}.\n""")
            else:
                delay_print(f"\nHealth cannot be greater than {HEALTH}.")
        else:
            delay_print("\nItem found in inventory but cannot be consumed for healing.")
            heal(mainplayer)
    else:
        delay_print("\nItem not found in inventory.")
        heal(mainplayer)
    print("----------------------------------\n")

def options(mainplayer):
    """options menu function"""
    print("Options:\n")
    print("(i)nventory")
    print("(s)tats")
    print("(h)eal")
    print("(q)uit\n")
    playerchoice = input("-------> ")
    print("\n")
    match playerchoice:
        case "i":
            playerinventory(mainplayer)
        case "s":
            stats(mainplayer)
        case "h":
            heal(mainplayer)
        case "q":
            quitgame()
        case _:
            print("Not an option, try again.\n")

def displayitem(item):
    """item display function"""
    print(f"""{item} : A {allitems[item]['category']} item used to
          {allitems[item]['use']} {allitems[item]['points']} points.""")

def droppeditem(mainplayer):
    """function to possibly drop an item based on set probability
    and randomly choose an item from defined lists"""
    if randomperc() <= itemchance:
        newitem = randomitem(weaponitems)
        delay_print("The enemy dropped something...")
        displayitem(newitem)
        olditem = mainplayer.weapon
        playerchoice = input(f"\nDo you want trade your current weapon [{olditem}] for this? (y/n) \n")
        if playerchoice == "y":
            print("\n")
            delay_print(f"\nYou swapped [{olditem}] for [{newitem}].\n")
            mainplayer.weapon = newitem
        else:
            delay_print("\nYou left the item on the ground and walked away.")
    else:
        delay_print("--the enemy dropped nothing--\n")

def loadgame():
    """load game function"""
    delay_print("Type the saved game file name to continue your adventure: ")
    gamesave = input() + ".csv"
    gamesave_reader = csv.DictReader(open(gamesave, encoding="UTF-8"))
    gamesave_dict = {}
    for gamesave_row in gamesave_reader:
        gamesave_key = gamesave_row.pop('key')
        if gamesave_key in gamesave_dict:
            pass
        gamesave_dict[gamesave_key] = gamesave_row
        mainplayer = Player(name = gamesave_dict["savedvalues"]["name"],
                            age = gamesave_dict["savedvalues"]["age"],
                            health = gamesave_dict["savedvalues"]["health"],
                            inventory = [],
                            weapon = gamesave_dict["savedvalues"]["weapon"],
                            playerdamage = gamesave_dict["savedvalues"]["playerdamage"],
                            experience = gamesave_dict["savedvalues"]["experience"],
                            level = gamesave_dict["savedvalues"]["level"],
                            kills = gamesave_dict["savedvalues"]["kills"])
    with open(gamesave_dict["savedvalues"]["inventory"] + ".csv", "r", encoding="UTF-8") as savedinv:
        savedinv = list(csv.reader(savedinv, delimiter=','))
        for invrow in savedinv:
            for saveditem in invrow:
                mainplayer.inventory.append(saveditem)
    print("\n------------------------------------------\n")
    delay_print(f"Welcome back to the Game, {mainplayer.name}!\n")
    displaystats(mainplayer)
    return mainplayer

def newgame():
    """new game function"""
    delay_print("Let's start a new game!\n")
    name = playername()
    age = playerage(name)
    # instantiate player
    mainplayer = Player(name,
                        age,
                        health = HEALTH,
                        inventory = [],
                        weapon = "dagger",
                        playerdamage = float(),
                        experience = 0,
                        level = 1,
                        kills = 0)
    mainplayer.welcome()
    return mainplayer

def playername():
    """name get function"""
    while True:
        delay_print("\nWhat is your character's name? ")
        name = input()
        if len(name) > 0 and len(name) <= 16:
            return name
        print("Name must be between 1 and 16 characters.")
        continue

def playerage(name):
    """age get function"""
    while True:
        delay_print(f"\nHow old is {name.title()}? ")
        age = input()
        if age.strip().isdigit():
            if int(age) < 100 and int(age) >= 18:
                return age
            print("Age must fall between 18 and 99.")
        delay_print(f"{age} is not a valid age.")
        continue

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

def main():
    """main game function"""
    playerchoice = input("(N)ew Game or (L)oad Game? ")
    print("\n")
    if playerchoice == "l" or playerchoice == "L":
        mainplayer = loadgame()
    elif playerchoice == "n" or playerchoice == "N":
        mainplayer = newgame()
    while mainplayer.health > 0:
        mainplayer.playerdamage = float(allitems[mainplayer.weapon]["points"]) + fightchance
        print("-------------------------------------------------------------\n")
        playerchoice = input("Choose your option: [ (w)alk, (f)ight, or (o)ptions] : ")
        print("\n")
        match playerchoice:
            case "w":
                walk(mainplayer)
            case "f":
                fight(mainplayer)
            case "o":
                options(mainplayer)
            case other:
                print(f"{other} is not an option.")
        while mainplayer.health <= 0:
            playagain = input("You lost :( Do you want to play again? (y/n) ")
            if playagain == "y":
                delay_print("\nLet's play again!\n")
                main()
            else:
                break

main()
