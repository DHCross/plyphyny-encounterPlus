/*
 * Plyphyny System - Custom Helpers for Encounter+
 * Version: 1.0.3
 * ----------------
 * Handlebars helpers and combat logic automation
 */

// ============================================
// BATTLE PHASE CALCULATION
// ============================================

/**
 * Calculates Battle Phase from Prowess Die value
 * Based on Prowess Die → Phase mapping:
 * d12 → Phase 1 (fastest)
 * d10 → Phase 2
 * d8  → Phase 3
 * d6  → Phase 4
 * d4  → Phase 5 (slowest)
 */
Handlebars.registerHelper('calculatePhase', function(prowessDie) {
    const phaseMap = {
        12: 1,
        10: 2,
        8: 3,
        6: 4,
        4: 5
    };
    return phaseMap[prowessDie] || 5; // Default to slowest if invalid
});

/**
 * Converts Prowess Die to descriptive position text
 */
Handlebars.registerHelper('calculatePhasePosition', function(prowessDie) {
    const positionMap = {
        12: 'first (Legendary)',
        10: 'second (Heroic)',
        8: 'third (Competent)',
        6: 'fourth (Average)',
        4: 'last (Slow)'
    };
    return positionMap[prowessDie] || 'last';
});

/**
 * Alternative: Calculate phase from Initiative Score
 * Score 12+ → Phase 1, 9-11 → Phase 2, 7-8 → Phase 3, 5-6 → Phase 4, 1-4 → Phase 5
 */
Handlebars.registerHelper('calculatePhaseFromScore', function(initiativeScore) {
    if (initiativeScore >= 12) return 1;
    if (initiativeScore >= 9) return 2;
    if (initiativeScore >= 7) return 3;
    if (initiativeScore >= 5) return 4;
    return 5;
});

/**
 * Calculate total initiative score from components
 */
Handlebars.registerHelper('calculateInitiative', function(prowessMV, reactionFocus, finesseFocus) {
    return (prowessMV || 0) + (reactionFocus || 0) + (finesseFocus || 0);
});

// ============================================
// DEFENSE CASCADE HELPERS
// ============================================

/**
 * Calculate defense layer color for visual indicators
 */
Handlebars.registerHelper('defenseLayerColor', function(layer) {
    const colors = {
        'shield': '#95a5a6',     // Gray
        'adp': '#4287f5',        // Blue
        'armor': '#7f8c8d',      // Dark gray
        'pdp': '#e67e22',        // Orange
        'hp': '#e74c3c'          // Red
    };
    return colors[layer] || '#000000';
});

/**
 * Calculate defense percentage for progress bars
 */
Handlebars.registerHelper('defensePercent', function(current, max) {
    if (!max || max === 0) return 0;
    return Math.round((current / max) * 100);
});

/**
 * Check if defense layer is depleted
 */
Handlebars.registerHelper('isDepleted', function(current) {
    return current <= 0;
});

/**
 * Check if defense layer is critical (below 25%)
 */
Handlebars.registerHelper('isCritical', function(current, max) {
    if (!max || max === 0) return false;
    return (current / max) < 0.25;
});

// ============================================
// THREAT DICE HELPERS
// ============================================

/**
 * Parse and roll threat dice notation (e.g., "3d8", "2d6+2")
 */
Handlebars.registerHelper('rollThreatDice', function(notation) {
    // Parse notation like "3d8" or "2d6+2"
    const match = notation.match(/^(\d+)d(\d+)(?:\+(\d+))?$/);
    if (!match) return 0;
    
    const count = parseInt(match[1]);
    const sides = parseInt(match[2]);
    const bonus = parseInt(match[3] || 0);
    
    let total = bonus;
    for (let i = 0; i < count; i++) {
        total += Math.floor(Math.random() * sides) + 1;
    }
    
    return total;
});

/**
 * Apply threat damage through defense cascade
 * Returns object with how damage was distributed
 */
