# Plyphyny Phase Combat Logic

Based on **Eldritch Rules 8.17.2025**.

## 1. The Core Structure
*   **Round Duration**: 10 seconds.
*   **Phases**: 5 phases (2 seconds each).
*   **Countdown Order**: Phase 1 (Fastest) → Phase 5 (Slowest).
*   **Phase 0 (New)**: Reserved for "Follow-Through" actions or specific Legendary speeds.

## 2. Determining the Phase (Sorting Algorithm)

**Formula**:
`Initiative Score = Prowess MV + Agility Focus (Reaction) + Melee Focus (Finesse)`

**Phase Table**:
| Total Score | Phase | Speed Rank |
| :--- | :--- | :--- |
| **12+** | **Phase 1** | Legendary/Master |
| **9–11** | **Phase 2** | Heroic |
| **7–8** | **Phase 3** | Competent |
| **5–6** | **Phase 4** | Average |
| **1–4** | **Phase 5** | Untrained/Slow |

## 3. Intra-Phase Sorting (Tie-Breaking)

When multiple combatants share a phase, sort by:

**Priority 1: Attack Precedence (Range/Reach)**
(Longer reach acts earlier)
1.  **Long Range** (Bows, Spells)
2.  **Long Reach** (Polearms, Whips)
3.  **Medium Reach** (Swords, Axes)
4.  **Short Reach** (Daggers, Unarmed)

**Priority 2: Heroic Action Order**
(Narrative importance tie-breaker)
1.  **PCs & Legendary NPCs**
2.  **Exceptional Enemies**
3.  **Standard Enemies**
4.  **Minor Enemies**

**Priority 3: Random Initiative (The Fallback)**
Roll: `d20? + Prowess + Agility + Reaction` (Exact roll mechanics to be confirmed, usually high roll wins).

## 4. Tactical Movement & "Follow-Through"

**The "Follow-Through" Mechanic**:
*   **Trigger**: Performed a **Run** action (2x speed) during **Phase 5** of the previous round.
*   **Effect**: Act immediately at the start of the next round (effectively **Phase 0**).
*   **Cost**: **-3 Threat Points** on any attack made during this follow-through action.
*   **Reset**: Flag clears after the action is taken.

## 5. Data Structure Implementation

**Combatant Object Extensions**:
```json
{
  "data": {
    "prowessMV": 12,                  // Source of Prowess Die value
    "reactionFocus": 2,               // Agility Focus
    "finesseFocus": 0,                // Melee Focus
    "weaponReach": "Long Range",      // Enum: Long Range, Long Reach, Medium Reach, Short Reach
    "followThroughActive": false,     // Boolean flag
    "classification": "Heroic"        // Enum corresponding to tier
  }
}
```

**Sorting Logic Pseudo-code**:
```javascript
function sortCombatants(combatants) {
    return combatants.sort((a, b) => {
        // 1. Follow-Through (Active acts before Inactive)
        if (a.followThroughActive !== b.followThroughActive) {
            return a.followThroughActive ? -1 : 1;
        }

        // Calculate Scores
        const scoreA = a.prowessMV + a.reactionFocus + a.finesseFocus;
        const scoreB = b.prowessMV + b.reactionFocus + b.finesseFocus;
        
        // Calculate Phases (Higher Score = Lower Phase Number = Acts Earlier)
        const phaseA = calculatePhase(scoreA);
        const phaseB = calculatePhase(scoreB);

        // 2. Battle Phase (Ascending: 1 -> 5)
        if (phaseA !== phaseB) {
            return phaseA - phaseB;
        }

        // 3. Weapon Reach Priority (Ascending: 1 -> 4)
        // Map: Long Range=1, Long Reach=2, Medium=3, Short=4
        const reachA = getReachPriority(a.weaponReach);
        const reachB = getReachPriority(b.weaponReach);
        if (reachA !== reachB) {
            return reachA - reachB;
        }

        // 4. Heroic Tier (Ascending: 1 -> 4)
        // Map: PC/Legendary=1, Exceptional=2, Standard=3, Minor=4
        const tierA = getHeroicTier(a.classification);
        const tierB = getHeroicTier(b.classification);
        if (tierA !== tierB) {
            return tierA - tierB;
        }

        // 5. Fallback Roll
        return b.initiativeRoll - a.initiativeRoll;
    });
}
```
