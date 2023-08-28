"""import"""
import csv
from player import Player, HEALTH
from constants import savedfiles_noext, SAVE_GAME_DIR, SAVE_GAME_INV_DIR

def loadgame():
    """load game function"""
    print("\nCurrent game saves: \n")
    for file in savedfiles_noext:
        print(file)
    print("\n")
    print("Type the saved game file name to continue your adventure: ")
    gamesave = input() + ".csv"
    gamesave_reader = csv.DictReader(open(SAVE_GAME_DIR + gamesave, encoding="UTF-8"))
    gamesave_dict = {}
    for gamesave_row in gamesave_reader:
        gamesave_key = gamesave_row.pop('key')
        if gamesave_key in gamesave_dict:
            pass
        gamesave_dict[gamesave_key] = gamesave_row
        player = Player(name = gamesave_dict["savedvalues"]["name"],
                            age = gamesave_dict["savedvalues"]["age"],
                            health = gamesave_dict["savedvalues"]["health"],
                            inventory = [],
                            weapon = gamesave_dict["savedvalues"]["weapon"],
                            playerdamage = gamesave_dict["savedvalues"]["playerdamage"],
                            experience = gamesave_dict["savedvalues"]["experience"],
                            level = gamesave_dict["savedvalues"]["level"],
                            kills = gamesave_dict["savedvalues"]["kills"],
                            SPEED = gamesave_dict["savedvalues"]["SPEED"])
    with open(SAVE_GAME_INV_DIR + gamesave_dict["savedvalues"]["inventory"]
              + ".csv", "r", encoding="UTF-8") as savedinv:
        savedinv = list(csv.reader(savedinv, delimiter=','))
        for invrow in savedinv:
            for saveditem in invrow:
                player.inventory.append(saveditem)
    print("\n------------------------------------------\n")
    player.delay_print(f"Welcome back to the Game, {player.name.title()}!\n")
    player.displaystats()
    return player

def newgame():
    """new game function"""
    print("Let's start a new game!\n")
    name = playername()
    age = playerage(name)
    # instantiate player
    player = Player(name,
                        age,
                        health = HEALTH,
                        inventory = [],
                        weapon = "dagger",
                        playerdamage = float(),
                        experience = 0,
                        level = 1,
                        kills = 0,
                        SPEED = 0.05)
    player.welcome()
    return player

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
