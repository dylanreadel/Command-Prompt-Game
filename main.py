"""import standard libraries"""
import os
import random
import time
import sys
import csv
from collections import Counter

from items import displayitem, random_item, items, consumableitems, weaponitems, tokenitems
from rules import rules

# set directory to current directory
os.chdir('C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game')

# set save game file directory
savedirectory = "C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game/savegame/"

# saved files in directory
savedfiles = os.listdir(savedirectory)

# saved files in directory w/o file extensions
savedfiles_noext = [x.split('.')[0] for x in savedfiles]

# inventory saved file directory
invsavedirectory = "C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game/invsave/"

# random int 0 to 100 generator
def randomperc():
    """random percent function"""
    percent = float(random.randint(0, 100))
    return percent

# Global Variables
# starting player health
HEALTH = 100

# chance of safely walking forward
walkchance = float(50)

# chance of winning fight without weapon
fightchance = float(20)

############## GAME MECHANIC FUNCTIONS ##############

def walk(mp):
    """walk mechanic function"""
    if randomperc() <= walkchance:
        experiencegain = random.randint(0, 10)
        mp.delay_print(f"You safely walked forward. +{experiencegain} experience")
        mp.experience += experiencegain
        progression(mp)
    else:
        mp.delay_print("You encountered an enemy!\n")
        fightretreat = input("(f)ight or (r)etreat? ")
        if fightretreat == "f":
            fight(mp)
        elif fightretreat == "r":
            retreat(mp)
        else:
            mp.delay_print("Input is not an option.")

def fight(mp):
    """fight mechanic function"""
    mp.delay_print("\nYou chose to fight. An enemy approaches.\n")
    mp.delay_print("A battle breaks out!\n")
    print("---------------\n")
    time.sleep(mp.SPEED * 40)
    # success if random int is less/equal to total damage chance
    if randomperc() <= mp.playerdamage:
        mp.delay_print("You won the fight!\n")
        mp.delay_print("+5 Health\n")
        mp.health += 5
        mp.experience += 10
        mp.kills += 1
        progression(mp)
        mp.display_health()
        droppeditem(mp, weaponitems)
        droppeditem(mp, consumableitems)
    else:
        mp.delay_print("The enemy beat you this time.\n")
        mp.delay_print("-10 Health\n")
        mp.health -=10
        mp.display_health()

def retreat(mp):
    """retreat from fight function"""
    mp.delay_print("You have safely retreated from the enemy.")

def progression(mp):
    """level progression function"""
    if mp.experience >= 25 * mp.level**1.5:
        mp.level += 1
        mp.inventory.append(random_item(tokenitems))
        print("\n------------------------------------------\n")
        mp.delay_print("\nYou leveled up!")
        mp.delay_print(f"\nLevel {mp.level-1} -----> Level {mp.level}")
        mp.delay_print(f"""\nXP required to reach Level {mp.level + 1}: {int(25 * mp.level**1.5)}""")
        print("\n------------------------------------------\n")

def quitgame(mp):
    """quit game function"""
    save = input("Would you like to save the game? (y/n) ")
    if save == "y":
        savegame(mp)
    yesno = input("Are you sure you want to quit the game? (y/n) ")
    if yesno == "y":
        sys.exit()
    else:
        print("\n")
        return

def displayinventory(mp):
    """display inventory function"""
    print("-------------------------------------------------------------\n")
    print("INVENTORY MENU\n")
    counteditems = dict(Counter(mp.inventory))
    for item, count in counteditems.items():
        display = displayitem(item)
        print(str(count) + "x " + display)
    print("\n-------------------------------------------------------------\n")

def playerinventory(mp):
    """inventory menu function"""
    displayinventory(mp)
    playerchoice = input("Press enter to return to game\n")
    if playerchoice == "":
        return

def displaystats(mp):
    """display stats function"""
    print("-------------------------------------------------------------\n")
    print(f"        STATS MENU: {mp.name.title()}, {mp.age} years old\n")
    print(f"             Level: {mp.level}")
    print(f"        Experience: {mp.experience}\n")
    print(f"    Current Health: {mp.health}")
    print(f"   Equipped Weapon: {mp.weapon}")
    print(f"     Weapon Damage: {items[mp.weapon].points}")
    print(f"      Total Damage: {mp.playerdamage} (Base {fightchance} Damage + Weapon Damage)\n")
    print("-------------------------------------------------------------\n")

def displayadvancedstats(mp):
    """display advanced stats function"""
    print("-------------------------------------------------------------\n")
    print(f"ADVANCED STATS MENU: {mp.name.title()}, {mp.age} years old\n")
    print(f"   Enemies Executed: {mp.kills}\n")
    print("-------------------------------------------------------------\n")

def stats(mp):
    """stats menu function"""
    displaystats(mp)
    playerchoice = input("(a)dvanced stats or press enter to return to game\n")
    print("\n")
    if playerchoice == "a":
        displayadvancedstats(mp)
    elif playerchoice == "":
        return

