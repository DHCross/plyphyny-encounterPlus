# Eldritch RPG / Plyphyny System Manual

The Eldritch / Plyphyny system is an action-oriented role-playing engine that prioritizes narrative flow over grid simulation, though it supports tactical play. Its mechanics are built on a "die-step" system where proficiency is measured by the size of the die (d4 to d12) rather than a static number.

## Core Mechanics

### 1. The Ability Tree (Resolution Mechanic)
All actions are resolved using an **Ability Tree** structure consisting of three tiers. When attempting an action, you build a dice pool by combining the dice from these tiers:

*   **Tier 1: Basic Ability:** The root attribute (Competence, Prowess, or Fortitude).
*   **Tier 2: Specialty:** A learned skill governed by the Basic Ability (e.g., Agility or Melee).
*   **Tier 3: Focus:** A specific area of expertise that grants a static bonus (e.g., +1 to +5) rather than an extra die.

**The Roll:** `Basic Die + Specialty Die + Focus Bonus` vs `Challenge Die (or Opponent Roll)`

#### Situational Challenge Dice
When facing environmental or abstract challenges (not active opponents), the GM **rolls** a Challenge Die instead of setting a static Target Number.

| Difficulty | Challenge Die | Disadvantage (Sum) |
| :--- | :--- | :--- |
| Easy | d4 | 2d4 |
| Moderate | d6 | 2d6 |
| Difficult | d8 | 2d8 |
| Demanding | d10 | 2d10 |
| Formidable | d12 | 2d12 |

*Easier than Easy = Automatic Success.*

### 2. The Three Core Abilities
Every character is defined by three primary stats:
*   **Competence:** Represents mental acumen, knowledge, and social influence.
*   **Prowess:** Covers physical coordination, combat skills, and agility.
*   **Fortitude:** Represents physical toughness, willpower, and resistance to harm.

### 3. Combat Resolution (Ablative Defense)

#### The Core Philosophy: No "To-Hit" Rolls
Eldritch uses an **ablative defense system** rather than a binary "to-hit" mechanic. Every attack is assumed to be a successful exertion of force—there is no "miss." The attacker rolls to determine the **magnitude** of their threat, and whether that threat results in injury depends entirely on the defender's resources.

*   **Threat Points (Potential Harm):** The raw input value from the attacker's roll. Represents kinetic energy, magical force, or lethal intent.
*   **Damage (Actual Harm):** The final integer applied to Passive Defense after all mitigation. Represents actual injury.

#### Attack Sequence (Generating Threat Points)
The attacker rolls their relevant **Ability + Specialty**:
*   **Melee:** `Prowess Die + Melee Die + Threat Focus Bonus`
*   **Ranged:** `Prowess Die + Precision Die + Ranged Threat Focus Bonus`
*   **Iconic Bonus:** +1 Threat per Level + Resonant Focus (Might/Ferocity/Speed)
*   **Mastery Die:** Optional addition. If using Iconic Weapon and rolling a 1, trigger Master Twist.

#### Defense Resolution (Process in Order)

**Step A: Shield Mitigation**
*   *Condition:* Defender must have AD > 0 to actively block.
*   *Effect:* Static reduction: Small -1, Medium -2, Large -3 TP.
*   *Result:* If TP reduced to 0, attack is fully deflected.

**Step B: Active Defense (AD)**
*   *Pool:* `Prowess MV + Agility MV + Melee MV`
*   *Effect:* Remaining TP deducted from AD pool. Refreshes after combat.
*   *Absorbed:* `Min(Remaining_TP, Current_AD)`
*   *Overflow:* If TP exceeds AD (pool hits 0), excess continues to Step C.

**Step C: Armor Reduction (DR)**
*   *PC Mechanic:* Roll Armor Die (Leather d6, Chain d8, Plate d10) to reduce remaining TP.
*   *Monster Mechanic (QSB):* Non-legendary monsters use static HP bonus instead of rolling.

**Step D: Passive Defense (PD)**
*   *Pool:* `Fortitude MV + Endurance MV + Strength MV`
*   *Effect:* `Final_Damage = Max(0, Remaining_TP - Armor_Roll)`
*   *Consequence:* PD heals slowly (1-2/day).
*   *0 PD:* Unconscious. *Negative PD ≥ Fortitude MV:* Death.

#### Implementation Pseudocode
```
1. Input: Total_Threat = Attack Roll
2. IF Active_Defense > 0 AND Has_Shield:
      Total_Threat = Total_Threat - Shield_Value
3. Absorbed_By_AD = Min(Total_Threat, Active_Defense)
   Active_Defense = Active_Defense - Absorbed_By_AD
   Remaining_Threat = Total_Threat - Absorbed_By_AD
4. IF Remaining_Threat > 0:
      Armor_Value = Roll(Armor_Die) // or static for QSB monsters
      Final_Damage = Max(0, Remaining_Threat - Armor_Value)
5. Passive_Defense = Passive_Defense - Final_Damage
```

#### Advanced Mechanics
*   **Defense Negation:** Some feats/spells bypass defense layers (costs 5 SP, requires d12 Challenge roll).
*   **SP Backlash:** If SP runs out, costs are paid directly from Passive Defense.

