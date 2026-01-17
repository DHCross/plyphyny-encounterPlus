import csv
import json
import os

input_csv = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny or Eldritch Spells/grimoire_index sheets - Grimoire.csv"
output_json = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/plyphyny_It2X/spells.json"

spells = []

try:
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Skip empty rows or rows without a name (if any)
            if not row.get('Spell Name'):
                continue

            spell = {
                "name": row['Spell Name'],
                "data": {
                    "path": row.get('Path', ''),
                    "category": row.get('Category', ''),
                    "tier": row.get('Tier', ''),
                    "rank": row.get('Rank/Die', ''),
                    "rarity": row.get('Rarity', ''),
                    "effects": row.get('Effects', ''),
                    "notes": row.get('Notes', '')
                }
            }
            spells.append(spell)

    with open(output_json, mode='w', encoding='utf-8') as jsonfile:
        json.dump(spells, jsonfile, indent=2)

    print(f"Successfully converted {len(spells)} spells to {output_json}")

except Exception as e:
    print(f"Error: {e}")
