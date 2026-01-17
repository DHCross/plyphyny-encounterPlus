# Phase 2: Battle Mechanics UI Implementation Guide

## Overview

This document guides the implementation of Plyphyny's unique battle mechanics UI - a system fundamentally different from D&D and Daggerheart.

---

## System Differences

### Plyphyny vs D&D 5e

| Feature | D&D 5e | Plyphyny |
|---------|--------|----------|
| **Initiative** | d20 + DEX modifier | Prowess die (no roll) |
| **Turn Order** | Random per combat | Deterministic, reusable |
| **Defense** | Single AC value | 4-layer cascade (Shield→ADP→Armor→PDP→HP) |
| **Recovery** | Hit points only | Multiple SP-driven Revitalize options |
| **Damage** | Direct HP reduction | Threat dice through defensive layers |
| **Resource** | Spell slots | Spirit Points (SP) |
| **Tactical Element** | Surprise, luck | Positioning, reach, classification |

### Plyphyny vs Daggerheart

| Feature | Daggerheart | Plyphyny |
|---------|-------------|---------|
| **Initiative** | Fixed attribute | Prowess die value |
| **Defense** | HP + Stress | ADP + PDP + HP + SP |
| **Phase System** | Mentioned, not UI | Core mechanic with reach/classification |
| **Recovery** | Rest | In-combat Revitalize options |
| **Reach** | Distance tracking | Initiative tie-breaker |
| **Threat** | Attack rolls | Threat dice pools |

---

## Key Implementation Components

### 1. Battle Phase Calculator

**File**: `battle-mechanics.json` (already created)
**UI Location**: Character/Adversary forms, "Combat Actions" tab

**Logic**:
```
Prowess Die → Battle Phase:
- d12 → Phase 1 (acts first)
- d10 → Phase 2
- d8 → Phase 3
- d6 → Phase 4
- d4 → Phase 5 (acts last)
```

**Implementation**:
- Display as read-only field in combat
- Show visual indicator (1→green, 5→red)
- Include "acts in which order" explanation

### 2. Initiative Order Sorting

**Files**: 
- `forms/battle-tracker.json` (new)
- `battle-mechanics.json` (reference)

**Three-Tier Algorithm**:
```
Tier 1: Battle Phase (1→5)
Tier 2: Weapon Reach (Long → Medium → Short → None)
Tier 3: Classification (PA → Legendary → Exceptional → Standard → Minor → NPC)
```

**Display**:
- List all combatants in sorted order
- Color-code by phase
- Show reach and classification
- Display turn number

### 3. Defense Cascade Visualizer

**Files**:
- `config.json` (updated with bars)
- `views/character-combat.json` (new)

**Cascade Order**:
```
1. Shield: Fixed reduction (if equipped)
2. ADP: Primary pool (blue bar #4287f5)
3. Armor: Roll reduction (if equipped)
4. PDP: Secondary pool (orange bar #e67e22)
5. HP: Direct health (red bar #e74c3c)
```

**Display Options**:
- Stacked bars showing each layer
- Flow diagram showing cascade
- Tooltip explaining each layer
- Color-coded for easy recognition

### 4. Threat Dice Roller

**File**: `forms/battle-tracker.json`

**Features**:
- Input field for threat dice notation (e.g., "3d8", "2d6+2")
- Roll button with random result
- Display total threat points
- Auto-apply to next defense layer

**Formula**:
```
Parse: XdY[+Z]
Roll: X times roll(1,Y), sum results, add Z
```

### 5. Revitalize System UI

**File**: `forms/battle-tracker.json` (Revitalize tab)

**Three Options with Clear Buttons**:

**Option 1: Invigorate**
- Label: "Invigorate (Free)"
- Cost: None
- Effect: Roll Prowess die + Reaction Focus
- Gain: That many ADP points
- When: This turn, can use once per turn
- Condition: ADP < Max (implied)

**Option 2: Deep Recovery**
- Label: "Deep Recovery (1 SP)"
- Cost: 1 Spirit Point
- Effect: Guaranteed Prowess die + Reaction Focus
- Gain: That many ADP points
- When: This turn
- Condition: SP >= 1

**Option 3: Steady Renewal**
- Label: "Steady Renewal (Variable)"
- Cost: 0-N Spirit Points
- Effect: 25% max ADP + (10% × SP spent)
- Gain: Gradual recovery over time
- When: Available next turn
- Condition: Available after this turn ends

**UI Pattern**:
```
[Invigorate] [Deep Recovery] [Steady Renewal]
    ↓              ↓               ↓
  (Free)        (1 SP)         (Var SP)
   Immediate    Immediate      Next Turn
   +1d{die}     +{die}         +25%+10%×SP
```