def healmenu(mp):
    """heal menu function"""
    while mp.health < HEALTH:
        print("\n------------------------Healing Menu-------------------------\n")
        mp.display_health()
        displayinventory(mp)
        print("Type a consumable, healing item from your inventory to heal.")
        inputitem = input("(or press ENTER to return to game) \n\n")
        if inputitem in mp.inventory:
            healitem(mp, inputitem)
        elif inputitem == "":
            break
        else:
            mp.delay_print("\nItem not found in inventory.")
            continue
        choice = input("Do you want to heal again? (y/n) \n")
        if choice == "y":
            continue
        else:
            break
    print("-------------------------------------------------------------\n")
    mp.delay_print(f"Health cannot be greater than {HEALTH}.")

def healitem(mp, item):
    """determine if inventory item can heal"""
    if items[item].use == "heal":
        if mp.health + int(items[item].points) < HEALTH:
            mp.health += int(items[item].points)
            mp.delay_print(f"\nYou consumed 1 {item} to increase your health by {items[item].points}.\n")
            mp.display_health()
        else:
            mp.health = HEALTH
            mp.delay_print(f"\nYou consumed 1 {item} to increased your health to max ({HEALTH}).")
        index_item = mp.inventory.index(item)
        mp.inventory.pop(index_item)
    else:
        mp.delay_print("\nItem found in inventory but cannot be consumed for healing.")
        healmenu(mp)

def options(mp):
    """options menu function"""
    print("Options:\n")
    print("(i)nventory")
    print("(s)tats")
    print("(h)eal")
    print("(g)ame speed")
    print("(r)ules")
    print("(q)uit\n")
    playerchoice = input("-------> ")
    print("\n")
    match playerchoice:
        case "i" | "I":
            playerinventory(mp)
        case "s" | "S":
            stats(mp)
        case "h" | "H":
            healmenu(mp)
        case "g" | "G":
            mp.game_speed()
        case "q" | "Q":
            quitgame(mp)
        case "r" | "R":
            rules()
        case _:
            print("Not an option, try again.\n")

def droppeditem(mp, itemcat):
    """function to possibly drop an item based on set probability
    and randomly choose an item from defined lists"""
    newitem = random_item(itemcat)
    if randomperc() <= float(items[newitem].rarity):
        mp.delay_print("The enemy dropped something...\n")
        display = displayitem(newitem)
        print(display)
        if newitem in weaponitems:
            olditem = mp.weapon
            playerchoice = input(f"\nDo you want trade your current weapon [{olditem}] for this? (y/n) \n\n")
            if playerchoice == "y":
                print("\n")
                mp.delay_print(f"\nYou swapped [{olditem}] for [{newitem}].\n")
                mp.weapon = newitem
            else:
                mp.delay_print("\nYou left the item on the ground and walked away.\n")
        else:
            print(f"\nYou picked up {newitem}.\n")
            mp.inventory.append(newitem)

def loadgame():
    """load game function"""
    print("\nCurrent game saves: \n")
    for file in savedfiles_noext:
        print(file)
    print("\n")
    print("Type the saved game file name to continue your adventure: ")
    gamesave = input() + ".csv"
    gamesave_reader = csv.DictReader(open(savedirectory + gamesave, encoding="UTF-8"))
    gamesave_dict = {}
    for gamesave_row in gamesave_reader:
        gamesave_key = gamesave_row.pop('key')
        if gamesave_key in gamesave_dict:
            pass
        gamesave_dict[gamesave_key] = gamesave_row
        mp = Player(name = gamesave_dict["savedvalues"]["name"],
                            age = gamesave_dict["savedvalues"]["age"],
                            health = gamesave_dict["savedvalues"]["health"],
                            inventory = [],
                            weapon = gamesave_dict["savedvalues"]["weapon"],
                            playerdamage = gamesave_dict["savedvalues"]["playerdamage"],
                            experience = gamesave_dict["savedvalues"]["experience"],
                            level = gamesave_dict["savedvalues"]["level"],
                            kills = gamesave_dict["savedvalues"]["kills"],
                            SPEED = gamesave_dict["savedvalues"]["SPEED"])
    with open(invsavedirectory + gamesave_dict["savedvalues"]["inventory"] + ".csv", "r", encoding="UTF-8") as savedinv:
        savedinv = list(csv.reader(savedinv, delimiter=','))
        for invrow in savedinv:
            for saveditem in invrow:
                mp.inventory.append(saveditem)
    print("\n------------------------------------------\n")
    mp.delay_print(f"Welcome back to the Game, {mp.name.title()}!\n")
    displaystats(mp)
    return mp

