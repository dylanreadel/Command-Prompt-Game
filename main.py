"""import standard libraries"""
import sys
from items import items
from player import loadgame, newgame, walk, fight, options, fightchance

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
            mp = loadgame()
        case "n" | "N":
            mp = newgame()
        case other:
            print(f"{other} is not an option.")
            print("Exiting Game")
            sys.exit()
    return mp

def main_game_loop():
    """main game loop"""
    mp = game_start()
    while mp.health > 0:
        mp.playerdamage = float(items[mp.weapon].points) + fightchance
        print("-------------------------------------------------------------\n")
        if mp.health < 50:
            mp.delay_print("Reminder! Heal in the options menu.\n")
            mp.display_health()
        playerchoice = input("Choose your option: [ (w)alk, (f)ight, or (o)ptions ] : ")
        print("\n")
        match playerchoice:
            case "w" | "W":
                walk(mp)
            case "f" | "F":
                fight(mp)
            case "o" | "O":
                options(mp)
            case other:
                print(f"{other} is not an option.")
    return mp

def game_over(mp):
    """game over sequence"""
    i = 0
    while i < 1:
        playagain = input("You didn't make it this time...Do you want to play again? (y/n) ")
        print("\n")
        match playagain:
            case "y" | "Y":
                mp.delay_print("\nLet's play again!\n")
                i += 1
                main()
            case "n" | "N":
                i += 1
                sys.exit()
            case other:
                mp.delay_print(f"{other} is not an option.\n")

def main():
    """main function"""
    mp = main_game_loop()
    game_over(mp)

if __name__ == "__main__":
    main()
