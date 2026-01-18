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
└── views/               # JSON (native) or HTML (web) views
  ├── character.json   # Preferred for native rendering
  ├── character.html   # Optional HTML view (web renderer)
  ├── adversary.json
  ├── adversary.html
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

## 4. Display Views (`views/*.json` and `views/*.html`)

Views define how the entity looks when viewing its "Stat Block" or "Sheet". These are distinct from Forms.

Encounter+ supports **two renderers**:

1) **Native JSON views** (`views/*.json`) — preferred, stable, theme-aware
2) **HTML views** (`views/*.html`) — optional, rendered in a web view

**CRITICAL**: The native renderer expects a `"views"` array containing view component objects. It does **not** read external CSS.

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

### HTML Views (Optional)
HTML views are useful for complex layouts but require careful resource handling. If you use HTML:

* Include the base tag so assets resolve inside the bundled system:
```html
<base href="{{BASE_URL|default: '../'}}" />
```
* Prefer **inline CSS** inside the `<style>` tag to avoid path issues when the system is zipped.
* If you link CSS files, paths may fail in the app’s sandbox.

**Rule of Thumb:** If you only need color/style tweaks, prefer JSON views + themes. If you need advanced layout or CSS effects, use HTML + inline CSS.

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

### Styling JSON Views with Themes
If you want consistent color across native JSON views, use `themes/default.json`. Encounter+ reads theme keys such as:

* `tintColor`, `primaryColor`, `textColor`
* `bgColor`, `bgImage`
* `textStyles` (e.g., `title`, `title2`, `title3`, `subtitle`, `heading`)

**Example (theme snippet):**
```json
{
  "tintColor": "#55efc4",
  "primaryColor": "#5b2c6f",
  "textColor": "#ffffff",
  "bgColor": "#1a1625",
  "textStyles": {
    "title": { "color": "#55efc4", "size": 40 },
    "subtitle": { "color": "#a29bfe" }
  }
}
```

**Important:** JSON views only understand `style` keys that exist in the theme. If you invent a new style (e.g., `"item-title"`), it will render only if your theme defines it.

### View Naming & Case Sensitivity
The Encounter+ app matches entities to views based on the entity definition in `entities.json`. If your entity is named `"Adversary"`, the app may look for `views/Adversary.json` or `views/Adversary.html`.
* **Best Practice:** Make view filenames match the Entity Name exactly (including case).
* Example: For Entity `"Adversary"`, name the view `Adversary.html` (not `adversary.html`).

## 5. Styling Decision Matrix

Use this to decide which renderer to use:

**Use JSON Views + Theme when:**
* You want reliability and compatibility across devices.
* You only need colors, typography, and spacing.
* You can express the layout in `hStack`/`vStack`/`statBlock` components.
* **Pro Tip**: Use a custom `themes/default.json` with keys like `"item-title"`, `"race-trait"` to control colors globally.

**Use HTML Views + Inline CSS when:**
* You need complex layout, rich typography, glows, gradients, or custom spacing.
* You accept that external CSS (`<link href="...">`) may fail to load in a `.system` bundle due to sandboxing.
* **Requirement**: Use `<style>...</style>` blocks inside the HTML file itself for all CSS.
* **Requirement**: Include `<base href="{{BASE_URL|default: '../'}}" />` in the `<head>`.

**Rule:** If styling fails in HTML, fall back to JSON + theme first, then reintroduce HTML only where needed. Also, verify filename casing matches the Entity definition.

---

## 6. Content Injection & Data Prep

Views are empty without data. Ensure your JSON data files (`races.json`, `items.json`) are populated.

*   **Descriptions**: Fields like `descr` or `description` are often used in views. Creating entities with empty strings (`""`) will result in blank sections.
*   **Workflow**: Extract rich text from source documents (PDF/Markdown) and inject it into the `descr` field of the corresponding entity.
*   **Templating**: Use `{{descr|default: 'No description.'}}` in views to handle missing data gracefully.

