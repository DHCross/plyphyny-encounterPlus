# Creating Game Systems for Encounter+ Beta v5: An AI Developer's Guide

This guide outlines the architectural patterns and file structures required to build custom RPG systems in **Encounter+ Beta v5**. It is designed for AI coding assistants to understand the relationships between configuration, data entry (Forms), and display logic (Views).

---

## 1. System Architecture

A "System" in Encounter+ is a folder bundle ending in `.system` containing three core components.

### Folder Structure
```text
MyGame.system/
├── config.json          # Core definitions, stats, and resource bars
├── forms/               # JSON definitions for data entry UIs
│   ├── character.json
│   ├── adversary.json   # Often maps to 'monster' entity
│   ├── item.json
│   └── spell.json
└── views/               # HTML/Handlebars templates for stat blocks
    ├── character.json
    ├── adversary.json
    └── ...
```

---

## 2. Core Configuration (`config.json`)

The `config.json` file is the registry for the system. It defines what entities exist and how they are summarized in lists.

### Key Sections

*   **`id` & `name`**: Unique identifiers.
*   **`entities`**: Definitions for `character`, `monster`, `spell`, `item`.
    *   **`stat`**: The primary sorting stat (e.g., `cr`, `level`).
    *   **`combatant`**: Defines how the entity appears in the Battle Tracker.

### Combatant Configuration (Battle Tracker)
This section controls the tactical view. Encounter+ v5 supports multiple resource bars and dynamic details.

```json
"combatant": {
  "hp": "data.hp",                // Main health bar (Red)
  "adp": "data.ad_current",       // Active Defense (Blue)
  "pdp": "data.pd_current",       // Passive Defense (Orange)
  "init": "data.battlephase",     // Sorting value for initiative
  "detail": "{{data.race}} {{data.class}} - Phase {{data.battlephase}}" // Subtitle
}
```

---

## 3. Data Entry Forms (`forms/*.json`)

Forms define the UI for creating and editing entities. They use a proprietary JSON schema organized by **Tabs** > **Sections** > **Fields**.

### Structure
```json
{
  "tabs": [
    {
      "key": "main",
      "title": "Main Stats",
      "sections": [
        {
          "type": "group",
          "title": "Attributes",
          "fields": [ ... ]
        }
      ]
    }
  ]
}
```

### Common Field Types
*   **`text`**: Simple string input.
*   **`number`**: Numeric input.
*   **`select`**: Dropdown menu (`options` array required).
*   **`checkbox`**: Boolean switch.
*   **`readonly`**: Display-only field, often used for calculated results.

### Data Binding
*   **`attribute`**: Maps the input to the underlying data object (e.g., `data.prowessDie`).
*   **`render`**: Used in `readonly` fields to display derived data using Handlebars syntax (e.g., `Phase: {{data.battlephase}}`).

---

## 4. Display Views (`views/*.json`)

Views define how the entity looks when viewing its "Stat Block" or "Sheet". These are distinct from Forms.

**CRITICAL**: Encounter+ Beta v5 uses a **declarative view structure**, NOT raw HTML. The system expects a `"views"` array containing view component objects.

### Required Structure
```json
{
  "debug": false,
  "spacing": 8,
  "padding": [16],
  "views": [
    {
      "type": "hStack",
      "spacing": 12,
      "views": [
        {
          "type": "image",
          "value": "{{image}}",
          "width": 60,
          "height": 60
        },
        {
          "type": "vStack",
          "spacing": -1,
          "views": [
            {
              "style": "title",
              "value": "{{name}}"
            },
            {
              "style": "subtitle",
              "value": "{{data.class}} (Level {{data.level}})"
            }
          ]
        }
      ]
    },
    {
      "type": "divider"
    },
    {
      "type": "text",
      "value": "**HP:** {{data.hp}}"
    }
  ]
}
```

### View Component Types
*   **`hStack`**: Horizontal layout (side-by-side)
*   **`vStack`**: Vertical layout (stacked)
*   **`text`**: Markdown-formatted text (supports **bold**, *italic*, etc.)
*   **`image`**: Display images (supports `"value"`, `"width"`, `"height"`, `"link"`)
*   **`divider`**: Visual separator line
*   **`statBlock`**: Specialized container for stat block styling
*   **`list`**: Iterate over array attributes (uses `"attribute"` and nested `"views"`)

