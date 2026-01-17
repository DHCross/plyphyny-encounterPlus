# Eldritch RPG / Plyphyny System Architecture

This document explains how the Encounter+ system module is built and how all the components work together.

## File Structure Overview

```
plyphyny_It2X/
├── system.json          # System metadata (name, version, author)
├── config.json          # Combat bars, initiative mode, entity roles
├── entities.json        # Entity type definitions (Hero, Monster, Item, Spell, Race)
├── types.json           # Picker/dropdown value definitions
├── filters.json         # Search/filter configurations
├── manual.md            # Rules reference documentation
├── instructions.md      # Quick start guide
├── forms/               # Data entry forms (JSON)
│   ├── hero.json        # Player character sheet with calculated attributes
│   ├── monster.json     # QSB stat block form
│   ├── item.json        # Equipment/magic items
│   ├── spell.json       # Spell definitions
│   └── race.json        # Playable race definitions
├── views/               # Display templates (JSON/MD)
│   ├── hero.json        # Character sheet view
│   ├── monster.json     # Monster stat block view
│   ├── item.json        # Item card view
│   ├── spell.json       # Spell card view
│   └── partials/        # Reusable view components
├── themes/              # Visual styling
│   └── default.json     # Colors, fonts, backgrounds
├── lang/                # Localization
│   └── en.json          # English translations
├── icons/               # Entity type icons
├── images/              # Background images
├── resources/           # Token images
│   ├── heroes/          # PC token assets
│   └── monsters/        # Monster token assets
├── heroes.json          # Pre-made hero data
├── monsters.json        # Bestiary data
├── items.json           # Equipment data
├── spells.json          # Spell compendium
└── races.json           # Playable race data
```

## Core Components

### 1. system.json
Defines the system identity:
```json
{
  "name": "Eldritch RPG",
  "slug": "eldritch-rpg",
  "version": "2.0",
  "author": "Your Name"
}
```

### 2. entities.json
Defines the data types available in the system:
```json
[
  {
    "name": "Hero",
    "label": "hero",
    "collection": { "label": "heroes" },
    "loadable": true,
    "role": "friendly"
  },
  {
    "name": "Monster",
    "label": "monster",
    "collection": { "label": "monsters" },
    "loadable": true,
    "role": "enemy"
  }
]
```

**Key Properties:**
- `name`: Display name
- `label`: Internal identifier (lowercase)
- `collection.label`: Filename for data (e.g., `heroes.json`)
- `loadable`: Can be added to encounters
- `role`: Combat role (`friendly`, `enemy`, `neutral`)

### 3. config.json
Configures combat automation:
```json
{
  "entities": {
    "Default": {
      "combatant": {
        "bars": [
          { "attribute": "data.ad_current", "title": "Active Defense", "label": "AD" },
          { "attribute": "hp", "title": "Passive Defense", "label": "PD" },
          { "attribute": "data.sp_current", "title": "Spirit Points", "label": "SP" }
        ]
      }
    },
    "Hero": { "role": "friendly" },
    "Monster": { "role": "enemy" }
  },
  "combat": {
    "initiative": {
      "mode": "fixed",
      "attribute": "data.initiative"
    }
  }
}
```

**Initiative Modes:**
- `"fixed"`: Uses a pre-calculated attribute value
- `"roll"`: Rolls dice for each combatant

### 4. forms/ (Data Entry)
JSON files defining input forms. Each form has `sections` containing `fields`:

```json
{
  "sections": [
    {
      "title": "Basic Info",
      "type": "group",
      "fields": [
        { "title": "Name", "attribute": "name" },
        { "title": "Level", "type": "number", "attribute": "data.level" },
        { "type": "picker", "attribute": "data.class", "attributeType": "HeroClass" }
      ]
    }
  ],
  "attributes": {
    "data.movement": "Math.floor((12 + data.prowessdie + data.agilitydie) / 5)",
    "data.initiative": "data.prowessdie + (data.init_mod || 0)"
  }
}
```

**Field Types:**
- `text` (default): Single line input
- `textArea`: Multi-line input
- `number`: Numeric input
- `picker`: Dropdown from `types.json`
- `stepper`: +/- Numeric control
- `progress`: Progress bar
- `reference`: Link to another entity

