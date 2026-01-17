Based on the video provided, here is a technical manual for creating and configuring custom RPG systems within the **Encounter+** application.

This guide focuses on the directory structure, JSON configuration, and asset management required to build a system from scratch.

---

# Manual: Creating Custom Systems in Encounter+

## 1. Initialization

Before editing code, you must initialize the system structure through the application interface.

1. **Launch Encounter+** on your Mac.
2. Navigate to **Settings** (Gear Icon) > **Systems**.
3. Click **Create** (top right).
4. **Configure System Details:**

* **Name:** Enter the name of your system (e.g., "Custom System").
* **Short Name:** enter a unique identifier (this will determine the folder name).

5. Click **Save**.
6. **Load the System:** In the Systems list, tap your new system and select **Load**.

## 2. Directory & File Structure

Once created, the application generates a specific file directory. Locate this to begin editing.

* **Location:** `~/Documents/Encounter+/systems/[system_name]/`
* **Key Files/Folders:**
* `entities.json`: Defines the core categories (Heroes, Monsters, Spells, Items).
* `lang/en.json`: Handles the localization and display names for the UI.
* `icons/`: Stores the PNG assets for the sidebar and tokens.

> **Note:** You can use any text editor to edit these files, though a code editor like VS Code is recommended for syntax highlighting.

## 3. Core Configuration (entities.json)

This file controls what objects exist in your system and how they behave.

1. Open `entities.json`.
2. You will see a list of default entities (Monster, Spell, Item, Hero).
3. **Entry Structure:**

```json
{
  "name": "Hero",
  "label": "heroes",
  "loadable": true,
  "role": "friendly"
}

```

4. **Field Definitions:**

* **name:** Internal ID for the entity type.
* **label:** The key used to link this entity to the language file (for display text) and the icon file.
* **loadable:** `true` or `false`.
* Set to `true` if this entity needs to be placed on a Battle Map (e.g., Characters, Monsters).
* Set to `false` for reference items (e.g., Spells, Loot).
* **role:** Defines default allegiance (e.g., `friendly` for heroes, `hostile` for monsters).

5. **Customization:** You may add, remove, or rename these blocks to fit your TTRPG needs.

## 4. Interface Localization (lang/en.json)

You must link the entities defined in Step 3 to human-readable text.

1. Open the `lang` folder and select `en.json`.
2. Locate the key that matches the **label** you defined in `entities.json`.

* *Example:* If your entity label is `"heroes"`, look for `"Entity.Custom.heroes"`.

3. Edit the value string to change what appears in the App Sidebar.

```json
"Entity.Custom.heroes": "Party Members"

```

4. If you added a *new* entity in Step 3, you must add a corresponding line here.

## 5. Iconography

To give your new entities custom icons in the sidebar:

1. Prepare your icon images as **PNG** files.
2. Navigate to the `icons` folder within your system directory.
3. **Naming Convention:** The filename **must** match the `label` defined in `entities.json`.

* *JSON Label:* `"heroes"`
* *Image Name:* `heroes.png`

4. Drop the file into the folder.

## 6. The Workflow Loop

Encounter+ does not live-update when you change external files. To see your changes:

1. Save all JSON and PNG files.
2. Return to Encounter+ **Settings** > **Systems**.
3. Select a different system (e.g., D&D 5E) and load it.
4. Select your **Custom System** and load it again.
5. Check the sidebar to verify your new categories, names, and icons are correct.


This manual provides a step-by-step guide to upgrading your Encounter+ system code to match the specific mechanics of the **Eldritch RPG (Plyphyny)** rules you uploaded.

These improvements focus on automating calculations (like Tactical Movement), separating data for better organization, and aligning your forms with the official Quick Stat Block (QSB) structure.

### 1. Enable Spells and Items

Your `lang/en.json` defines labels for Items and Spells, but your `entities.json` file is currently missing the definitions to make them actual, usable database objects.

**Action:** Open `plyphyny_It2X/entities.json` and update the list to include Items and Spells.

**JSON**

```
[
  {
    "name": "Monster",
    "label": "monster",
    "collection": { "label": "monsters" },
    "loadable": true
  },
  {
    "name": "Hero",
    "label": "hero",
    "collection": { "label": "heroes" },
    "loadable": true,
    "role": "friendly"
  },
  {
    "name": "Item",
    "label": "item",
    "collection": { "label": "items" },
    "loadable": false
  },
  {
    "name": "Spell",
    "label": "spell",
    "collection": { "label": "spells" },
    "loadable": false
  }
]
```

> **Why this helps:** This creates dedicated "folders" in the app for your Spells and Equipment, allowing you to manage them separately from Heroes and Monsters.

---

### 2. Automate Hero Stats (Movement & Armor)