### 4. Battle Phases (Initiative)
Combat rounds (approx. 10 seconds) are divided into five **Battle Phases**. Initiative is determined by your **Initiative Score**.

#### Initiative Score Calculation
`Initiative Score = Prowess Die Max Value + Reaction Focus + Finesse Focus`

*   **Prowess:** The primary determinant of turn order.
*   **Reaction:** This Agility-based focus adds directly to the Prowess MV.
*   **Finesse:** If wielding a Finesse weapon, this focus bonus also adds to the calculation.

#### Phase Breakpoints
| Initiative Score | Battle Phase | Timing |
| :--- | :--- | :--- |
| **12+** | **Phase 1** | First (0-2 seconds) |
| **9–11** | **Phase 2** | Second (2-4 seconds) |
| **7–8** | **Phase 3** | Third (4-6 seconds) |
| **5–6** | **Phase 4** | Fourth (6-8 seconds) |
| **1–4** | **Phase 5** | Last (8-10 seconds) |

*Note:* Legendary creatures with Prowess/BP ranks of **d14, d16, d18, or d20** act in a special "Pre-Phase 1" segment.

#### Intra-Phase Sorting (Tie-Breaking)
When multiple combatants act in the same Phase:
1.  **Weapon Reach/Range:** Longer reach/range acts first.
2.  **Heroic Order:** Player Characters and Legendary NPCs act before Minor, Standard, or Exceptional NPCs.
3.  **Random Initiative:** If still tied, roll `Prowess + Agility + Reaction`. Highest roll acts first.

#### Movement Systems

**Theater of the Mind (Narrative):**
*   *Unit:* Yards per Round (10 seconds)
*   *Formula:* `Move = 12 + Prowess_MV + Agility_MV`
*   *Multipliers:* Run ×2 (-3 TP), Sprint ×4 (no attacks)

**VTT / Tactical Grid:**
*   *Unit:* 5-ft Squares per Phase (2 seconds)
*   *Formula:* `Base Squares = floor((12 + Prowess_MV + Agility_MV) / 5)`
*   *Rounding:* Default = Down. Round UP if actor has Agility Specialty.

**The "Fast Layer" Modifiers (add to Speed Mod field):**

| Modifier Type | Bonus |
| :--- | :--- |
| **Speed Focus (d4–d6 BP)** | +1 |
| **Speed Focus (d8–d10 BP)** | +2 |
| **Speed Focus (d12+ BP)** | +3 |
| **Fast Trait** | +1 |
| **Especially Speedy** | +4 (replaces Fast) |
| **Tiny Size** | -1 |
| **Large Size** | +1 |
| **Huge Size** | +2 |
| **Gargantuan Size** | +3 |

**Action Multipliers:**
| Action | Speed | Combat Effect |
| :--- | :--- | :--- |
| Walk | ×1 | No penalty |
| Run | ×2 | -3 Threat Points to attacks |
| Sprint | ×4 | No actions allowed |

**Grid Occupation (Token Size):**
| Size | Grid Space | Notes |
| :--- | :--- | :--- |
| Tiny | 1 Square (shared) | Up to 4 per square |
| Small/Medium | 1 Square (1×1) | Standard |
| Large | 4 Squares (2×2) | |
| Huge | 9 Squares (3×3) | |
| Gargantuan | 16+ Squares (4×4+) | |

#### Follow-Through (Momentum Rule)
Actions in **Phase 5** carry momentum into the next round:

*   **Walk in Phase 5:** Start Round 2 normally.
*   **Run in Phase 5:** Immediate attack at Start of Round 2 ("Pre-Phase 1"), but with **-3 TP penalty**.
*   **Sprint in Phase 5:** Cannot act until **Phase 2** of Round 2 (skip Phase 1).

### 5. Magic System
Magic is skill-based rather than slot-based. Casters roll **Competence → Expertise** (plus a focus in Wizardry or Theurgy) against a Challenge Die determined by the spell's rarity.

*   **Spirit Points (SP):** A resource pool used to fuel powerful spells, magic items, or special feats. `Competence + Willpower`.
*   **Backlash:** Running out of SP can cause physical damage.

#### The Six Effects of Magic
| Effect | Function | Description |
| :--- | :--- | :--- |
| **Activate** | Event Catalyst | Summon, teleport, create light, traps, wards, contingent magic |
| **Afflict** | Status/Control | Stun, slow, confuse, paralyze, control mind (resisted via ST, not Defense) |
| **Harm** | Direct Damage | Inflict Threat Points (elemental, arcane, psychic attacks) |
| **Modify** | Alteration | Transmute, resize, buff/debuff abilities and attributes |
| **Protect** | Defense | Magical shields, conjured armor, walls, damage reduction, immunities |
| **Restore/Destroy** | Life/Entropy | Heal, cure, revive (Restore) or decay, disintegrate (Destroy) |

#### Spell Potency & Challenge
| Potency | Rarity | Challenge | TN | Maint. Penalty | Unlearned Cost (SP) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | Common | None | Auto | None | 0 |
| 1 | Common | d4 | 4 | -1 | 4 |
| 2 | Uncommon | d6 | 6 | -2 | 6 |
| 3 | Esoteric | d8 | 8 | -3 | 8 |
| 4 | Occult | d10 | 10 | -4 | 10 |
| 5 | Legendary | d12 | 12 | -5 | 12 |

