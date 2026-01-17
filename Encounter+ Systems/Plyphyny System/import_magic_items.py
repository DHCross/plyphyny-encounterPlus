import json
import re

input_file = "/Users/dancross/Documents/GitHub/eldritch-gm-tool-sui/Eldritch Rules 8.17.2025.txt"
existing_items_file = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/plyphyny_It2X/items.json"

# Load existing items
try:
    with open(existing_items_file, 'r', encoding='utf-8') as f:
        items = json.load(f)
except:
    items = []

# Define line range
START_LINE = 5313
END_LINE = 5460

new_items = []
current_category = "Gear"
current_subcategory = "Misc"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract chunk
chunk = lines[START_LINE:END_LINE]

item_regex = re.compile(r'\*\*(.*?):\*\*\s*(.*)')

for line in chunk:
    line = line.strip()
    if not line:
        continue
    
    # Check if section header
    if line in ["Amulets", "Armor", "Shields", "Garments", "Melee Weapons", "Potions", "Ranged Weapons", "Magic Rings", "Rods, Staffs & Wands"]:
        if line == "Amulets": current_category = "Gear"; current_subcategory = "Amulet"
        elif line == "Armor": current_category = "Armor"; current_subcategory = "Armor"
        elif line == "Shields": current_category = "Shield"; current_subcategory = "Shield"
        elif line == "Garments": current_category = "Gear"; current_subcategory = "Garment"
        elif line == "Melee Weapons": current_category = "Weapon"; current_subcategory = "Melee Weapon"
        elif line == "Potions": current_category = "Consumable"; current_subcategory = "Potion"
        elif line == "Ranged Weapons": current_category = "Weapon"; current_subcategory = "Ranged Weapon"
        elif line == "Magic Rings": current_category = "Gear"; current_subcategory = "Ring"
        elif line == "Rods, Staffs & Wands": current_category = "Gear"; current_subcategory = "Rod/Staff/Wand"
        continue

    # Match Item
    match = item_regex.match(line)
    if match:
        name = match.group(1).strip()
        details = match.group(2).strip()
        
        # Parse details: "Rarity: X, Potency: Y, Energy Points: Z, Description: D, Effect: E"
        # We can split by comma spaces, but description might have commas.
        # Strategy: Regex for key fields.
        
        rarity_m = re.search(r'Rarity: (.*?)(,|$)', details)
        potency_m = re.search(r'Potency: (.*?)(,|$)', details)
        ep_m = re.search(r'Energy Points: (.*?)(,|$)', details)
        
        # Description is tricky. "Description: ..... Effect:"
        desc_m = re.search(r'Description: (.*?)( Effect:|$)', details)
        effect_m = re.search(r'Effect: (.*)', details)
        
        rarity = rarity_m.group(1).strip() if rarity_m else ""
        potency = potency_m.group(1).strip() if potency_m else ""
        ep = ep_m.group(1).strip() if ep_m else ""
        desc = desc_m.group(1).strip() if desc_m else ""
        effect = effect_m.group(1).strip() if effect_m else ""
        
        # Construct item
        item = {
            "name": name,
            "data": {
                "type": current_category,
                "category": current_subcategory,
                "notes": f"**Rarity:** {rarity}\n**Potency:** {potency}\n**Energy Points:** {ep}\n\n**Description:** {desc}\n\n**Effect:** {effect}"
            }
        }
        
        # Refine Weapons
        if current_category == "Weapon":
             # Try to parse damage type or range from text? Hard.
             # Just leave stats empty, manual entry required for sophisticated fields.
             pass

        new_items.append(item)

# Merge
# Avoid duplicates
existing_names = {i['name'] for i in items}
for i in new_items:
    if i['name'] not in existing_names:
        items.append(i)

with open(existing_items_file, 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2)

print(f"Added {len(new_items)} magic items. Total items: {len(items)}")