Your current `hero.json` calculates defenses but is missing the **Tactical Movement** formula and the **Armor-as-Passive-HP** rule found in your PDFs.

**Action:** Open `plyphyny_It2X/forms/hero.json`.

A. Add the Movement & Armor Calculation

Scroll to the bottom attributes section. Update the calculations to include the Movement formula (12 + Prowess + Agility) / 5 and add Armor to Passive Defense.

**JSON**

```
    "attributes": [
        {
        "data.spiritpoints": "#{{data.competencedie}} + {{data.willpowerdie}}",
        "data.activedefense": "#{{data.prowessdie}} + {{data.agilitydie}} + {{data.meleedie}}",
        "data.passivedefense": "#{{data.fortitudedie}} + {{data.endurancedie}} + {{data.strengthdie}} + {{data.armordie}}",
        "data.movement": "#(12 + {{data.prowessdie}} + {{data.agilitydie}}) / 5"
        }
    ]
```

B. Display the Movement Stat

Add a field to display this calculated movement number. You can place this in the "Prowess Abilities" group or a new "Tactics" group.

**JSON**

```
{
  "title": "Tactical Movement (Squares/Phase)",
  "type": "number",
  "attribute": "data.movement"
}
```

---

### 3. Upgrade the Monster Form to "QSB" Standard

Your current monster form uses text fields for data that should be structured (like "Opponent Type"), and it lacks the detailed Health split (Active/Passive) required by Eldritch rules.

**Action:** Open `plyphyny_It2X/forms/monster.json`.

A. Use a Picker for Creature Category

Instead of typing "Standard" or "Legendary," force a choice to prevent typos.

1. First, add this to your `plyphyny_It2X/types.json`:
   **JSON**

   ```
   "CreatureCategory": {
     "Minor": "Minor",
     "Standard": "Standard",
     "Exceptional": "Exceptional",
     "Legendary": "Legendary"
   }
   ```
2. Then, update the field in `monster.json`:
   **JSON**

   ```
   {
     "title": "Creature Category",
     "type": "picker",
     "attribute": "data.Opponent_type",
     "attributeType": "CreatureCategory"
   }
   ```

B. Split Hit Points (Active vs Passive)

The QSB requires tracking both pools. Replace the single Hit Points field with two:

**JSON**

```
{
  "title": "Active HP (Defense Pool)",
  "type": "number",
  "attribute": "data.hpActive"
},
{
  "title": "Passive HP (Body/Soul)",
  "type": "number",
  "attribute": "data.hpPassive"
}
```

C. Fix Attack Flexibility

Your current form uses a picker for attacks (e.g., selecting 1d6). However, Eldritch monsters often have static modifiers (e.g., 1d6+2). Pickers cannot handle +2.

* **Recommendation:** Change the attack fields from `picker` to `text` to allow typing "1d6+2".
  **JSON**

  ```
  {
    "title": "Melee Threat (e.g. 1d6+2)",
    "type": "text",
    "attribute": "data.threatdicemelee"
  }
  ```

---

### 4. Organize Hero Lists

Currently, your Hero form dumps "Features, Items, Spells" into one single list. Separating these makes the character sheet easier to read and allows for specific fields (like "Cost" for spells).

**Action:** In `plyphyny_It2X/forms/hero.json`, replace the single "Features..." list with three distinct sections:

**Spells Section:**

**JSON**

```
{
  "title": "Grimoire (Spells)",
  "type": "list",
  "attribute": "data.spells",
  "form": {
    "title": "Spell",
    "sections": [
      {
        "type": "group",
        "fields": [
          { "title": "Spell Name", "attribute": "name" },
          { "title": "Path (e.g. Elementalism)", "attribute": "path" },
          { "title": "Spirit Cost", "attribute": "cost", "type": "number" },
          { "title": "Effect", "attribute": "text", "type": "textArea" }
        ]
      }
    ]
  }
}
```

**Inventory Section:**

**JSON**

```
{
  "title": "Inventory",
  "type": "list",
  "attribute": "data.inventory",
  "form": {
    "title": "Item",
    "sections": [
      {
        "type": "group",
        "fields": [
          { "title": "Item Name", "attribute": "name" },
          { "title": "Quantity", "attribute": "qty", "type": "number" },
          { "title": "Equipped?", "attribute": "equipped", "type": "switch" }
        ]
      }
    ]
  }
}
```

### Summary of Changes

1. **`entities.json`** : Added `Item` and `Spell` objects.
2. **`types.json`** : Added `CreatureCategory`.
3. **`forms/hero.json`** : Added **Movement** math, **Armor** math, and separated  **Spells/Inventory** .
4. **`forms/monster.json`** : Added **Category Picker** and split  **Active/Passive HP** .

Reload your system in Encounter+ (switch to D&D 5e and back to Plyphyny) to see these changes take effect.



---
