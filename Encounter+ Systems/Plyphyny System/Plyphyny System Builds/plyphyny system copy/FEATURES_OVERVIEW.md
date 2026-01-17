# Plyphyny Encounter+ System - Complete Enhancement Package

## Quick Start

The Plyphyny System has been fully enhanced for **EncounterPlus Beta 3982** compatibility with comprehensive GM tools, NPC templates, iconic items, and automated encounter generation.

### What's New

| Feature | File | Status |
|---------|------|--------|
| **NPC Templates** | `npc-templates.json` | ✅ Complete (9 roles) |
| **Iconic Items** | `iconic-items.json` | ✅ Complete (6 items) |
| **Special Abilities** | `special-abilities.json` | ✅ Complete (40+ types) |
| **Treasure Generation** | `treasure-tables.json` | ✅ Complete |
| **NPC Entity Type** | `entities.json` + `forms/npc.json` | ✅ Complete |
| **IconicItem Entity Type** | `entities.json` + `forms/iconic-item.json` | ✅ Complete |

---

## System Architecture

### Entity Types (7 Total)
1. **Character** - Player characters with full ability trees
2. **Adversary** - Encounters with combat mechanics
3. **NPC** - Quick-create non-player characters
4. **Spell** - 301 spells across all Eldritch paths
5. **Item** - General inventory items
6. **IconicItem** - Legendary equipment with special properties
7. **Race** - Character race definitions

### Core Game Mechanics
- **Ability System**: Competence, Prowess, Fortitude with specialties and focuses
- **Defense System**: Active Defense Pool (ADP) + Passive Defense Pool (PDP) + HP
- **Combat**: Threat dice attacks, Battle Phase initiative (d4-d12), Spirit Points
- **Revitalization**: Three recovery options (Invigorate, Deep Recovery, Steady Renewal)

---

## Feature Documentation

### 1. NPC Templates System

**File**: `npc-templates.json`

Generate NPCs instantly using 9 pre-built role templates:

```
Warrior (Prowess)        - Melee fighter
Rogue (Competence)       - Agile specialist
Mage (Competence)        - Spellcaster
Mystic (Fortitude)       - Spiritual guide
Theurgist (Competence)   - Divine magic user
Adept (Competence)       - Scholarly wizard
Assassin (Prowess)       - Lethal agent
Barbarian (Prowess)      - Rage fighter
Guard (Prowess)          - Trained soldier
```

**Each template includes**:
- Primary ability and key specialty
- Baseline ADP, PDP, and Prowess die
- Pre-selected advantages
- Level progression (1-5) with stat scaling

**How to Use**:
1. Create new NPC entity
2. Select Role from `forms/npc.json`
3. Choose Level (1-5)
4. Fill in name, race, gender
5. Stats auto-populate from template

---

### 2. Iconic Items System

**File**: `iconic-items.json`

Six sample legendary items representing three categories:

#### Iconic Weapons (2 items)
- **Iconic Sword**: +1 Threat Focus, common masterwork blade
- **Battle Axe of the Mountain King**: +2 Ferocity Focus, +1 Might Focus, meteorite iron

#### Iconic Magic Focuses (2 items)
- **Staff of the Archmage**: +2 Wizardry Focus, 10 Energy Points, spell amplification
- **Spellbook of Lost Paths**: +3 Wizardry Focus, 15 Energy Points, spell discovery

#### Iconic Inspirational Items (2 items)
- **Family Heirloom Amulet**: +1 General Inspiration (use once per session)
- **Cloak of the Shadow Dancer**: +1 Stealth Focus, shadow affinity

**Rarity System**:
- Common (1x value) - Starting equipment
- Uncommon (2.5x value) - Veteran gear
- Esoteric (5x value) - Rare finds
- Occult (10x value) - Ancient artifacts
- Legendary (25x value) - Campaign defining items

---

### 3. Special Abilities System

**File**: `special-abilities.json`

Comprehensive creature ability definitions covering:

#### Special Defenses (8 types)
- **Ethereal** - Pass through matter, only harmed by magic
- **Natural Armor** - Built-in DR from hide/scales/carapace
- **Immunities** - Magic, element, condition immunities
- **Damage Reduction** - DR 5-20 against physical attacks
- **Spell Resistance** - Bonus against spells
- **Regeneration** - Heal each round (halted by fire/acid)
- **Fast Healing** - Recover HP between encounters
- **Magic Resistance** - Advantage against magical effects

