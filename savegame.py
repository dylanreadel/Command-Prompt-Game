"""import"""
import csv
from constants import savedfiles_noext, SAVE_GAME_DIR, SAVE_GAME_INV_DIR

def savegame(player):
    """save game function"""
    print("\nCurrent game saves: \n")
    for file in savedfiles_noext:
        print(file)
    print("\n")
    savefile = input("Enter a name for your save game: ")
    with open(SAVE_GAME_DIR + savefile + ".csv", 'w',
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
                            player.name,
                            player.age,
                            player.health,
                            "inv_" + savefile,
                            player.weapon,
                            player.playerdamage,
                            player.experience,
                            player.level,
                            player.kills,
                            player.SPEED])
    with open(SAVE_GAME_INV_DIR + "inv_" + savefile + ".csv", "w",
              newline='', encoding="UTF-8") as csvfile:
        invsavewriter = csv.writer(csvfile, delimiter=',')
        invsavewriter.writerow(player.inventory)