### 6. Combat State Tracker

**File**: `forms/battle-tracker.json` ("Current Turn" tab)

**Tracked Information**:
- Current active combatant name
- Battle phase
- Weapon reach
- Current ADP/Max ADP
- Current PDP/Max PDP
- Current HP/Max HP
- Current SP/Max SP
- Revitalize available (Yes/No)
- Last action taken

---

## Form Structure

### Character Combat Actions Tab

```json
{
  "title": "Combat Actions",
  "sections": [
    {
      "title": "Battle Phase & Initiative",
      "fields": [
        "Weapon Reach (dropdown)",
        "Armor Type (text)",
        "Shield Value (number)",
        "Reaction Focus (number)"
      ]
    },
    {
      "title": "Defense & Recovery",
      "fields": [
        "ADP Maximum",
        "ADP Current",
        "Passive Defense Pool",
        "Hit Points"
      ]
    },
    {
      "title": "Spirit Points & Recovery",
      "fields": [
        "SP Current",
        "SP Maximum",
        "Revitalize Available (checkbox)",
        "Last Revitalize Used (readonly)"
      ]
    }
  ]
}
```

### Adversary Combat Actions Tab

```json
{
  "title": "Combat Actions",
  "sections": [
    {
      "title": "Initiative & Reach",
      "fields": [
        "Prowess Die (d4-d12)",
        "Weapon Reach",
        "Calculated Battle Phase (readonly)",
        "Reaction Focus"
      ]
    },
    {
      "title": "Defense & Recovery",
      "fields": [
        "Armor Type",
        "Shield Value",
        "Can Revitalize (checkbox)",
        "Revitalize Option (preferred)"
      ]
    },
    {
      "title": "Combat State",
      "fields": [
        "Already Revitalized This Turn",
        "Last Action (readonly)",
        "Turns in Combat (readonly)"
      ]
    }
  ]
}
```

---

## Battle Tracker Form Structure

### Tab 1: Initiative Order

**Display**:
- Table of all combatants
- Columns: Phase | Name | Reach | Type | ADP | Turn #
- Sorted by initiative order
- Highlight current combatant
- Color-code by phase

### Tab 2: Current Turn

**Display**:
- Current active combatant name (large)
- Summary of their stats
- Available actions:
  - Roll Threat Dice (button)
  - Revitalize (button, conditional)
  - Defend (button)
  - End Turn (button, primary)

### Tab 3: Threat Calculator

**Input**:
- Threat dice field (e.g., "3d8+2")
- Roll button
- Display total threat

**Cascade Display**:
- Shows defense order
- Applies to selected target

### Tab 4: Revitalize System

**Display**:
- Three revitalize buttons
- Last result message
- SP gain/loss
- ADP gain

---

## Color Coding System

### Battle Phase Colors
```
Phase 1: #2ecc71 (Green) - Legendary/First
Phase 2: #3498db (Blue) - Exceptional
Phase 3: #f39c12 (Orange) - Standard/Neutral
Phase 4: #e67e22 (Dark Orange) - Cautious
Phase 5: #c0392b (Red) - Last/Desperate
```

### Defense Bar Colors
```
Shield: #95a5a6 (Gray)
ADP: #4287f5 (Blue)
Armor: #9b59b6 (Purple)
PDP: #e67e22 (Orange)
HP: #e74c3c (Red)
```

### Status Colors
```
Ready: #2ecc71 (Green)
Vulnerable (ADP depleted): #f39c12 (Orange)
Defeated: #c0392b (Red)
Revitalize Available: #3498db (Blue)
```

---

## Implementation Checklist

### Phase 2A: Core Battle Mechanics (Week 1)
- [ ] Battle phase calculation display
- [ ] Initiative order sorting algorithm
- [ ] Turn order display in battle tracker
- [ ] Reach priority display

### Phase 2B: Defense System (Week 1-2)
- [ ] Update config.json with 4-bar system
- [ ] Display ADP + PDP + SP bars
- [ ] Show vulnerable state (ADP depleted)
- [ ] Create defense cascade visualizer

### Phase 2C: Combat Actions (Week 2)
- [ ] Add Combat Actions tabs to forms
- [ ] Create battle-tracker form
- [ ] Implement threat dice roller
- [ ] Create damage cascade calculator

### Phase 2D: Revitalize System (Week 2-3)
- [ ] Implement three revitalize buttons
- [ ] Calculate SP costs
- [ ] Display ADP gains
- [ ] Track revitalize availability

