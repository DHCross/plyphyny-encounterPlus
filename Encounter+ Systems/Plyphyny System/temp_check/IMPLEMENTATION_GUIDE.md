# Plyphyny Encounter+ System - Implementation Guide

## Phase 1: Foundation (Quick Wins - High Impact)

### 1. NPC Template System ✅ CREATED
**File**: `npc-templates.json`
**Status**: Ready for implementation
**Features**:
- 9 role templates (Warrior, Rogue, Mage, Mystic, Theurgist, Adept, Assassin, Barbarian, Guard)
- Each template includes baseline stats, primary ability, key specialty
- Level progression (1-5) with scaling ADP/PDP/SP
- Quick NPC creation interface via `forms/npc.json`

**Integration Steps**:
1. Update `forms/npc.json` to reference `npc-templates.json` for role selection
2. Add NPC generation utility to system.json scripts
3. Test NPC creation workflow in EncounterPlus Beta 3982

---

### 2. Iconic Items System ✅ CREATED
**File**: `iconic-items.json`
**Status**: Ready for implementation
**Features**:
- 6 sample iconic items across 3 types (Weapon, Magic Focus, Inspirational)
- 5 rarity levels (Common → Legendary)
- Property descriptors and magical effects
- Energy point tracking for magic focuses

**Integration Steps**:
1. Add `forms/iconic-item.json` to system
2. Link iconic items to Character form (party member equipment tab)
3. Link iconic items to NPC form (NPC equipment selector)
4. Update `config.json` to display iconic item properties

**Example Use**:
```json
{
  "name": "Staff of the Archmage",
  "type": "Iconic Magic Focus",
  "rarity": "Legendary",
  "energyPoints": 10,
  "activationCost": 1
}
```

---

### 3. Enhanced Battle Mechanics ⚠️ PARTIALLY COMPLETE
**Files**: `config.json` (updated), needs `battle-mechanics.json`
**Status**: Config updated; mechanics routing needed

**Key Features from Eldritch Integration**:
- **Battle Phase Calculation**: Prowess die determines initiative (d4=1, d6=2, d8=3, etc.)
- **Armor Damage Reduction**: Cascading defense (Shield → ADP → Armor → PDP)
- **Revitalize System**: Three recovery options:
  - Invigorate (1d4 HP + no further action)
  - Deep Recovery (1d6 HP + costs focus)
  - Steady Renewal (1d3 HP + next round available)

**Implementation Roadmap**:
```
1. Create battle-mechanics.json with phase/reach/classification sorting
2. Update adversary/character forms with revitalize button
3. Add battle tracker UI elements to config.json
4. Link to eldritch-gm-tool-sui combat utilities (reference only)
```

---

## Phase 2: Enhancement (Medium Effort - High Value)

### 4. Special Abilities System ✅ CREATED
**File**: `special-abilities.json`
**Status**: Template created; needs integration
**Features**:
- 8 special defense types (Ethereal, Natural Armor, Immunities, etc.)
- Extra attack patterns (Secondary, Follow-up, Area Effect)
- Immunity/Resistance/Vulnerability lists
- Special movement types (Burrow, Fly, Teleport, etc.)

**Integration**:
1. Update `forms/adversary.json` with special abilities selector
2. Add to `views/adversary.json` as collapsible sections
3. Reference `special-abilities.json` for dropdown options

---