---

## 7. Build & Packaging

To create a valid `.system` file:
1.  **Clean**: Remove development files (`.md`, `.ipynb`, `.txt`, `.jpg`) from the package.
2.  **Zip**: Compress the *contents* of your system folder (not the folder itself).
3.  **Rename**: Change the extension from `.zip` to `.system`.
4.  **Verify**: The root of the zip must contain `manifest.json`.

```bash
zip -r my-system.system * -x "*.md" -x "*.txt" -x "*.DS_Store"
```

---

## 8. Implementing Deterministic Mechanics (AI Workflow)

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

## 9. Plyphyny-Specific Implementations

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

## 10. Developer Notes: HTML Webview Architecture (2026)

**Critical Update**: Based on official developer guidance, Encounter+ Beta v5 is transitioning from SwiftUI native views to HTML webviews due to performance issues in iOS 26. This fundamentally changes view development best practices.

### HTML Views Are Now Preferred

**Why HTML?** 
- Better memory management and caching compared to SwiftUI
- Full CSS and JavaScript support
- More flexible styling and layout options
- Avoids iOS 26 SwiftUI performance degradation

### Path Requirements for HTML Views

**DO NOT use `<base href>` tags** — This breaks path resolution in the webview sandbox.

**Correct Pattern:**
```html
<!doctype html>
<html lang="en" {{HTML_CLASS}}>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- NO BASE TAG -->
    <title>{{name}}</title>
    <style>
        /* Inline CSS or use simple relative paths */
    </style>
</head>
```

**Asset Path Strategies:**

1. **Inline CSS** (Recommended for bundled systems):
```html
<style>
    :root {
        --primary-color: #5b2c6f;
        --bg-color: #f5f0e8;
    }
    body { background: var(--bg-color); }
</style>
```

2. **Relative Paths** (if external CSS is needed):
```html
<link rel="stylesheet" href="assets/css/custom.css">
<!-- NOT: ../assets/css/custom.css -->
<!-- NOT: {{BASE_URL}}assets/css/custom.css -->
```

3. **System-Relative Paths** (for shared resources):
```html
<img src="systems/plyphyny/images/icon.png">
```

### Image Reference Migration

If images fail to load after import, use the **"Fix Image References"** tool in Encounter+ Settings → Advanced. This updates paths from old formats to the new webview-compatible structure.

### When to Use JSON vs HTML Views

| Use Case | Renderer | Rationale |
|----------|----------|-----------|
| **Complex layouts** with gradients, custom fonts, animations | HTML | Full CSS/JS support |
| **Simple stat blocks** with text and numbers | JSON | Faster rendering, smaller file size |
| **Theme-aware** content that adapts to user preferences | JSON | Uses `themes/default.json` for styling |
| **Richly styled** content with fixed aesthetic | HTML | Inline styles guarantee appearance |
| **Dynamic calculations** requiring JavaScript | HTML | Full scripting capability |

**Recommendation**: For new systems in 2026+, prefer HTML views with inline CSS. This provides the most control and best performance under the new architecture.

---

## 11. Best Practices for AI Coders

1.  **Preserve Structure**: Do not invent new root folders. Stick to `forms/` and `views/`.
2.  **Parity is King**: If a rule applies to PCs, check if it applies to NPCs. In Plyphyny, Movement and Phase logic must be identical.
3.  **Explicit Naming**: Use `data.attribute_name` consistent with the `config.json`.
4.  **Read-Only Verification**: Always provide a `readonly` field in the Form that shows the "derived" value of complex stats so the user can verify the math manualy if the automation isn't strict.
5.  **HTML Views First**: When creating views, use HTML with inline CSS unless the content is purely text-based. Avoid `<base href>` tags.
6.  **Test Path Resolution**: After creating HTML views, verify that assets load correctly. Use simple relative paths (`assets/css/file.css`) not absolute or liquid-tag paths.