### Phase 2E: Polish & Documentation (Week 3)
- [ ] Color-coding system
- [ ] Tooltips and help text
- [ ] Combat workflow guide
- [ ] Testing and validation

---

## Files Modified/Created

### New Files
- ✅ `forms/battle-tracker.json` - Combat turn management
- ✅ `views/character-combat.json` - Combat display template
- ✅ `battle-mechanics.json` - Reference data
- `BATTLE_MECHANICS_ANALYSIS.md` - This guide (already created)

### Modified Files
- ✅ `forms/character.json` - Added Combat Actions tab
- ✅ `forms/adversary.json` - Added Combat Actions tab
- ✅ `config.json` - Updated bars for 4-layer system

### Still Needed
- `COMBAT_WORKFLOWS.md` - Common combat scenarios
- `UI_DESIGN_PATTERNS.md` - Design guidelines
- Sample battle screenshots/mockups

---

## Combat Workflow Examples

### Example 1: Simple Turn

```
Encounter Setup:
  Player (d8 Prowess) vs Goblin (d6 Prowess)
  
Initiative:
  Phase 1-3 not used
  Phase 4 (Goblin, d6)
  Phase 5 (Player, d8)

Wait... d8 → Phase 3, d6 → Phase 4:
  Phase 3 (Player) acts BEFORE Phase 4 (Goblin)
  
Turn 1 - Player:
  - Declares: "I attack with my sword"
  - Rolls: 3d8 threat dice
  - Result: 15 threat points
  - Applies to Goblin
  
Turn 2 - Goblin:
  - Declares: "I attack back"
  - Rolls: 2d6 threat dice
  - Result: 9 threat points
  - Applies to Player
  
Turn 3 - Player:
  - ADP taking damage
  - Uses Revitalize: Invigorate
  - Rolls Prowess die (d8) + Reaction Focus (+2) = 7
  - Gains 7 ADP back
```

### Example 2: Reach Tie-breaker

```
Encounter:
  Fighter (d8, Long reach) vs Rogue (d8, Short reach)
  
Both have d8 → Phase 3
Reach breaks tie:
  Fighter (Long) = Priority 1
  Rogue (Short) = Priority 3
  
Result: Fighter acts before Rogue (same phase, but better reach)
```

### Example 3: Classification Tie-breaker

```
Encounter:
  Player (d6) vs Boss (d6, Legendary)
  
Both have d6 → Phase 4
Same phase → Check reach (assume both Medium)
Same reach → Check classification:
  Player (PA) = Priority 1
  Boss (Legendary) = Priority 2
  
Result: Player acts before Boss (PA > Legendary)
```

---

## Success Criteria

### UI Completeness
- [ ] All combat actions accessible in forms
- [ ] Battle tracker shows correct initiative order
- [ ] Defense cascade visualized properly
- [ ] Revitalize system clear and functional

### Mechanic Accuracy
- [ ] Battle phase calculation correct
- [ ] Initiative sorting deterministic
- [ ] Damage cascade applies in correct order
- [ ] Revitalize options work as designed

### User Experience
- [ ] Combat flows smoothly in UI
- [ ] Turn order never ambiguous
- [ ] Actions have clear costs/benefits
- [ ] No confusion with D&D/Daggerheart

---

## Reference Implementation Notes

From the Eldritch GM Tool analysis, we have these patterns to reference:

**Battle Phase Calculation** (confirmed working):
```
d12 → 1, d10 → 2, d8 → 3, d6 → 4, d4 → 5
```

**Sort Algorithm** (confirmed working):
```
1. Sort by phase (ascending)
2. If tied, sort by reach priority (long→short)
3. If tied, sort by classification priority
```

**Revitalize Options** (confirmed working):
```
Invigorate: Roll die + bonus, free, this turn
Deep Recovery: Die + bonus (guaranteed), 1 SP, this turn
Steady Renewal: 25% + 10% per SP, next turn
```

**Damage Application** (confirmed working):
```
Shield → ADP → Armor → PDP → HP (in order)
```

---

## Next Steps After Phase 2

### Phase 3: Advanced Features
- Name generation system (by race)
- Combat history tracking
- Battle statistics and analysis
- Encounter difficulty calculator

### Long-term Enhancements
- Interactive battle map integration
- Audio cues for turn order
- Automated damage calculation
- Campaign-level statistics

---

**Status**: Phase 2 Planning Complete
**Ready for Implementation**: Yes
**Estimated Duration**: 2-3 weeks development
**Priority**: High - Core gameplay mechanics

