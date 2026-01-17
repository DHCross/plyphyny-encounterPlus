# Battle Mechanics Comparison & Plyphyny Enhancement Plan

## System Comparison

### D&D 5e Battle Mechanics
**Initiative**: Roll 1d20 + DEX modifier
- All creatures roll same die, fastest acts first
- Simple, standardized approach
- Speed attribute tracked separately from combat

**Defense**: Armor Class (AC)
- Single defense value (10-20 typically)
- Hit/Miss binary outcome
- Damage directly reduces HP

**Status Effects**: Conditions
- Restrained, Stunned, Charmed, Petrified, etc.
- 13 standard conditions
- Tracked in status effect system

**Combat Resolution**:
- Attack roll vs. AC
- Damage roll (varies by weapon)
- Marked HP directly (hit points go down)

---

### Daggerheart Battle Mechanics
**Initiative**: Fixed mode
- Initiative attribute determines order
- Appears to use encounter/tier system
- Less emphasis on die rolls, more on preparation

**Defense**: Hit Points + Stress
- Dual tracking system
- Stress similar to Plyphyny's Spirit Points
- Hit Points marked, separate from stress

**Special Mechanics**:
- Phase system mentioned but not implemented in UI
- Domain Cards affect combat
- Environmental entities tracked
- Tier system for adversaries (Minor, Standard, Exceptional)

**Status Effects**: Conditions system
- Restrained, Vulnerable mentioned in adversary abilities
- Integrated with reaction rolls

---

### Plyphyny Battle Mechanics (Current)
**Initiative**: Battle Phase system
- Based on Prowess die (d4-d12)
- d12 = Phase 1 (acts first), d4 = Phase 5 (acts last)
- Reflects character competence with weapons
- **VERY DIFFERENT** from D&D/Daggerheart

**Defense**: Ablative Defense System
- **Active Defense Pool (ADP)**: First layer of protection
- **Passive Defense Pool (PDP)**: Second layer after ADP depleted
- **Hit Points (HP)**: Final health pool
- **Spirit Points (SP)**: Resource for special actions

**Damage Application Cascade**:
```
Incoming Threat Dice:
1. Shield (if equipped) absorbs threat
2. ADP absorbs remaining threat
3. Armor (if equipped) rolls damage reduction (d4-d20)
4. PDP absorbs remaining threat
5. HP takes final damage
```

**Special Mechanics**:
- Threat Dice (2d6, 3d8, 3d10, etc.) instead of individual die rolls
- Revitalize system (3 options: Invigorate, Deep Recovery, Steady Renewal)
- Weapon Reach priority in combat order
- Classification priority (Player > NPC > Legendary > Exceptional > Standard > Minor)

---

## Key Differences from Reference Systems

| Aspect | D&D | Daggerheart | Plyphyny |
|--------|-----|-------------|---------|
| **Initiative** | d20 + DEX | Fixed attribute | Prowess die (d4-d12) |
| **Phase System** | No | Mentioned | YES - Core mechanic |
| **Defense Layers** | 1 (AC) | 2 (HP + Stress) | 3 (ADP + PDP + HP) |
| **Attack Type** | Single die roll | Implied | Threat Dice pools |
| **Recovery** | HP healing | Implied | 3 revitalize options |
| **Resources** | Spell slots, actions | Stress marks | Spirit Points + ADP/PDP |
| **Reach System** | Distance tracking | Mentioned | Initiative tie-breaker |

---

## Plyphyny Battle Phase System (Needs UI Implementation)

### Battle Phase Calculation
```
Prowess Die → Battle Phase:
- d12 → Phase 1 (acts first)
- d10 → Phase 2
- d8 → Phase 3
- d6 → Phase 4
- d4 → Phase 5 (acts last)
```

### Initiative Order Algorithm
```
1. Sort by Battle Phase (ascending: 1→5)
2. If tied, sort by Weapon Reach (long → medium → short → none)
3. If tied, sort by Classification (PA → NPC → Legendary → Exceptional → Standard → Minor)
4. Results in stable, predictable turn order
```

### Weapon Reach Priority
```
Long Reach:   Acts before medium/short (ranged superiority)
Medium Reach: Acts before short (balanced)
Short Reach:  Acts last (melee disadvantage in init)
None:         No reach-based adjustment
```

### Classification Priority
```
Highest: Player Adventurer (players always high priority)
         Legendary (boss creatures)
         Exceptional (tough encounters)
         Standard (normal foes)
         Minor (weak opponents)
Lowest:  NPCs (neutral parties)
```

---

## Revitalize System (Unique to Plyphyny)

### Option 1: Invigorate (No Cost)
- Roll Prowess die + Reaction Focus bonus
- Gain ADP equal to roll
- Action: Can continue this turn
- Best for: Mid-round recovery, maintaining position

### Option 2: Deep Recovery (1 Spirit Point)
- Gain Prowess die + Reaction Focus bonus to ADP
- Guaranteed maximum recovery per SP
- Action: Uses focus action (limits other actions)
- Best for: Critical recovery when needed

### Option 3: Steady Renewal (Variable SP Cost)
- Gain 25% of max ADP (base)
- +10% of max ADP per Spirit Point spent
- Action: Available next round (not immediate)
- Best for: Long-term sustainability, resource management

---

## Armor & Defense Mechanics

