import re
import json

input_file = "/Users/dancross/Documents/GitHub/eldritch-gm-tool-sui/src/components/Bestiary.tsx"
output_json = "/Users/dancross/Documents/GitHub/Encounter+ Systems/Plyphyny System/plyphyny_It2X/monsters.json"

monsters = []

def parse_hp(hp_str):
    # Format: "18 (9/9)" or just "18"
    if not hp_str:
        return 0, 0
    
    # Try match "X (A/P)"
    match = re.search(r'(\d+)\s*\((\d+)/(\d+)\)', hp_str)
    if match:
        total = int(match.group(1))
        active = int(match.group(2))
        passive = int(match.group(3))
        return active, passive
    
    # Else just total, split 50/50
    try:
        val = int(re.search(r'\d+', hp_str).group(0))
        return val // 2, val - (val // 2)
    except:
        return 0, 0

def clean_val(val):
    if val:
        return val.strip("'").strip('"')
    return ""

def parse_threat_dice(td_str):
    # td_str is like "{ melee: '2d6', ranged: '2d4' }"
    result = {}
    for key in ['melee', 'natural', 'ranged', 'arcane']:
        match = re.search(key + r":\s*['\"]([^'\"]+)['\"]", td_str)
        if match:
            result[key] = match.group(1)
        else:
            result[key] = ""
    return result

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the creatures array content
start_marker = "const BESTIARY_CREATURES: BestiaryCreature[] = ["
start_idx = content.find(start_marker)

if start_idx == -1:
    print("Could not find BESTIARY_CREATURES array")
    exit(1)

# We want everything inside the [ ] of the array
array_end_idx = content.find("];", start_idx)
array_content = content[start_idx:array_end_idx]

# Pattern matching the whole object from "  {" up to "  },"
object_pattern = re.compile(r"(  \{\n\s+id:.*?\n  \}),?", re.DOTALL)
matches = object_pattern.findall(array_content)

print(f"Found {len(matches)} potential objects")

for block in matches:
    # Name
    name_m = re.search(r"name:\s*['\"]([^'\"]+)['\"]", block)
    if not name_m: continue
    name = name_m.group(1)

    # Category
    cat_m = re.search(r"category:\s*['\"]([^'\"]+)['\"]", block)
    category = cat_m.group(1) if cat_m else ""

    # HP
    hp_m = re.search(r"hp:\s*['\"]([^'\"]+)['\"]", block)
    hp_str = hp_m.group(1) if hp_m else ""
    hpActive, hpPassive = parse_hp(hp_str)

    # DR
    dr_m = re.search(r"dr:\s*['\"]([^'\"]+)['\"]", block)
    dr = dr_m.group(1) if dr_m else ""

    # Saving Throw
    st_m = re.search(r"savingThrow:\s*['\"]([^'\"]+)['\"]", block)
    st = st_m.group(1) if st_m else ""

    # Battle Phase
    bp_m = re.search(r"battlePhase:\s*['\"]([^'\"]+)['\"]", block)
    bp = bp_m.group(1) if bp_m else ""

    # Description
    desc_m = re.search(r"description:\s*['\"]([^'\"]+)['\"]", block)
    desc = desc_m.group(1) if desc_m else ""

    # Extra Attacks
    ea_m = re.search(r"extraAttacks:\s*['\"]([^'\"]+)['\"]", block)
    ea = ea_m.group(1) if ea_m else ""

    # Special Abilities (Array)
    sa_m = re.search(r"specialAbilities:\s*\[(.*?)\]", block, re.DOTALL)
    features_text = ""
    if sa_m:
        abilities = re.findall(r"['\"]([^'\"]+)['\"]", sa_m.group(1))
        features_text = "; ".join(abilities)

    # Threat Dice (Object)
    td_m = re.search(r"threatDice:\s*\{(.*?)\}", block, re.DOTALL)
    td = {'melee': '', 'natural': '', 'ranged': '', 'arcane': ''}
    if td_m:
        td = parse_threat_dice(td_m.group(1))

    # Construct Monster
    monster = {
        "name": name,
        "hp": hpPassive,
        "hpMax": hpPassive,
        "data": {
            "Opponent_type": category,
            "hpActive": hpActive,
            "hpPassive": hpPassive,
            "hp": hpActive + hpPassive, # Calculated total for view
            "dr_static": dr,
            "savingthrow": st,
            "battlephase": bp,
            "subtitle": desc,
            "ea": ea,
            "features_text": features_text,
            "threatdicemelee": td['melee'],
            "threatdicenatural": td['natural'],
            "threatdiceranged": td['ranged'],
            "threatdicearcane": td['arcane'],
            "behavior": "", 
            "notes": "Source: SUI Bestiary"
        }
    }
    monsters.append(monster)

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(monsters, f, indent=2)

print(f"Successfully converted {len(monsters)} monsters to {output_json}")