*Learned Path Spells cost 0 SP. Unlearned Cost = Challenge Die Max Value.*

#### Spell Failure Consequences
| Rarity | Reattempt Delay | Consequence |
| :--- | :--- | :--- |
| Common (d0) | N/A | None |
| Common (d4) | 1 Round | Spell Fizzles |
| Uncommon (d6) | 2 Rounds | -1 SP |
| Esoteric (d8) | 3 Rounds | -3 SP |
| Occult (d10) | 4 Rounds | -4 SP |
| Legendary (d12) | 5 Rounds | -5 SP |

*Path Mastery feat negates failure consequences for chosen path.*

#### Defense Negation Costs
| Negation | Challenge | SP Cost | Note |
| :--- | :--- | :--- | :--- |
| Bypass Armor | Armor Die | 1–5 SP | Cost = armor rank |
| Bypass Shield | d8/d10/d12 | 3/4/5 SP | By shield size |
| Bypass AD | d12 | 5 SP | Requires Mastery Die |

#### Ranked Effect Unlocks
| Branch Rank | Classification | Unlocks |
| :--- | :--- | :--- |
| 1–3 | Weak | Common (d4) |
| 4+ | Average | Uncommon (d6) |
| 12+ | Respectable | Esoteric (d8) |
| 16+ | Skilled | Occult (d10) |
| 20+ | Great | Legendary (d12) |
| 24+ | Phenomenal | Legendary+ (d12+) |

#### Spell Rarity Distribution (Loot)
| Rarity | Standard | Gritty | Arcane-Rich |
| :--- | :--- | :--- | :--- |
| Common | 01–45 | 01–55 | 01–35 |
| Uncommon | 46–75 | 56–85 | 36–65 |
| Esoteric | 76–90 | 86–95 | 66–85 |
| Occult | 91–98 | 96–99 | 86–95 |
| Legendary | 99–00 | 00 | 96–00 |

### 6. Arcanum (Magic Crafting)
Arcanum governs the "craft" of magic—binding magical effects into physical forms (items, potions, wards) through formulae and components.

#### Prerequisites
*   **Gift of Magic:** Required to manipulate magical energy.
*   **Arcanum Advantage (4 CP):** Grants knowledge of formulae and rituals.
*   **Ritual Magic Feat (Adepts):** Adds Mastery Die to crafting rolls.

#### Crafting Challenge Table
| Rarity | Potency | Challenge (2× Die) | Time |
| :--- | :--- | :--- | :--- |
| Common | d4 | 2d4 | 1 hour |
| Uncommon | d6 | 2d6 | 2 hours |
| Esoteric | d8 | 2d8 | 3 hours |
| Occult | d10 | 2d10 | 4 hours |
| Legendary | d12 | 2d12 | 5 hours |

**Crafter's Roll:** `Competence + Expertise + Focus` (+ Mastery if Adept)

#### Types of Arcanum
*   **Artificing:** Imbue objects with spell effects. Items have `Energy Points = Creator's Branch MV`.
*   **Alchemy:** One-shot potions. Failure causes SP backlash = Rarity MV.
*   **Wards/Glyphs:** Inscribe time = Challenge Die in seconds. Trigger on conditions.
*   **Spell Ritualization:** Cast non-instant spells as rituals (+2 per 10 min, max +5).

#### Permanency
To create Artifacts that recharge: **Permanency Ritual** (Level 3+), difficulty 2d4–2d12.

### 7. The Mastery Die
As characters level up, they gain a **Mastery Die** (d4 to d12).
*   **Usage:** Add to rolls for feats, spells, or iconic item attacks limited times per day.
*   **Master Twist:** If Mastery Die rolls a 1 (on Iconic Item), re-roll and add to total.

### 8. Character Points (CP) & Advancement
Progression is point-buy. CP is used to purchase higher die ranks or advantages. **Level** is derived from *Earned* CPs (not starting build).

#### Level & Mastery Progression
| Level | Earned CP | Mastery Die | Uses/Day |
| :--- | :--- | :--- | :--- |
| 1 | 10–100 | d4 | 2 |
| 2 | 101–199 | d6 | 4 |
| 3 | 200–299 | d8 | 6 |
| 4 | 300–399 | d10 | 8 |
| 5 | 400–500+ | d12 | 10 |

#### Earning CPs
| Source | Amount |
| :--- | :--- |
| Showing Up | 1 CP |
| Participation | 1 CP |
| Creative Play/Risk | +2 CP |
| Singular Action (win encounter) | 4 CP |
| Survival (devastating battle) | 4 CP |
| Overcoming Danger | 2 CP |
| Scene/Arc Completion | ~10 CP |
| Negotiate Minor Threat | 2 CP |
| Negotiate Standard Threat | 4 CP |
| Negotiate Exceptional Threat | 6 CP |
| Negotiate Legendary Threat | 8–10 CP |

