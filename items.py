"""import csv library"""
import csv
import random
import os

class Item:
    """defining instantiation of Item class"""
    def __init__(self, row, header, item_id):
        self.__dict__ = dict(zip(header, row))
        self.item_id = item_id
    def __repr__(self):
        return self.item_id

# set directory to current directory
os.chdir('C:/Users/dylan/Documents/Code Projects/VSCode Projects/CommandPromptGame/Command-Prompt-Game')

# read in item csv as a list
with open('items.csv', encoding="UTF-8") as itemdata:
    itemslist = list(csv.reader(itemdata))

# create instance of each row item in list,
# assign item ID to each item in list,
# add ability to call items by name
items = {a[0]:Item(a, itemslist[0], f"item_{i+1}") for i, a in enumerate(itemslist[1:])}

# create empty lists to hold different item types
# for random item assignment
consumableitems = []
weaponitems = []
tokenitems = []

# assign each item to list based on category
for i in items:
    match items[i].category:
        case "consumable":
            consumableitems.append(i)
        case "weapon":
            weaponitems.append(i)
        case "token":
            tokenitems.append(i)

def random_item(category):
    """return random item based on inputted category"""
    return random.choice(category)

# rarity labels
def rarity_label(item):
    """defining rarity label function"""
    rarityint = int(items[item].rarity)
    if rarityint > 80:
        rarity = "POOR"
    elif rarityint > 60:
        rarity = "DECENT"
    elif rarityint > 40:
        rarity = "EPIC"
    elif rarityint > 20:
        rarity = "FABLED"
    elif rarityint > 0:
        rarity = "MYTHICAL"
    return rarity

def displayitem(item):
    """item display function"""
    rarity = rarity_label(item)
    cat = items[item].category
    use = items[item].use
    points = items[item].points
    n = 40 - (len(item) + 12)
    m = int((10 - len(rarity)) / 2)
    return f" {item}" + (" " * n) + "[" + (" " * m) + f"{rarity}" + (" " * m) + f"] : A {cat} item used to {use} {points} points."

# TEST
# displayitem("apple")
