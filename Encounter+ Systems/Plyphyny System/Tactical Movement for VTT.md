Based on the **Tactical Combat Eldritch 2025** supplement and the **Player Reference** sheets, Prowess rank does not convert directly into movement squares with a simple lookup. Movement is calculated using a formula that combines Prowess, Agility, and a strict rounding rule.

Here is the full logic for converting Prowess into tactical movement squares, where 1 square equals 5 feet.

### 1. Base Movement Formula

To calculate **Base Movement per Phase (Walk)**, use:

[
\text{Squares} = \frac{12 + \text{Prowess MV} + \text{Agility MV}}{5}
]

* **12** is a constant applied to all characters.
* **Prowess MV** is the maximum value of the Prowess die (d4 = 4, d8 = 8, d12 = 12).
* **Agility MV** is the maximum value of the Agility *Specialty* die. If the character does not have the Agility specialty, this value is 0 (or 4 if you allow the default untrained d4, though the rounding rule below penalizes untrained characters).

### 2. Rounding Rule (Critical)

The result of the formula is almost never a whole number. Rounding depends entirely on whether the character has the **Agility Specialty**.

* **Has Agility Specialty:** round **up** to the nearest whole number.
* **No Agility Specialty:** round **down** to the nearest whole number.

### 3. Speed Focus Modifier

After calculating and rounding Base Movement, apply the **Speed Focus** bonus if the character has it. This bonus is added directly to the final square value.

* **Speed Focus d4–d6:** +1 square per phase
* **Speed Focus d8–d10:** +2 squares per phase
* **Speed Focus d12+:** +3 squares per phase

### 4. Calculated Examples

The table below shows how Prowess and Agility combine to produce final Walk speed in squares, assuming the character has the Agility Specialty (rounding up).

| Prowess Rank | Agility Rank | Math                     | Result    |
| ------------ | ------------ | ------------------------ | --------- |
| d4 (4)       | d4 (4)       | (12 + 4 + 4) ÷ 5 = 4.0   | 4 squares |
| d6 (6)       | d6 (6)       | (12 + 6 + 6) ÷ 5 = 4.8   | 5 squares |
| d8 (8)       | d8 (8)       | (12 + 8 + 8) ÷ 5 = 5.6   | 6 squares |
| d10 (10)     | d8 (8)       | (12 + 10 + 8) ÷ 5 = 6.0  | 6 squares |
| d12 (12)     | d12 (12)     | (12 + 12 + 12) ÷ 5 = 7.2 | 8 squares |

If a character has **Prowess d6** but **no Agility Specialty**, the calculation becomes:

[
(12 + 6) ÷ 5 = 3.6
]

Rounded **down**, the final movement is **3 squares**.

### 5. Movement Multipliers

Once Base Movement (Walk) is known, other movement modes are simple multipliers.

* **Run:** Base × 2 (attacks suffer a −3 Threat Point penalty)
* **Sprint:** Base × 4 (no other actions allowed)

### Developer Note (VS Code Module)

When implementing this logic, the `calculateMovement()` function must check whether the Agility specialty exists in order to apply `Math.ceil()` versus `Math.floor()` correctly.

For NPCs or monsters using Quick Stat Blocks, substitute **Battle Phase (BP) Die MV** in place of **Prowess MV**. The formula and rounding rules remain unchanged.
Based on the **Eldritch RPG Tactical Combat (2025)** and **Creature Movement** rules, creature movement on the grid is fully deterministic and derived primarily from the creature’s **Battle Phase (BP) Die**. This approach enforces strict parity between player characters and monsters.

For the Encounter+ module, movement must be calculated as **Squares Per Phase**, where 1 square equals 5 feet, using the algorithm below.

---

### 1. Core Movement Formula

The 2025 system uses a unified parity formula rather than arbitrary movement values.

[
\text{Base Squares} = \frac{12 + \text{BP Die MV} + [\text{Agility MV}]}{5}
]

* **12** is a universal constant applied to all creatures.
* **BP Die MV** is the maximum value of the creature’s Battle Phase die (for example, a d8 contributes 8).
* **Agility MV** is normally **0** for Quick Stat Block creatures and is only added if the creature explicitly lists an Agility specialty.

**Rounding rules:**

* **Standard:** round to the nearest whole number.
* **Exception:** if the creature explicitly has the **Agility Specialty**, always round **up**.

---

### 2. “Fast Layer” Modifiers (Added After Base)

After calculating Base Squares, apply the following flat bonuses in order.

#### A. Derived Movement Bonus (Automatic)

The BP die size grants an inherent speed bonus, sometimes referred to in UI terms as a “Celerity Tier.”

* **BP d4–d6:** +1 square per phase
* **BP d8–d10:** +2 squares per phase
* **BP d12+:** +3 squares per phase

#### B. Trait Bonuses (Conditional)

Check creature traits for these keywords:

* **Fast:** +1 square per phase (stacks with the derived bonus).
* **Especially Speedy:** +4 squares per phase (replaces Fast, still stacks with the derived bonus).

#### C. Size Modifiers (Apply Last)

* **Tiny / Small:** −1 square per phase
* **Medium:** +0
* **Large:** +1 square per phase
* **Huge:** +2 squares per phase
* **Gargantuan:** +3 squares per phase

---

### 3. Movement Action Logic (Multipliers)

The final value after all modifiers is the creature’s **Walk** speed in squares per phase. Faster movement options apply multipliers and combat tradeoffs.

| Mode   | Multiplier | Combat Effect                   |
| ------ | ---------- | ------------------------------- |
| Walk   | ×1         | Normal attacks allowed          |
| Run    | ×2         | −3 Threat Points to all attacks |
| Sprint | ×4         | No actions allowed              |

**Especially Speedy Variant:**
Creatures with the **Especially Speedy** trait use enhanced multipliers:

* **Run:** ×3
* **Sprint:** ×5
* **Burst:** ×7 (lasts 1 phase only; requires 1 full round of rest afterward)

---

### 4. Follow-Through Mechanic

Movement that occurs at the very end of a round (Phase 5) carries momentum into the next round.

* **Walking in Phase 5:** The creature acts normally on its initiative in the next round.
* **Running in Phase 5:** The creature makes an immediate attack at the very start of the next round (effectively Phase 0), suffering the usual −3 Threat Point running penalty.
* **Sprinting in Phase 5:** The creature continues moving but cannot act until its next eligible turn.

---

### Developer Example

**Creature:** Large Wolf (standard Quick Stat Block)
**Stats:** BP d8, Trait: Fast, Size: Large

1. **Base:** (12 + 8) ÷ 5 = 4.0 → 4 squares
2. **Derived Bonus (d8):** +2
3. **Trait (Fast):** +1
4. **Size (Large):** +1

**Total Walk Speed:** 8 squares per phase
**Run:** 16 squares (−3 Threat Points)
**Sprint:** 32 squares (no actions)

This is the value your Encounter+ module should treat as authoritative for grid movement.