function applyThreatDamage(threat, shield, adpCurrent, armor, pdpCurrent) {
    let remaining = threat;
    const result = {
        shieldReduced: 0,
        adpDamage: 0,
        armorReduced: 0,
        pdpDamage: 0,
        hpDamage: 0
    };
    
    // Layer 1: Shield (fixed reduction)
    if (shield > 0 && remaining > 0) {
        result.shieldReduced = Math.min(shield, remaining);
        remaining -= result.shieldReduced;
    }
    
    // Layer 2: Active Defense Pool
    if (adpCurrent > 0 && remaining > 0) {
        result.adpDamage = Math.min(adpCurrent, remaining);
        remaining -= result.adpDamage;
    }
    
    // Layer 3: Armor (roll reduction)
    if (armor > 0 && remaining > 0) {
        const armorRoll = Math.floor(Math.random() * armor) + 1;
        result.armorReduced = Math.min(armorRoll, remaining);
        remaining -= result.armorReduced;
    }
    
    // Layer 4: Passive Defense Pool
    if (pdpCurrent > 0 && remaining > 0) {
        result.pdpDamage = Math.min(pdpCurrent, remaining);
        remaining -= result.pdpDamage;
    }
    
    // Layer 5: Hit Points (final layer)
    if (remaining > 0) {
        result.hpDamage = remaining;
    }
    
    return result;
}

// ============================================
// REACH & CLASSIFICATION HELPERS
// ============================================

/**
 * Get reach priority for initiative sorting (lower = acts earlier)
 */
Handlebars.registerHelper('reachPriority', function(reach) {
    const priority = {
        'Long Range': 1,
        'Long Reach': 2,
        'Medium Reach': 3,
        'Short Reach': 4,
        'None': 5
    };
    return priority[reach] || 5;
});

/**
 * Get heroic tier priority for initiative sorting (lower = acts earlier)
 */
Handlebars.registerHelper('heroicTier', function(classification) {
    const tier = {
        'PC': 1,
        'Legendary': 1,
        'Exceptional': 2,
        'Standard': 3,
        'Minor': 4,
        'NPC': 4
    };
    return tier[classification] || 4;
});

// ============================================
// REVITALIZE HELPERS
// ============================================

/**
 * Calculate Invigorate recovery (roll Prowess die + Reaction Focus)
 */
Handlebars.registerHelper('calculateInvigorate', function(prowessDie, reactionFocus) {
    const roll = Math.floor(Math.random() * prowessDie) + 1;
    return roll + (reactionFocus || 0);
});

/**
 * Calculate Deep Recovery (guaranteed max die + Reaction Focus)
 */
Handlebars.registerHelper('calculateDeepRecovery', function(prowessDie, reactionFocus) {
    return prowessDie + (reactionFocus || 0);
});

/**
 * Calculate Steady Renewal (25% of max ADP + 10% per SP spent)
 */
Handlebars.registerHelper('calculateSteadyRenewal', function(maxADP, spSpent) {
    const baseRecovery = Math.floor(maxADP * 0.25);
    const bonusRecovery = Math.floor(maxADP * 0.10 * spSpent);
    return baseRecovery + bonusRecovery;
});

// ============================================
// STATUS & CONDITION HELPERS
// ============================================

/**
 * Determine combat status based on defense pools
 */
Handlebars.registerHelper('combatStatus', function(hp, adpCurrent, pdpCurrent) {
    if (hp <= 0) return 'DEFEATED';
    if (adpCurrent <= 0 && pdpCurrent <= 0) return 'Critically Vulnerable';
    if (adpCurrent <= 0) return 'Vulnerable (ADP depleted)';
    if (pdpCurrent <= 0) return 'Fatigued (PDP depleted)';
    return 'Combat Ready';
});

/**
 * Format default value if field is empty
 */
Handlebars.registerHelper('default', function(value, defaultValue) {
    return value || defaultValue;
});

// ============================================
// UTILITY HELPERS
// ============================================

/**
 * Simple equality check for conditionals
 */
Handlebars.registerHelper('eq', function(a, b) {
    return a === b;
});

/**
 * Greater than check
 */
Handlebars.registerHelper('gt', function(a, b) {
    return a > b;
});

/**
 * Less than check
 */
Handlebars.registerHelper('lt', function(a, b) {
    return a < b;
});

/**
 * Greater than or equal
 */
Handlebars.registerHelper('gte', function(a, b) {
    return a >= b;
});

/**
 * Less than or equal
 */
Handlebars.registerHelper('lte', function(a, b) {
    return a <= b;
});

/**
 * Logical AND
 */
Handlebars.registerHelper('and', function(a, b) {
    return a && b;
});

/**
 * Logical OR
 */
Handlebars.registerHelper('or', function(a, b) {
    return a || b;
});

console.log('Plyphyny System helpers loaded successfully');