def savegame(mp):
    """save game function"""
    print("\nCurrent game saves: \n")
    for file in savedfiles_noext:
        print(file)
    print("\n")
    savefile = input("Enter a name for your save game: ")
    with open(savedirectory + savefile + ".csv", 'w',
              newline='', encoding="UTF-8") as csvfile:
        savewriter = csv.writer(csvfile, delimiter=',')
        savewriter.writerow(["key",
                            "name",
                            "age",
                            "health",
                            "inventory",
                            "weapon",
                            "playerdamage",
                            "experience",
                            "level",
                            "kills",
                            "SPEED"])
        savewriter.writerow(["savedvalues",
                            mp.name,
                            mp.age,
                            mp.health,
                            "inv_" + savefile,
                            mp.weapon,
                            mp.playerdamage,
                            mp.experience,
                            mp.level,
                            mp.kills,
                            mp.SPEED])
    with open(invsavedirectory + "inv_" + savefile + ".csv", "w",
              newline='', encoding="UTF-8") as csvfile:
        invsavewriter = csv.writer(csvfile, delimiter=',')
        invsavewriter.writerow(mp.inventory)

def newgame():
    """new game function"""
    print("Let's start a new game!\n")
    name = playername()
    age = playerage(name)
    # instantiate player
    mp = Player(name,
                        age,
                        health = HEALTH,
                        inventory = [],
                        weapon = "dagger",
                        playerdamage = float(),
                        experience = 0,
                        level = 1,
                        kills = 0,
                        SPEED = 0.05)
    mp.welcome()
    return mp

def playername():
    """name get function"""
    while True:
        print("\nWhat is your character's name? \n")
        name = input()
        if len(name) > 0 and len(name) <= 16:
            return name
        print("Name must be between 1 and 16 characters.\n")
        continue

def playerage(name):
    """age get function"""
    while True:
        print(f"\nHow old is {name.title()}? \n")
        age = input()
        if age.strip().isdigit():
            if int(age) < 100 and int(age) >= 18:
                return age
            print("Age must fall between 18 and 99.\n")
        print(f"{age} is not a valid age.\n")
        continue

class Player:
    """Class representing a Player"""

    def __init__(self, name, age, health, inventory,
                 weapon, playerdamage, experience,
                 level, kills, SPEED):
        """player initialization"""
        self.name = name
        self.age = age
        self._health = int(health)
        self.inventory = inventory
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
        if health >= 100:
            self._health = 100
        else:
            self._health = health

    def display_health(self):
        """display health function"""
        if self._health % 2 == 0:
            print("Health: " + ("{}" * int(self._health / 10)), str(self._health), "\n")
        else:
            num = self._health - 5
            print("Health: " + ("{}" * int(num / 10)) + "{", str(self._health), "\n")
   
    def game_speed(self):
        """game speed function to determine print and sleep times"""
        speedinput = input("\nSet Game Speed: (s)lug | (c)at | (f)alcon \n\n")
        match speedinput:
            case "s" | "S":
                print("\nGame speed set to slug pace.\n")
                self.SPEED = 0.08
            case "c" | "C":
                print("\nGame speed set to cat pace.\n")
                self.SPEED = 0.04
            case "f" | "F":
                print("\nGame speed set to falcon pace.\n")
                self.SPEED = 0
            case other:
                print(f"\n{other} not an option.")

        if speedinput == "s":
            print("\nGame speed set to slug pace.\n")
            self.SPEED = 0.04
        elif speedinput == "c":
            print("\nGame speed set to cat pace.\n")
            self.SPEED = 0.02
        elif speedinput == "f":
            print("\nGame speed set to falcon pace.\n")
            self.SPEED = 0
        else:
            print("\nNot an option.")

    def welcome(self):
        """welcome message"""
        print("\n------------------------------------------\n")
        self.game_speed()
        self.delay_print(f"Welcome to the Game, {self.name.title()}!")
        self.delay_print(f"Your character is {self.age} years old.\n")
        startinv = ["apple", "chips", "bandage", "apple"]
        self.inventory.extend(startinv)
        self.playerdamage = float(items[self.weapon].points) + fightchance
        time.sleep(self.SPEED * 40)
        rules()
        time.sleep(self.SPEED * 300)
        displaystats(self)
        time.sleep(self.SPEED * 200)
        displayinventory(self)
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

def main():
    """main game function"""
    print("\n   _______________________________________")
    print("  |                                       |")
    print("  |           T H E     G A M E           |")
    print("  |                                       |")
    print("  |                by DR                  |")
    print("  |                                       |")
    print("  |    (N)ew Game    |    (L)oad Game     |")
    print("  |_______________________________________|\n")
    playerchoice = input()
    print("\n")
    match playerchoice:
        case "l" | "L":
            mp = loadgame()
        case "n" | "N":
            mp = newgame()
        case other:
            print(f"{playerchoice} is not an option.")
            print("Exiting Game")
            sys.exit()
    while mp.health > 0:
        mp.playerdamage = float(items[mp.weapon].points) + fightchance
        print("-------------------------------------------------------------\n")
        playerchoice = input("Choose your option: [ (w)alk, (f)ight, or (o)ptions ] : ")
        print("\n")
        match playerchoice:
            case "w":
                walk(mp)
            case "f":
                fight(mp)
            case "o":
                options(mp)
            case other:
                print(f"{other} is not an option.")
        while mp.health <= 0:
            playagain = input("You didn't make it this time...Do you want to play again? (y/n) ")
            if playagain == "y":
                mp.delay_print("\nLet's play again!\n")
                main()
            else:
                break

if __name__ == "__main__":
    main()