#### Extra Attacks (4 types)
- **Secondary Attack** - Additional weapon or natural attack
- **Follow-up Attack** - Automatic bonus effect on hit
- **Area Effect** - Affects multiple targets (breath, aura)
- **Special Ability** - Unique supernatural ability

#### Immunities & Resistances
- Pre-defined lists: Charm, Fear, Paralysis, Poison, Psychic, Fire, Cold, Lightning
- Customizable per creature

#### Special Movement (7 types)
- Burrow, Climb, Fly, Hover, Swim, Teleport, Ethereal Shift

---

### 4. Treasure Generation System

**File**: `treasure-tables.json`

Automated encounter loot generation by creature category:

```
Creature Type       Gold Range      Item Chance    Item Rarity
─────────────────────────────────────────────────────────────
Minor               50-100 gp       20%           Common
Standard            200-500 gp      40%           Common-Esoteric
Exceptional         500-2000 gp     60%           Uncommon-Occult
Legendary           5000-10000 gp   80%           Esoteric-Legendary
```

**Pre-built Tables** (4 examples):
1. **Bandit Hoard**: 2d100 gold, gems, minor magic item
2. **Guard's Equipment**: Coin, weapon, armor, supplies
3. **Mage's Spellbook**: Gold, scrolls, potions, esoteric item
4. **Dragon's Hoard**: Massive gold, gems, jewelry, legendary items

---

## File Reference

### Configuration Files
- `manifest.json` - System metadata (v1.0.3, build 5.0.0+3848)
- `system.json` - System description and version
- `config.json` - Combat UI colors, defense bar setup
- `entities.json` - Entity type registry (7 types)
- `collections.json` - Collection organization
- `types.json` - Type definitions
- `filters.json` - Search/filter configuration

### Data Files
- `characters.json` - Player character templates
- `adversaries.json` - 39 encounter creatures
- `npcs.json` - NPC collection (empty, ready for data)
- `spells.json` - 301 spells (all with descriptions)
- `items.json` - Standard items
- `races.json` - Character races
- `npc-templates.json` - 9 NPC role templates ⭐ NEW
- `iconic-items.json` - 6 legendary items ⭐ NEW
- `special-abilities.json` - Creature ability definitions ⭐ NEW
- `treasure-tables.json` - Loot generation rules ⭐ NEW

### UI Forms (`forms/` directory)
- `character.json` - Character creation (3 tabs)
- `adversary.json` - Encounter creation (3 tabs)
- `npc.json` - Quick NPC creation (3 tabs) ⭐ NEW
- `iconic-item.json` - Iconic item management (3 tabs) ⭐ NEW
- `spell.json` - Spell form
- `item.json` - Item form
- `race.json` - Race form

### Display Templates (`views/` directory)
- `character.json` - Character sheet layout
- `adversary.json` - Encounter stat block
- `npc.json` - NPC card layout ⭐ NEW
- `iconic-item.json` - Item details display ⭐ NEW
- `spell.json` - Spell card layout
- `item.json` - Item card layout

### Localization
- `lang/en.json` - English labels and descriptions

### Themes
- `themes/default.json` - Default UI theme

### Documentation ⭐ NEW
- `IMPLEMENTATION_GUIDE.md` - Phase-by-phase implementation roadmap
- `ENHANCEMENT_SUMMARY.md` - Complete feature overview
- `ENHANCEMENT_ANALYSIS.md` - Original 12-category enhancement analysis

---

## Integration Examples

### Creating an NPC from Template

```json
{
  "name": "Captain Redmond",
  "type": "NPC",
  "race": "Human",
  "gender": "Male",
  "role": "Warrior",
  "level": 3,
  "data": {
    "adp": 20,
    "pdp": 10,
    "hp": 30,
    "spiritPoints": 7,
    "prowessDie": 8,
    "advantages": ["Commanding", "Intimidation", "Magic Resistance (+1)", "Tactician"]
  }
}
```

### Equipping an Iconic Item

```json
{
  "name": "Battle Axe of the Mountain King",
  "type": "IconicItem",
  "rarity": "Esoteric",
  "data": {
    "properties": "+2 Ferocity Focus, +1 Might Focus",
    "damage": "2d6 + Focus bonuses"
  }
}
```

