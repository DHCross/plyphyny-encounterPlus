# Codemap for Plyphyny System Battle Mechanics Implementation

## 1. Goal
Implement missing logic and automation for the Plyphyny System in Encounter+ Beta, specifically focusing on Battle Phases, Defense Cascade, and Handlebars helpers.

## 2. Identified Gaps
- **Missing Scripts**: `assets/js/custom.js` (or similar) is missing.
- **Missing Helpers**: `calculatePhase`, `calculatePhasePosition` referenced in `character-combat.json` are undefined.
- **Combat Logic**: The mathematical logic for Battle Phases (Prowess Die -> Phase Number) is specified in docs but not code.

## 3. Reference Architecture (Based on dnd5e)
- `manifest.json` or `system.json` should likely reference the script, or it might be auto-loaded from `assets/js/custom.js` depending on convention. *Investigation required on how dnd5e loads it.*

## 4. Implementation Plan

### Step 4.1: Script Setup
- Create `assets/js/plyphyny.js` (or `custom.js`).
- Ensure it is loaded by the system.

### Step 4.2: Handlebars Helper Implementation
Implement the following helpers in JavaScript:
- `calculatePhase(prowessDie)`: Returns phase number 1-5 based on die size.
- `calculatePhasePosition(prowessDie)`: Returns "Fast", "Normal", "Slow" etc. description.
- *(Potential)* `calculateDefense(shield, adp, armor, pdp)`: If calculation is needed.

### Step 4.3: View Integration
- Verify `character-combat.json` correctly calls these helpers.
- Verify data binding (`data.prowessDie`, `data.ad_current`, etc.) matches the logic.

## 5. Logic Specs (from PHASE_2_BATTLE_MECHANICS.md)
- **Battle Phase**:
    - d12 -> Phase 1
    - d10 -> Phase 2
    - d8 -> Phase 3
    - d6 -> Phase 4
    - d4 -> Phase 5