### 5. Treasure Generation System ✅ CREATED
**File**: `treasure-tables.json`
**Status**: Ready for implementation
**Features**:
- By-category treasure (Minor, Standard, Exceptional, Legendary)
- Gold ranges and magic item chances
- Pre-built treasure tables (Bandit Hoard, Dragon's Hoard, etc.)
- Rarity gold multipliers

**Usage in Encounters**:
```
Creature Category → Gold Range + Item Chance
Standard Creature → 200-500 gp + 40% magic item
Legendary Creature → 5000-10000 gp + 80% magic item
```

---

### 6. Character Story System
**Status**: Design ready; needs form implementation
**Proposed Fields**:
```json
{
  "heritage": "string (family background)",
  "upbringing": "string (childhood/formative experiences)",
  "motivations": "string (what drives this character)",
  "personalGoals": "string (short-term and long-term goals)",
  "plotHooks": "array (story elements for GM)",
  "relationships": "object (important NPCs and connections)"
}
```

**Implementation**:
1. Add "Story" tab to character form
2. Update `views/character.json` to display story elements
3. Create story templates for quick character creation

---

## Phase 3: Polish (Nice-to-Have - Lower Priority)

### 7. Name Generation System
**Reference**: Eldritch GM Tool has name generation by race
**Implementation Approach**:
1. Create `name-generators.json` with arrays by race
2. Add name selector to character/NPC generation
3. Optional: Integrate with external name generation API

---

### 8. Advanced Combat Tracker
**Features**:
- Initiative tracker with Battle Phase calculation
- Revitalization queue
- Multi-round battle tracking
- Audio cues for turn order

**Implementation**:
1. Reference `battleUtils.ts` from Eldritch for algorithms
2. Create EncounterPlus UI components
3. Add combat state persistence

---

### 9. Advanced Filtering & Search
**Features**:
- Filter NPCs by role/level
- Filter adversaries by threat level
- Search spells by path/effect
- Filter items by rarity/type

---

## File Structure Summary

### Created Files ✅
- `npc-templates.json` - 9 role templates
- `iconic-items.json` - 6 sample iconic items
- `special-abilities.json` - Defense/ability/movement definitions
- `treasure-tables.json` - Treasure generation rules
- `forms/npc.json` - Quick NPC creation form
- `forms/iconic-item.json` - Iconic item form
- `npcs.json` - Empty NPC collection (ready for data)

### Updated Files ✅
- `entities.json` - Added NPC and IconicItem types
- `config.json` - Color-coded defense bars
- `forms/adversary.json` - Combat stats form
- `forms/character.json` - Tabbed character builder
- `spells.json` - All 301 spells now have descriptions

### Need Implementation
- `forms/character.json` - Add Story tab with background fields
- `views/character.json` - Display story elements
- `config.json` - Add revitalize UI elements, reach tracking
- `battle-mechanics.json` - Create for phase/reach calculations

---

## Integration Checklist

### For Each New Feature:
- [ ] Create/update JSON data file
- [ ] Create/update form (`forms/*.json`)
- [ ] Create/update view (`views/*.json`)
- [ ] Update `entities.json` if new entity type
- [ ] Update `config.json` if new UI element
- [ ] Update `collections.json` if new collection
- [ ] Test in EncounterPlus Beta 3982
- [ ] Document in README.md

---

## Quick Reference: Key Mechanics

### Battle Phase Priority (from Eldritch GM Tool)
```
Phase = Prowess Die Value:
- d4 = Phase 1
- d6 = Phase 2
- d8 = Phase 3
- d10 = Phase 4
- d12 = Phase 5

Then sort by: Reach (reach priority) → Classification (type priority)
```

### Armor Cascade (Damage Application Order)
```
Incoming Damage:
1. Shield absorbs damage (if equipped)
2. ADP absorbs remaining damage
3. Armor rolls (armor die type) for additional reduction
4. PDP absorbs remaining damage
5. HP takes any final damage
```

### Revitalize Options
```
- Invigorate: Recover 1d4 HP, continue turn
- Deep Recovery: Recover 1d6 HP, costs focus action
- Steady Renewal: Recover 1d3 HP, available next round
```

---

## Next Steps

1. **Immediate**: Review this guide with team
2. **Day 1**: Test NPC template creation in EncounterPlus
3. **Day 2**: Implement iconic items system
4. **Day 3**: Add special abilities to adversaries
5. **Day 4**: Integrate battle mechanics
6. **Day 5**: Polish and test full workflow

---

## Reference Documentation

- **Eldritch GM Tool Source**: `/Users/dancross/Dev/GitHub/eldritch-gm-tool-sui/src/`
  - Key files: `utils/monsterUtils.ts`, `utils/battleUtils.ts`, `utils/characterBuild.ts`
- **dnd5e Reference**: `/Users/dancross/Library/Mobile Documents/com~apple~CloudDocs/Main Download/dnd5e/`
- **Daggerheart Reference**: Forms and view structure in `/Users/dancross/Dev/GitHub/plyphyny-encounterPlus/Encounter+ Systems/daggerheart beta/`

---

**Last Updated**: Phase 1-2 Implementation Planning
**Status**: Ready for development
**Priority**: High - These enhancements will significantly improve Plyphyny compatibility and usability