### Creature with Special Abilities

```json
{
  "name": "Shadow Wraith",
  "category": "Exceptional",
  "threatDice": "3d8",
  "data": {
    "specialDefenses": ["Ethereal", "Regeneration"],
    "extraAttacks": ["Drain Life (Special Ability)"],
    "immunities": ["Charm", "Sleep"],
    "vulnerabilities": ["Holy weapon"],
    "specialMovement": ["Ethereal Shift"]
  }
}
```

---

## EncounterPlus Beta 3982 Compatibility

### ✅ Verified Working
- System loads in Beta 3982
- Character creation interface
- Adversary/encounter builder
- Spell reference library
- Item management

### ✅ Tested Features
- 301 spells with descriptions
- 39 pre-built encounters
- Character ability trees
- Combat statistics display
- Defense pool visualization

### ✅ Ready for Testing
- NPC quick creation
- Iconic item equipment
- Special ability effects
- Automated treasure loot

---

## Performance Statistics

- **Total Entities**: 7 types
- **NPC Templates**: 9 roles with progression
- **Iconic Items**: 6 items + framework for unlimited
- **Special Abilities**: 40+ ability types
- **Spells**: 301 (all with descriptions)
- **Encounters**: 39 pre-built adversaries
- **Treasure Tables**: 4 pre-built + custom framework

---

## Development Roadmap

### Phase 1: COMPLETE ✅
- NPC Templates system
- Iconic Items system
- Special Abilities definitions
- Treasure Generation system

### Phase 2: PLANNED
- Character story/background system
- Advanced battle mechanics UI
- Battle phase sorting and reach tracking
- Revitalization UI components

### Phase 3: PLANNED
- Name generation system (by race)
- Advanced combat tracker
- Search/filter enhancements
- Campaign management tools

---

## Quick Reference: Core Mechanics

### Battle Phase Priority
```
Phase = Prowess Die Value:
- d4 = Phase 1 (Invigorate on turn 1)
- d6 = Phase 2
- d8 = Phase 3
- d10 = Phase 4
- d12 = Phase 5 (Last to act)

Then sort by: Reach Priority → Classification
```

### Damage Application Cascade
```
1. Shield (if equipped) absorbs damage
2. Active Defense Pool (ADP) absorbs remainder
3. Armor (if equipped) rolls damage reduction
4. Passive Defense Pool (PDP) absorbs remainder
5. Health Points (HP) takes final damage
```

### Revitalize Options
```
- Invigorate: Recover 1d4 HP, continue turn (free)
- Deep Recovery: Recover 1d6 HP, costs focus action (powerful, limited)
- Steady Renewal: Recover 1d3 HP, available next round (weak, flexible)
```

---

## Files by Priority

### Must Have (Core System)
- ✅ `manifest.json` - System identification
- ✅ `system.json` - System details
- ✅ `config.json` - Combat setup
- ✅ `entities.json` - Entity types
- ✅ `spells.json` - Spell library
- ✅ `adversaries.json` - Encounters

### Should Have (Full System)
- ✅ `npc-templates.json` - NPC creation
- ✅ `iconic-items.json` - Equipment items
- ✅ `special-abilities.json` - Creature abilities
- ✅ `treasure-tables.json` - Loot system

### Nice to Have (Enhancement)
- ✅ `IMPLEMENTATION_GUIDE.md` - Implementation roadmap
- ✅ `ENHANCEMENT_SUMMARY.md` - Feature overview
- ✅ `ENHANCEMENT_ANALYSIS.md` - Original analysis

---

## Support & Documentation

For detailed implementation instructions, see:
- **Implementation Guide**: `IMPLEMENTATION_GUIDE.md`
- **Enhancement Summary**: `ENHANCEMENT_SUMMARY.md`
- **Original Analysis**: `ENHANCEMENT_ANALYSIS.md`

For reference architecture, see:
- **Eldritch GM Tool**: `/Users/dancross/Dev/GitHub/eldritch-gm-tool-sui/`
- **dnd5e Reference**: `/Users/dancross/Library/Mobile Documents/com~apple~CloudDocs/Main Download/dnd5e/`

---

**System Version**: 1.0.3
**Build**: 5.0.0+3848
**EncounterPlus Beta**: 3982
**Last Updated**: Implementation Phase 1 Complete
**Status**: Ready for use and Phase 2 enhancement

