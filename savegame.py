"""import"""
import csv
from constants import savedfiles_noext, SAVE_GAME_DIR, SAVE_GAME_INV_DIR

def savegame(player):
    """save game function"""
    file = file_input()
    file = check_for_overwrite(file, player)
    write_to_file(file, player)

def file_input():
    """receive save file input from user"""
    print("\nCurrent game saves: \n")
    for file in savedfiles_noext:
        print(file)
    print("\n")
    file = input("Enter a name for your save game: ")
    print("\n")
    return file

def check_for_overwrite(file, player):
    """check if user input for save file is already used"""
    if file in savedfiles_noext:
        print("Save name already found in saved games.\n")
        yesno = input(f"Do you want to overwrite save [{file}]? (y/n) ")
        print("\n")
        match yesno:
            case "y" | "Y":
                return file
            case "n" | "N":
                savegame(player)
            case other:
                print(f"{other} is not an option.\n")
    else:
        return file

def write_to_file(file, player):
    """write game info to save file"""
    with open(SAVE_GAME_DIR + file + ".csv", 'w',
              newline='', encoding="UTF-8") as csvfile:
        savewriter = csv.writer(csvfile, delimiter=',')
        savewriter.writerow(["key",
                            "name",
                            "age",
                            "health",
                            "energy",
                            "inventory",
                            "weapon",
                            "playerdamage",
                            "experience",
                            "level",
                            "kills",
                            "SPEED"])
        savewriter.writerow(["savedvalues",
                            player.name,
                            player.age,
                            player.health,
                            player.energy,
                            "inv_" + file,
                            player.weapon,
                            player.playerdamage,
                            player.experience,
                            player.level,
                            player.kills,
                            player.SPEED])
    with open(SAVE_GAME_INV_DIR + "inv_" + file + ".csv", "w",
              newline='', encoding="UTF-8") as csvfile:
        invsavewriter = csv.writer(csvfile, delimiter=',')
        invsavewriter.writerow(player.inventory)
    print(f"Game saved successfully! Save: [{file}]\n")