#### Spending CPs
| Improvement | Cost |
| :--- | :--- |
| Increase Die Rank | New Die's Max Value (d4→d6 = 6 CP) |
| Increase Focus (+1) | 4 CP per +1 |
| Cross-Class Feat (Lvl 3) | 8 CP |
| Cross-Class Feat (Lvl 4) | 6 CP |
| Cross-Class Feat (Lvl 5) | 4 CP |

## Advantages

### General Advantages
| Advantage | CP | Effect |
| :--- | :--- | :--- |
| Animal Affinity | 2 | +2 to fauna lore/animal handling |
| Arcane Inheritance | 4 | Start with magical Iconic Item |
| Arcanum | 4 | Craft magic items (+2 Expertise). Requires Gift of Magic |
| Attractiveness | 2/rank | d4–d12 ranked. Manipulate via opposed vs Willpower |
| Brutishness | 2 | +1 harm per 2 CP in unarmed combat (max +4) |
| Commanding | 2 | +2 when directing troops/allies |
| Eidetic Memory | 2 | +2 to learn spells or recall facts |
| Empathic | 2 | +2 to read emotions |
| Expeditious | 2 | +2 to Speed rolls (run/sprint) |
| Fortunate | 4 | Re-roll a "1" once per day |
| Heightened Senses | 2/sense | +1 per sense (Sight, Hearing, etc.) |
| Inconspicuous Caster | 2 | Reduce silent/still casting penalty |
| Intimidation | 2 | +2 Fortitude to dominate/resist |
| Intuitive | 2 | +2 Perception branch |
| Linguist | 2 | +2 to speak/understand languages |
| Literacy | 1–2 | Read/write (1 CP = 1 language, 2 CP = all) |
| Lorekeeper | 2 | +2 research; 1 hint/session |
| Menacing | 2 | +2 Perception (coercion) or Strength |
| Natural Talent | 2 | +2 to all Expertise checks |
| Observant | 2 | +2 Perspicacity |
| Read Emotions | 2 | Insight into motivations (+2 if Intuitive) |
| Religion | 2 | Knowledge of beliefs/rituals |
| Resilient | 2 | Double PD healing rate |
| Scholar | 2 | +2 Expertise for class knowledge |
| Sense of Direction | 1 | Always know true north |
| Streetwise | 2 | +2 urban social interaction |
| Strong-willed | 2 | +2 Willpower → Courage |
| Survival | 2/rank | +1 to +5 survival checks |
| Tactician | 2 | Swap Prowess for Competence in maneuvers (+2) |
| Underworld Contacts | 1 | Know shady contacts |

### Magical Advantages
| Advantage | CP | Effect |
| :--- | :--- | :--- |
| Gift of Magic (Tier 1) | 8 | Cast Wizardry/Theurgy spells |
| Gift of Magic (Tier 2) | 12 | Tier 1 + Magic Defense |
| Magic Defense | — | Use AD against magical damage |
| Magic Resistance (Lesser) | 2 | +1 saves vs magical afflictions |
| Magic Resistance (Greater) | 4 | +2 saves vs d10/d12 afflictions |
| Mythic Physiology | GM | Species traits (Natural Armor, etc.) |
| Low-light Vision | 2 | See in dim light |
| Night Vision | 4 | See in total darkness (60 ft) |

## Character Classes

| Class | Category | Base Die Ranks (Ability -> Specialty -> Focus) | Class Advantages | Class Feats |
| :--- | :--- | :--- | :--- | :--- |
| **Adept** | Wizardry | **Competence d6** -> Adroitness d4 (Cleverness +1) + Expertise d6 (Wizardry +1) + Perception d4 (Perspicacity +1) | Arcanum, Gift of Magic, Literacy, Scholar | Guile, Lore, Ritual Magic, Quick-witted |
| **Assassin** | Skullduggery | **Competence d4** -> Adroitness d6 + Perception d4<br>**Prowess d4** -> Agility d4 + Melee d4 (Finesse or Ranged Finesse +1)<br>**Fortitude** -> Vitality d6* | Expeditious, Heightened Senses (Hearing), Observant, Read Emotions | Death Strike, Lethal Exploit, Ranged Ambush, Shadow Walk |
| **Barbarian** | Warcraft | **Prowess d6** -> Melee d8<br>**Fortitude d4** -> Strength d4 (Ferocity +1) | Animal Affinity, Brutishness, Menacing, Resilient | Berserk, Brawl, Feat of Strength, Grapple |
| **Mage** | Wizardry | **Competence d6** -> Expertise d8 (Wizardry +1)<br>**Fortitude d4** -> Willpower d6 (Resistance +1) | Arcanum, Gift of Magic, Magic Defense, Scholar | Arcane Finesse, Dweomers, Intangible Threat, Path Mastery (Thaumaturgy, Elementalism, or Sorcery) |
| **Mystic** | Wizardry | **Competence d6** -> Expertise d6 (Wizardry +1)<br>**Prowess d4** -> Melee d4<br>**Fortitude d4** -> Endurance d6 (Resilience +1 & Vitality +2) | Empathic, Gift of Magic, Intuitive, Magic Resistance (Lesser), Strong-Willed | Iron Mind, Path Mastery ("Mysticism"), Premonition, Psychic Powers |
| **Rogue** | Skullduggery | **Competence d4** -> Adroitness d4 (Skulduggery +1) + Perception d4<br>**Prowess d6** -> Agility d8 | Expeditious, Fortunate, Streetwise, Underworld Contacts | Backstab, Evasion, Roguish Charm, Stealth |
| **Theurgist** | Theurgy | **Competence d8** -> Expertise d4 (Theurgy +1)<br>**Fortitude d6** -> Willpower d4 | Gift of Magic, Magic Defense, Religion, Strong-Willed | Divine Healing, Path Mastery (Druidry or Hieraticism), Spiritual Smite, Supernatural Intervention |
| **Warrior** | Warcraft | **Prowess d8** -> Melee d6 (Threat +1)<br>**Fortitude d6** | Commanding, Intimidation, Magic Resistance (+1), Tactician | Battle Savvy, Maneuvers, Stunning Reversal, Sunder Foe |

