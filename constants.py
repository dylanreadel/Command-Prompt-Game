"""import"""
import random
import os

# random int 0 to 100 generator
def randomperc():
    """random percent function"""
    percent = float(random.randint(0, 100))
    return percent

# Global Variables
# starting player health
HEALTH = 100

# starting player energy
ENERGY = 100

# starting inventory size
INVENTORY_SIZE = 10

# chance of safely walking forward
walkchance = float(50)

# chance of winning fight without weapon
fightchance = float(20)

# set directory to current directory
os.chdir('C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game')

# set save game file directory
SAVE_GAME_DIR = "C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game/savegame/"

# inventory saved file directory
SAVE_GAME_INV_DIR = "C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game/invsave/"

# saved files in directoryd
savedfiles = os.listdir(SAVE_GAME_DIR)

# saved files in directory w/o file extensions
savedfiles_noext = [x.split('.')[0] for x in savedfiles]
