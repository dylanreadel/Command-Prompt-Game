"""import standard libraries"""
import sys
import os

# import other functions, classes, constants
from items import items
from constants import fightchance
from loadgame import loadgame, newgame

# set directory to current directory
os.chdir('C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game')

def game_start():
    """game start sequence"""
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
            player = loadgame()
        case "n" | "N":
            player = newgame()
        case other:
            print(f"{other} is not an option.")
            print("Exiting Game")
            sys.exit()
    return player

def main_game_loop(player):
    """main game loop"""
    while player.health > 0:
        player.playerdamage = float(items[player.weapon].points) + fightchance
        print("-------------------------------------------------------------\n")
        if player.health < 50:
            player.delay_print("Reminder! Heal in the options menu.\n")
            player.display_health()
        playerchoice = input("Choose your option: [ (w)alk, (f)ight, or (o)ptions ] : ")
        print("\n")
        match playerchoice:
            case "w" | "W":
                player.walk()
            case "f" | "F":
                player.fight()
            case "o" | "O":
                player.options()
            case other:
                print(f"{other} is not an option.")
    return player

def game_over(player):
    """game over sequence"""
    i = 0
    while i < 1:
        playagain = input("You didn't make it this time...Do you want to play again? (y/n) ")
        print("\n")
        match playagain:
            case "y" | "Y":
                player.delay_print("\nLet's play again!\n")
                i += 1
                main()
            case "n" | "N":
                i += 1
                sys.exit()
            case other:
                player.delay_print(f"{other} is not an option.\n")

def main():
    """main function"""
    player = game_start()
    main_game_loop(player)
    game_over(player)

if __name__ == "__main__":
    main()