***Note on Assassin Base Ranks:** While *Vitality* is a Focus of *Endurance* (Fortitude), the Assassin class description lists Vitality d6 alongside Prowess and Agility requirements.

## Class Feats

### Adept Feats
| Feat | Test | Challenge | Effect |
| :--- | :--- | :--- | :--- |
| Guile | Comp→Adroit→Skulduggery | d4–d12 | Persuade, trick, influence |
| Lore | Comp→Expertise→Scholar | d4–d12 | Recall locations, creatures, laws |
| Ritual Magic | Comp→Expertise→Arcanum | d4–d12 | Craft items; cast unlearned rituals |
| Quick-witted | Comp→Adroit→Cleverness | Variable | Jury-rig solutions |

### Assassin Feats
| Feat | Sub-Feat | Test | Effect |
| :--- | :--- | :--- | :--- |
| Death Strike | — | Prow→Melee→Finesse (d10/d12) | +2nd Prowess die from ambush |
| Death Strike | Stunning | vs Fortitude | 2 SP: Stun victim |
| Lethal Exploit | Bypass Armor | Comp→Perc→Alertness (d8) | Ignore armor DR |
| Ranged Ambush | Vitality Shot | Prow→Precision (d10) | Bypass AD |
| Ranged Ambush | Pin to Wall | vs Agility | 5 SP: Restrain target |
| Shadow Walk | — | Prow→Agility→Reaction (d12) | 1 Mastery: Move through shadows |

### Barbarian Feats
| Feat | Sub-Feat | Test | Effect |
| :--- | :--- | :--- | :--- |
| Berserk | Rage | Fort→Str→Ferocity (d8) | +Threat from rage |
| Berserk | Thrash | Prow→Melee→Threat (d10) | Bypass AD |
| Berserk | Trounce | Prow→Melee→Threat (d12) | Bypass armor |
| Brawl | Crush | Prow→Melee (d6) | +Unarmed damage |
| Brawl | Throw/Tackle | Prow→Str vs Agility | Hurl or knock prone |
| Feat of Strength | — | Fort→Str→Might | Break/lift obstacles |
| Grapple | — | Prow→Str→Might (d10) | Immobilize opponent |

### Mage Feats
| Feat | Sub-Feat | Effect |
| :--- | :--- | :--- |
| Arcane Finesse | Bypass Armor | 1–5 SP: Spell ignores armor |
| Arcane Finesse | Bypass AD | Mastery: Negate AD pool |
| Arcane Finesse | Nullify Shield | Negate shield bonuses |
| Dweomers | Increase Harm | Boost spell threat |
| Dweomers | Area Effect | 4 SP: Single→AoE (d10) |
| Intangible Threat | — | Non-physical damage |
| Path Mastery | — | Passive: No failure effects; re-roll Mastery 1s |

### Mystic Feats
| Feat | Sub-Feat | Test | Effect |
| :--- | :--- | :--- | :--- |
| Iron Mind | — | Fort→Will→Resistance | Block mind reading |
| Premonition | Insight | Comp→Perc (d8) | Sense impending danger |
| Premonition | Sense Threat | Comp→Perc (d6) | Determine threat level |
| Psychic Powers | Mind Read | vs Willpower | Detect surface thoughts |
| Psychic Powers | See Aura | Comp→Perc (d6) | View health/magic auras |
| Path Mastery | Mysticism | Passive | Enhance Mastery for Mysticism |

### Rogue Feats
| Feat | Sub-Feat | Test | Effect |
| :--- | :--- | :--- | :--- |
| Backstab | — | Prow→Melee→Finesse | +Damage from surprise |
| Evasion | Elude Hazard | Prow→Agil→Reaction | Dodge traps/hazards |
| Evasion | Dodge | Prow→Agil (d12–d4) | 4 SP: Avoid all harm |
| Roguish Charm | — | Comp→Adroit (d8) | Befriend/persuade |
| Stealth | — | vs Perception | Move silently, gain surprise |

### Theurgist Feats
| Feat | Sub-Feat | Effect |
| :--- | :--- | :--- |
| Divine Healing | Bolster/Mend | Restore AD or PD |
| Divine Healing | Cure Debility | Restore lost die ranks |
| Divine Healing | Regenerate | Regrow limbs (d12) |
| Spiritual Smite | — | Channel divine damage (d8/d12) |
| Path Mastery | Druidry/Hieraticism | Specialize in path |
| Supernatural Intervention | — | All SP: Petition deity (d12) |

