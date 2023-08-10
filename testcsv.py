import csv

reader = csv.DictReader(open("items.csv"))

allitems = {}
for row in reader:
    key = row.pop('itemname')
    if key in allitems:
        pass
    allitems[key] = row

print(allitems)