### Defense Cascade (Threat Application Order)
```
1. Shield: Fixed damage reduction (if equipped)
2. ADP: Direct threat absorption (pool system)
3. Armor: Roll armor die (d4 to d20 based on type)
4. PDP: Secondary protection pool
5. HP: Direct health reduction
```

### Armor Die Examples
- Light (Leather): d4
- Medium (Chain Mail): d6-d8
- Heavy (Plate): d10-d12
- Natural Armor: +X to max HP (no roll)

---

## Proposed UI Enhancements for Phase 2

### 1. Battle Tracker Form
**New form: `forms/battle-tracker.json`**
- Initiative order calculation display
- Visual phase indicator
- Reach priority display
- Classification priority markers

### 2. Combat Actions UI
**Enhance `forms/adversary.json` and `forms/character.json`**
- Add "Combat Actions" tab
- Revitalize button with 3 options
- Threat dice roll interface
- Armor roll calculator

### 3. Initiative Optimizer
**New form: `forms/initiative-order.json`**
- Display sorted combatant list
- Phase → Reach → Classification sorting
- Color-coded by phase number
- Quick reference for turn order

### 4. Defense Pool Tracker
**Enhance `config.json` combatant display**
- Add shield indicator
- Show armor type/die
- Display SP current/max
- Visual cascade of damage (shield → ADP → armor → PDP → HP)

### 5. Revitalize Manager
**New form: `forms/revitalize-options.json`**
- Three buttons: Invigorate, Deep Recovery, Steady Renewal
- SP cost indicator
- ADP gain calculator
- Turn availability tracker

---

## Implementation Priority

### High Priority (Phase 2 Start)
1. Battle Phase calculation in config.json
2. Initiative order sorting algorithm
3. Revitalize UI component
4. Threat dice roller

### Medium Priority (Phase 2 Mid)
5. Reach priority display
6. Classification priority sorting
7. Armor cascade visualizer
8. Combat action tracker

### Lower Priority (Phase 2 End)
9. Advanced battle analysis
10. Multi-round battle history
11. Combat statistics
12. Encounter difficulty calculator

---

## Comparison to Eldritch GM Tool

The Eldritch GM Tool (from your other repo) implements most of these mechanics in TypeScript:

**What We Can Reference**:
- `calculateBattlePhase()` - Phase calculation algorithm ✅ (already in analysis)
- `sortCombatants()` - Initiative sorting ✅ (already have this)
- `reachPriority()` - Reach-based sorting ✅ (already have this)
- `applyThreat()` - Damage cascade ✅ (already have this)
- `performRevitalize()` - Revitalize system ✅ (already have this)
- `rollArmorDice()` - Armor rolling ✅ (already have this)

**Implementation Pattern**:
Use TypeScript implementations as reference for:
- Function logic verification
- Edge case handling
- State management patterns
- Error checking

---

## Critical Insights

### Why Plyphyny's System is Different
1. **Battle Phase Prowess Die**: Reflects character capability (not just luck)
   - Strong warriors (d12) act before weak soldiers (d4)
   - Creates tactical positioning importance
   
2. **Ablative Defense**: Multiple layers of protection
   - ADP acts as "armor pool" that refreshes (via Revitalize)
   - PDP as "backup defense" harder to recover
   - HP as "real damage" permanent until rest
   
3. **Revitalize Options**: In-combat recovery system
   - Differentiates from "heal when not in combat"
   - Creates tactical decisions about resource spending
   - Allows dramatic comebacks (Deep Recovery)

### Why It Matters for UI
- UI must show Battle Phase clearly (not initiative roll)
- Must display 3-layer defense, not single AC
- Must show SP resource as tactical option
- Must explain Revitalize choices with clear outcomes

---

## Design Recommendations

### UI Philosophy for Plyphyny
```
D&D: Simple + Fast
"Roll d20, get a number, that's initiative"

Daggerheart: Elegant + Prepared
"Initiative set, no rolls, smooth flow"

Plyphyny: Strategic + Tactical
"Your prowess determines when you act
Your defenses layer in meaningful ways
Your spirit fuels both recovery and special abilities"
```

### Visual Hierarchy
1. **Battle Phase** (Most Important)
   - Large, clear display
   - Color-coded by phase (1=green, 5=red)
   
2. **Defense Pool Status** (Very Important)
   - Shield → ADP → Armor → PDP → HP cascade
   - Stacked or layered visual
   
3. **Revitalize Options** (Important in combat)
   - Three distinct buttons
   - Cost and benefit clearly labeled
   
4. **Threat Dice** (Important for damage)
   - Show as pool notation (2d6, 3d8, etc.)
   - Total damage range display

---

## Files to Create/Enhance

### New Files (Phase 2)
- `forms/battle-tracker.json` - Initiative management
- `forms/revitalize-options.json` - Recovery system UI
- `forms/initiative-order.json` - Combat order display
- `utils/battle-mechanics.json` - Calculation reference

### Enhanced Files (Phase 2)
- `config.json` - Add battle phase colors, revitalize UI elements
- `forms/adversary.json` - Add Combat Actions tab
- `forms/character.json` - Add Combat Actions tab
- `views/adversary.json` - Add initiative/phase display
- `views/character.json` - Add initiative/phase display

### Documentation (Phase 2)
- `BATTLE_MECHANICS.md` - System explanation
- `UI_DESIGN.md` - UI implementation guide
- `COMBAT_WORKFLOWS.md` - Common combat scenarios

---

**Next Step**: Build Phase 2 with full battle mechanics UI implementation