### Handlebars in Views
*   **Variables**: `{{name}}`, `{{data.hp}}`
*   **Filters**: `{{data.hp|default: 0}}`, `{{name|map: 'MonsterType'}}`
*   **Conditionals**: `{% if data.hp %}...{% endif %}`
*   **Includes**: `{% include "partial-name.md" %}` (for markdown partials)

### Common Styles
*   `"title"` - Large header text
*   `"subtitle"` - Secondary header
*   `"stats-ability"` - Centered ability score boxes
*   `"section-title"` - Section headers
*   `"stats-body"` - Standard stat block text

### ❌ WRONG (Old/Invalid Format)
```json
{
  "layout": [
    { "type": "header", "field": "name" },
    { "type": "section", "fields": ["race", "class"] }
  ]
}
```

### ✅ CORRECT (v5 Format)
```json
{
  "views": [
    {
      "style": "title",
      "value": "{{name}}"
    },
    {
      "type": "text",
      "value": "{{data.race}} {{data.class}}"
    }
  ]
}
```

---

## 5. Implementing Deterministic Mechanics (AI Workflow)

When implementing complex rules (like Plyphyny's Phase Combat or Movement), follow this pattern:

### Step 1: Define the Data Model
Decide on the JSON paths. Use strict naming conventions.
*   `data.prowessMV` (Number)
*   `data.speedFocus` (Number)
*   `data.hasAgilitySpecialty` (Boolean)

### Step 2: Create the Inputs (Forms)
Create fields for the *raw variables*.
```json
{ "type": "number", "attribute": "data.prowessMV", "title": "Prowess MV" },
{ "type": "checkbox", "attribute": "data.hasAgilitySpecialty", "title": "Agility Spec?" }
```

### Step 3: Implement Calculations (Render/Helpers)
Encounter+ allows specific formatting helpers. Validating complex logic often requires a "result" field that guides the user, as raw JS execution inside the JSON is limited.

*   **Pattern**: Use `readonly` fields with descriptive `render` templates to show the user the calculated result based on their inputs.

```json
{
  "type": "readonly",
  "title": "Walk Speed (Squares)",
  "render": "Base: {{data.prowessMV}} + 12 / 5... see logic rules."
}
```
*Note: For fully automated math, the system relies on internal compiled scripts or specific `calculate` helpers if enabled in the build.*

---

## 6. Plyphyny-Specific Implementations

### A. Battle Phase Logic (The "Countdown")
*   **Input**: Prowess Die (`data.prowessDie`)
*   **Logic**: Map `d12` -> `Phase 1`, `d4` -> `Phase 5`.
*   **UI**: Use a `select` element for Prowess Die, and display the resulting Phase clearly in the Combatant Details.

### B. Movement Parity Logic
*   **Player vs. Monster**:
    *   **Players**: Check `data.speedFocus` for tier bonuses.
    *   **Monsters**: Apply tier bonuses automatically based on `data.prowessDie` (BP Die).
*   **Rounding**:
    *   `{{#if data.hasAgilitySpec}}Round Up{{else}}Round Down{{/if}}`

### C. Resource Cascades
*   **Defense**: Shield -> ADP -> Armor -> PDP -> HP.
*   **Implementation**: Ensure `config.json` lists all these pools so the Battle Tracker can display them (colors: Blue for ADP, Orange for PDP, Red for HP).

---

## 7. Best Practices for AI Coders

1.  **Preserve Structure**: Do not invent new root folders. Stick to `forms/` and `views/`.
2.  **Parity is King**: If a rule applies to PCs, check if it applies to NPCs. In Plyphyny, Movement and Phase logic must be identical.
3.  **Explicit Naming**: Use `data.attribute_name` consistent with the `config.json`.
4.  **Read-Only Verification**: Always provide a `readonly` field in the Form that shows the "derived" value of complex stats so the user can verify the math manualy if the automation isn't strict.

