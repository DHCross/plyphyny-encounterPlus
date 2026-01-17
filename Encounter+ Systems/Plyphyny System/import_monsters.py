import csv
import json
import re

input_csv = "/Users/dancross/Documents/GitHub/eldritch-gm-tool-sui/Monster List/eldritch_bestiary.csv"
output_json = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/plyphyny_It2X/monsters.json"

monsters = []

def clean_int(val):
    if not val:
        return 0
    try:
        return int(float(val))
    except:
        return 0

try:
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter: Must have Name and (HP or Active Def)
            name = row.get('Name', '').strip()
            hp = row.get('Hit Points (Total)', '').strip()
            ad = row.get('Active Defense', '').strip()

            if not name or (not hp and not ad):
                continue

            monster = {
                "name": name,
                "data": {
                    "Opponent_type": row.get('Category', ''),
                    "threatdicemelee": row.get('Threat Dice (Melee)', ''),
                    "threatdicenatural": row.get('Threat Dice (Natural)', ''),
                    "threatdiceranged": row.get('Threat Dice (Ranged)', ''),
                    "threatdicearcane": row.get('Threat Dice (Arcane)', ''),
                    "ea": row.get('Extra Attacks', ''),
                    "hpActive": clean_int(row.get('Active Defense')),
                    "hpPassive": clean_int(row.get('Passive Defense')),
                    "dr_static": row.get('Damage Reduction', ''),
                    "savingthrow": row.get('Saving Throw', ''),
                    "battlephase": row.get('Battle Phase', ''),
                    "movement": row.get('Movement Rate', ''),
                    "reach": row.get('Reach', ''),
                    "behavior": row.get('Behavior', ''),
                    "features_text": row.get('Special Abilities', ''),
                    "notes": row.get('Notes', '') + " Source Page: " + row.get('Source Page', '')
                }
            }
            monsters.append(monster)

    with open(output_json, mode='w', encoding='utf-8') as jsonfile:
        json.dump(monsters, jsonfile, indent=2)
    
    print(f"Successfully converted {len(monsters)} monsters to {output_json}")

except Exception as e:
    print(f"Error: {e}")