### Warrior Feats
| Feat | Sub-Feat | Test | Effect |
| :--- | :--- | :--- | :--- |
| Battle Savvy | Bypass Armor | Prow→Melee (d10) | Ignore armor DR |
| Battle Savvy | Focused Strike | Variable | +Threat bonus |
| Maneuvers | Disarm | vs Agility | Knock weapon away |
| Maneuvers | Feint | vs Perception | Bypass shields, +damage |
| Maneuvers | Leg Sweep/Trip | Prow→Melee (d6) | Knock prone, reduce init |
| Maneuvers | Multiple Attacks | Special | Split pool for extra attacks |
| Stunning Reversal | — | Prow→Agil→Reaction | Augment attack + restore AD |
| Sunder Foe | — | Prow→Str→Might (d10) | +Damage, destroy gear |

### Feat Resolution
*   **Roll:** Ability Branch vs Challenge Die (d4–d12) or Contested
*   **Mastery Die:** Optional addition for success/special effects
*   **Success:** Effect occurs; SP deducted if required
*   **Failure:** No effect; no SP spent (usually)

**Modalities:** Full Action | Overlay (enhances attack) | Reaction (triggered)

### Feat Spirit Point Costs

#### Assassin SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Death Strike: Stunning | 2 SP | Force stun save |
| Ranged Ambush: Vitality Shot | 5 SP | Bypass AD |
| Ranged Ambush: Pin to Wall | 5 SP | Restrain target |

#### Barbarian SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Rage | 1 SP per +1 TP | Max +5 TP |
| Thrash | 5 SP | Bypass AD |
| Trounce | 1–5 SP | Bypass Armor (= Armor Rank) |
| Crush | 1–5 SP | Add Strength Die (= Str Rank) |
| Throw/Tackle | 2 SP | Hurl or knock prone |

#### Mage SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Bypass Armor | 1–5 SP | = Armor Die Rank |
| Bypass AD | 5 SP | Negate AD pool |
| Reduce Save | 1 SP per -1 | Penalty to resistance |
| Nullify Shield | 3–5 SP | Small/Med/Large |
| Increase Harm | 1–5 SP | +1 to +5 TP |
| Area Effect | 1 SP/round | Single→AoE |
| Intangible Threat | 4–17 SP | Non-physical damage |
| Clandestine | 1–3 SP | Remove Words/Gestures/Audio/Visual |

#### Rogue SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Dodge | 4 SP | Avoid all harm (one attack) |

#### Theurgist SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Bolster/Mend | 1 SP | Restore Defense |
| Cure Debility | Variable | = Restored Die MV |
| Heal | 12 SP | Restore AD + PD |
| Negate Affliction | 4–12 SP | By condition strength |
| Regenerate | 12 SP | Regrow limbs |
| Spiritual Smite | 8–12 SP | +3 to +5 TP; +2 SP per extra +1 |
| Supernatural: Avatar | 12 SP | Divine intervention |
| Supernatural: Resurrection | 2d12 SP | Even on failure |

#### Warrior SP Costs
| Feat | Cost | Effect |
| :--- | :--- | :--- |
| Bypass Armor | 1–5 SP | = Armor Die Rank |
| Focused Strike | 1–5 SP | +1 TP per SP |
| Sunder Foe | 3 SP | +3 TP, destroy gear |

### Defense Negation Summary
| Target | SP Cost |
| :--- | :--- |
| Bypass Armor | 1–5 SP (= Armor Die Rank) |
| Bypass Shield | 3–5 SP (Small 3, Med 4, Large 5) |
| Bypass AD | 5 SP (+ Mastery Die) |

## Races

| Race | Base Die Ranks (Ability -> Specialty -> Focus) | Advantages & Flaws |
| :--- | :--- | :--- |
| **Drakkin** | **Competence d6**<br>**Prowess d6**<br>**Fortitude d6** -> Endurance d6 + Strength d4 | **Advantages:** Breath Weapon, Natural Armor (1d4), Night Vision. |
| **Dwarf** | **Prowess d6** -> Melee d6<br>**Fortitude d8** -> Endurance d4 | **Advantages:** Night Vision, Sense of Direction, Strong-willed. |
| **Elf** | **Competence d6** -> Expertise d6 (Wizardry +1)<br>**Prowess d4** -> Agility d4 (Reaction +1) | **Advantages:** Gift of Magic, Magic Resistance (+1), Night Vision. |
| **Gnome** | **Competence d4** -> Adroitness d6 + Expertise d6 + Perception d4 (Perspicacity +1) | **Advantages:** Eidetic Memory, Low-light Vision, Observant.<br>**Flaw:** Restriction (small weapons only). |
| **Half-Elf** | **Competence d6**<br>**Prowess d6** -> Agility d4<br>**Fortitude d4** -> Endurance d4 + Willpower d4 | **Advantages:** Heightened Senses, Low-light Vision, Magic Resistance (+1). |
| **Half-Orc** | **Fortitude d6** -> Endurance d6 + Strength d8 (Ferocity +1) | **Advantages:** Intimidation, Low-light Vision, Menacing.<br>**Flaw:** Ugliness. |
| **Halfling** | **Competence d6** -> Adroitness d6 (Cleverness +1)<br>**Fortitude d6** -> Willpower d4 (Courage +1) | **Advantages:** Low-light Vision, Read Emotions, Resilient.<br>**Flaw:** Restriction (small weapons only). |
| **Human** | **Competence d6**<br>**Prowess d6** -> Melee d4 (Threat +1)<br>**Fortitude d4** -> Willpower d6 | **Advantages:** Fortunate, Survival. |

