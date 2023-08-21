"""import csv library"""
import csv
import random

class Item:
    """defining instantiation of Item class"""
    def __init__(self, row, header, item_id):
        self.__dict__ = dict(zip(header, row))
        self.item_id = item_id
    def __repr__(self):
        return self.item_id

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
    match items[item].rarity:
        case "80":
            return "BASIC"
        case "60":
            return "EPIC"
        case "40":
            return "ULTRA"
        case "20":
            return "LEGENDARY"

def displayitem(item):
    """item display function"""
    rarity = rarity_label(item)
    cat = items[item].category
    use = items[item].use
    points = items[item].points
    print(f"[ {item} ({rarity}) ] : A {cat} item used to {use} {points} points.")

displayitem("sword")
