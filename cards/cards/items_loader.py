import json

with open("cards/cards/items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(items)