## Weapons & Equipment

### Melee Weapons
| Weapon Category | Weapon Name | Size / Reach | Damage Type |
| :--- | :--- | :--- | :--- |
| **Bludgeoning** | Club | Small / Short | Crushing |
| | Footman's Mace | Medium / Short | Crushing |
| | Staff | Medium / Short | Crushing |
| | Warhammer | Large / Short | Crushing |
| **Blades** | Dagger | Small / Short | Impaling |
| | Great Axe | Large / Medium | Slashing |
| | Greatsword | Large / Medium | Slashing |
| | Handaxe | Small / Short | Slashing |
| | Rapier | Medium / Medium | Impaling |
| | Standard Sword | Medium / Medium | Slashing |
| **Polearms** | Fauchard or Glaive | Large / Long | Slashing |
| | Halberd or Lucerne Hammer | Large / Long | Slashing |
| | Lance (Mounted) | Large / Long | Impaling |
| | Spear or Spear-Guisarme | Large / Long | Impaling |
| **Unarmed** | Fists | Short | Crushing |
| | Improvised | Short | Crushing |
| | Kicks | Short | Crushing |

### Ranged Weapons
Ranges are listed in feet for Short / Medium / Long.

| Weapon Name | Range (ft) | Damage Type |
| :--- | :--- | :--- |
| Compound Bow | 50 / 100 / 300 | Impaling |
| Crossbow, Heavy | 55 / 115 / 200 | Impaling |
| Crossbow, Light | 75 / 150 / 300 | Impaling |
| Dagger (thrown) | 10 / 30 / 50 | Impaling |
| Great Bow | 40 / 100 / 200 | Impaling |
| Longbow | 30 / 75 / 150 | Impaling |
| Shortbow | 20 / 50 / 100 | Impaling |
| Sling | 10 / 20 / 50 | Crushing |
| Spear (thrown) | 10 / 30 / 50 | Impaling |
| Throwing Axe | 10 / 30 / 50 | Slashing |

### Damage Type & Focus Synergy
If you wield an **Iconic Weapon**, you add the bonus from the specific Focus below to your Threat Points.

| Damage Type | Associated Focus Bonus | Iconic Weapon Synergy |
| :--- | :--- | :--- |
| **Crushing** | **Might** (Strength) | Wielding warhammers, clubs, maces, staves, or slings. |
| **Slashing** | **Ferocity** (Strength) | Wielding swords, axes, or throwing axes. |
| **Impaling** | **Speed** (Agility) OR **Skullduggery** (Adroitness)* | Wielding rapiers, spears, bows, crossbows, or daggers. (*Rogues may use Skullduggery*) |

## The Quick Stat Block (QSB)
The **Quick Stat Block (QSB)** is a streamlined data format designed to allow Game Masters to run combat encounters efficiently without managing full character sheets for every opponent. While Player Characters (PCs) are built using the granular **Ability Tree** system to allow for long-term progression and customization, the QSB abstracts these mechanics into immediate, static values to prioritize narrative speed and ease of play.

### The QSB Format Structure

The QSB distills a creature's capabilities into specific, abbreviated tags:

*   **TY (Type):** The creature's **Category** (Minor, Standard, Exceptional, Legendary). This defines its "weight class" and caps the number of dice it can use in an attack.
*   **TD (Threat Dice):** The attack pools available to the creature (e.g., *Melee 2d6*). Unlike PCs who build pools from abilities, creatures use pre-calculated dice combinations for **Melee**, **Ranged**, **Natural**, and **Arcane** attacks.
*   **HP (Hit Points):** A single abstract pool split 50/50 into Active and Passive defense (unless modified by traits like "Fast" or "Tough").
*   **DR (Damage Reduction):** For most creatures, armor is converted into a **static HP bonus** added to the Passive Defense pool rather than a die roll.
*   **ST (Saving Throw):** A single die rank (e.g., d6) used for all resistance checks, replacing the specific Ability Branch saves used by PCs.
*   **BP (Battle Phase):** A single die rank representing initiative and movement speed, replacing the complex Prowess + Focus calculations.

### Key Differences: QSB vs. PC Formatting

The primary difference lies in **Abstraction vs. Construction**. PCs are constructed to simulate growth and specific skill sets, whereas QSBs are abstracted to simulate threat levels during a scene.

#### 1. Attack Resolution (Pools vs. Threat Dice)
*   **PCs (Construction):** Players build dice pools by combining **Ability + Specialty + Focus**. A Warrior attacks by rolling Prowess + Melee + Threat Focus + Weapon Bonuses.
*   **QSB (Abstraction):** Monsters use **Threat Dice (TD)**. The math is pre-packaged. An Orc doesn't have a "Prowess" stat; it simply rolls `Melee 2d6`. The logic of *how* it attacks is baked into the die count.