**Calculated Attributes:**
The `attributes` block defines formulas that auto-calculate values based on other fields. Uses JavaScript expressions.

### 5. views/ (Display Templates)
JSON files defining how entities appear when viewed:

```json
{
  "spacing": 8,
  "padding": [12],
  "views": [
    {
      "type": "hStack",
      "views": [
        { "value": "**{{name}}**", "style": "title" },
        { "type": "image", "value": "{{token}}", "height": 60 }
      ]
    },
    {
      "type": "text",
      "value": "**HP:** {{data.hp}} | **AD:** {{data.ad}}"
    }
  ]
}
```

**View Types:**
- `text`: Markdown-rendered text
- `image`: Image display
- `hStack`/`vStack`: Horizontal/Vertical layout
- `divider`: Separator line
- `list`: Repeating items

**Template Variables:**
- `{{name}}`: Entity name
- `{{data.fieldname}}`: Form data
- `{{token}}`: Token image path
- `{{'Key'|l}}`: Localized string

### 6. types.json (Pickers/Dropdowns)
Defines options for picker fields:

```json
{
  "HeroClass": {
    "adept": "Class.Adept",
    "assassin": "Class.Assassin",
    "barbarian": "Class.Barbarian"
  },
  "Rarity": {
    "common": "Rarity.Common",
    "uncommon": "Rarity.Uncommon",
    "esoteric": "Rarity.Esoteric"
  }
}
```

### 7. lang/en.json (Localization)
Maps translation keys to display text:

```json
{
  "Entity.Hero": "Hero",
  "Entity.Hero.many": "Heroes",
  "Class.Adept": "Adept",
  "Class.Assassin": "Assassin",
  "Rarity.Common": "Common"
}
```

### 8. themes/default.json (Styling)
Controls visual appearance:

```json
{
  "tintColor": "#58180D",
  "primaryColor": "#9C2B1B",
  "textColor": "#000000",
  "bgImage": "/images/paper.png",
  "styles": {
    "title": { "font": "HoeflerText-Regular", "color": "#58180D", "size": 30 },
    "body": { "font": "NotoSans", "size": 15 }
  }
}
```

## Data Flow

```
User Input (forms/) 
    ↓
Raw Data (heroes.json, monsters.json)
    ↓
Calculated Attributes (forms/.attributes)
    ↓
Display (views/)
    ↓
Combat (config.json → initiative, bars)
```

## Combat Integration

### Battle Phases → Initiative
Eldritch uses Battle Phases (5 → 1) instead of rolled initiative. In Encounter+:
1. `data.initiative` is calculated from Prowess + Init Mod
2. `config.json` uses `"mode": "fixed"` with `"attribute": "data.initiative"`
3. Higher scores act first (Phase 1 gets higher initiative value)

### Combat Bars
Three defense pools display on tokens:
- **AD (Active Defense)**: `data.ad_current`
- **PD (Passive Defense)**: `hp` (built-in)
- **SP (Spirit Points)**: `data.sp_current`

## Packaging

To create an installable module:
```bash
zip -r plyphyny.zip plyphyny_It2X -x "*.DS_Store"
```

Rename to `.encounter` extension if needed, or import directly as `.zip` in Encounter+.

## Comparison with D&D 5e Systems

| Feature | D&D 5e (XML) | Eldritch (JSON System) |
|---------|--------------|------------------------|
| Stats | STR, DEX, CON, INT, WIS, CHA | Competence, Prowess, Fortitude (+ Specialties + Focuses) |
| HP | Single pool | AD + PD + Armor stacking |
| Initiative | d20 + DEX mod | Fixed Battle Phase (d4–d12) |
| Attacks | To-hit + Damage | Threat Points vs Defense Stack |
| Data Format | XML `<monster>` tags | JSON forms + calculated attributes |

## Advanced Features

### Conditional Display
Show fields only when conditions are met:
```json
{
  "title": "Spell Focus",
  "attribute": "data.spellfocus",
  "visibleIf": "data.gift_of_magic == true"
}
```

### Form Partials
Reusable form components in `forms/partials/`:
```json
{
  "type": "form",
  "form": { "partial": "ability-scores" }
}
```

### View Partials
Reusable view templates in `views/partials/`:
```json
{
  "type": "text",
  "value": "{% include 'monster-qsb.md' %}"
}
```
