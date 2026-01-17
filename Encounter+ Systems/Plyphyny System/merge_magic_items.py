import json
import re
import os

markdown_file = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/magic_items_update.md"
json_file = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/plyphyny_It2X/items.json"

# Load existing items
items_map = {}
if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        existing_items = json.load(f)
        for item in existing_items:
            # Clean duplicate names if any. Key by name.
            items_map[item['name']] = item

def get_type_category(header):
    header = header.lower()
    if 'amulets' in header: return 'Gear', 'Amulet'
    if 'armor' in header: return 'Armor', 'Armor' # Shields logic handled inside loop
    if 'weapons' in header: return 'Weapon', 'Weapon'
    if 'potions' in header: return 'Consumable', 'Potion'
    if 'rings' in header: return 'Gear', 'Ring'
    if 'rods' in header: return 'Gear', 'Rod/Staff/Wand'
    return 'Gear', 'Misc'

with open(markdown_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_type = 'Gear'
current_cat = 'Misc'
headers = []
in_table = False

for line in lines:
    line = line.strip()
    if line.startswith('####'):
        # New section
        section = line.replace('####', '').strip()
        current_type, current_cat = get_type_category(section)
        in_table = False
        continue

    if line.startswith('|'):
        if 'Item Name' in line:
            # Header row
            headers = [h.strip() for h in line.split('|')[1:-1]]
            headers = [h.lower() for h in headers]
            in_table = True
            continue
        if '---' in line:
            continue
        
        # Data row
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) != len(headers):
            continue
        
        row = dict(zip(headers, parts))
        
        name = row.get('item name', '').replace('**', '').strip()
        if not name: continue
        
        rarity = row.get('rarity', '')
        ep = row.get('energy points (ep)', '') or row.get('duration', '') # Potions use Duration col sometimes
        effect = row.get('effect', '')
        desc = row.get('description', '')
        
        # Determine specific category for Armor/Shields
        row_type = current_type
        row_cat = current_cat
        if 'Shield' in name:
            row_type = 'Shield'
            row_cat = 'Shield'
        
        # Format Notes
        notes = f"**Rarity:** {rarity}\n"
        if 'duration' in headers:
             notes += f"**Duration:** {row.get('duration', '')}\n"
        else:
             notes += f"**Energy Points:** {ep}\n"
        
        notes += f"\n**Description:** {desc}\n\n**Effect:** {effect}"
        
        # Create/Update Item
        item = {
            "name": name,
            "data": {
                "type": row_type,
                "category": row_cat,
                "notes": notes
            }
        }
        
        # Overwrite/Add
        items_map[name] = item

# Convert back to list
final_items = list(items_map.values())

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(final_items, f, indent=2)

print(f"Merged magic items. Total count: {len(final_items)}")