#### 2. Defense and Armor (Rolling vs. Static Math)
*   **PCs:** Defense is a multi-step process involving Active Defense pools, Shield reduction, and **rolling Armor Dice** (e.g., d8 for chainmail) to reduce incoming damage.
*   **QSB:** To speed up combat, non-Legendary creatures do not roll for armor. Their armor value is converted into a **flat HP bonus** added directly to their Passive Defense. A goblin in leather armor doesn't roll a d6 to reduce damage; it simply has +3 HP.

#### 3. Saving Throws (Granular vs. Universal)
*   **PCs:** A PC must use specific Ability Branches for saves (e.g., *Competence $\rightarrow$ Perception* to disbelieve an illusion, or *Fortitude $\rightarrow$ Willpower* to resist fear).
*   **QSB:** Creatures possess a universal **Saving Throw (ST)** rank (e.g., d8). Regardless of whether they are dodging a trap or resisting a spell, the GM rolls this single die.

#### 4. The Legendary Exception
**Legendary Creatures** bridge the gap between QSB and PC formatting. Because they are narrative centerpieces (like Dragons or Demon Lords), they utilize PC-style mechanics for durability. Unlike standard monsters, Legendary creatures **roll for Armor DR** and possess specific Ability Trees for high-stakes interactions, rather than relying solely on static bonuses.

### NPC Level Templates (Full-Fledged NPCs)
For NPCs built like PCs (not QSB), use the Template Code system.

#### Level Templates
| Level | CP Range | Template | Mastery |
| :--- | :--- | :--- | :--- |
| 1 | 30–100 | AAB | d4 |
| 2 | 101–199 | ABC | d6 |
| 3 | 200–299 | BCD | d8 |
| 4 | 300–399 | CDD | d10 |
| 5 | 400–500+ | CDE | d12 |

#### Letter Code Definitions
Assign letters to Abilities (Competence, Prowess, Fortitude) by priority:

| Code | Ability | Specialties | Focuses |
| :--- | :--- | :--- | :--- |
| **A** | d4 | 3×d4 | None |
| **B** | d6 | 3×d6 | 1×(+1) |
| **C** | d8 | 3×d8 | 3×(+1) |
| **D** | d10 | 3×d10 | 2×(+2), 4×(+1) |
| **E** | d12 | 3×d12 | 3×(+3), 3×(+2) |

*Example: Level 3 Warrior (BCD) → D to Prowess, C to Fortitude, B to Competence*

## Iconic Items & Mastery Die

### 1. The Mastery Die
The Mastery Die represents a character's growing expertise, luck, and inner reserve. It is a bonus die that players can choose to add to ability tests, attack rolls, or class feats to increase their total result.

*   **Progression:** The size of the die and the number of times it can be used per day increase as the character gains levels.
    *   **Level 1:** d4 (2 uses/day)
    *   **Level 2:** d6 (4 uses/day)
    *   **Level 3:** d8 (6 uses/day)
    *   **Level 4:** d10 (8 uses/day)
    *   **Level 5:** d12 (10 uses/day)
*   **Surge:** If a character runs out of daily uses, they may spend **Spirit Points** equal to the Mastery Die's maximum value (e.g., 4 SP for a d4) to gain an additional roll.

### 2. Iconic Items (Signature Items)
Every character starts with one Iconic Item at Level 1 and may designate a new one at each level. These are personal items—heirlooms, masterwork weapons, or sentimental objects—that grant mechanical bonuses when used.

#### Iconic Weapons
When attacking with an Iconic Weapon, the character gains significant bonuses to their **Potential Harm** (Threat Points):
1.  **Level Bonus:** You add a static bonus of **+1 Threat Point per character level**.
2.  **Focus Synergy:** You add a *second* Focus bonus based on the weapon's damage type, stacking with your standard combat focus.
    *   **Crushing:** Adds **Might** (Strength).
    *   **Slashing:** Adds **Ferocity** (Strength).
    *   **Impaling:** Adds **Speed** (Agility) (or **Skullduggery** for Rogues).

#### Iconic Magic Foci
For spellcasters (Mages, Mystics, Theurgists), Iconic Items act as catalysts.
*   **Battle Foci:** When used to channel Harm spells, the caster adds their **Vitality** focus bonus to the Potential Harm.
*   **Inspirational Foci:** Non-combat items (lockets, journals) that grant a **+1 bonus per level** to ability checks in a specific branch (e.g., Competence $\rightarrow$ Adroitness).

### 3. The "Master Twist"
The most powerful interaction between these two mechanics is the **Master Twist**.

When a player uses their **Mastery Die** while using an **Iconic Item** (attacking with an iconic sword or casting with an iconic wand):
*   **Trigger:** If the Mastery Die rolls a **1** (its minimum value).
*   **Effect:** The player immediately **re-rolls** the Mastery Die and **adds** the new result to the original 1 (Total = $1 + New\ Roll$).

This mechanic represents a "twist of fate" or a moment of desperate brilliance brought about by the character's deep connection to their signature gear. This effect can only be activated once per use of the Mastery Die.
