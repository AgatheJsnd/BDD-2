"""
Module Preferences - Régime, Allergies, Valeurs
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# RÉGIME ALIMENTAIRE
# ============================================================================

REGIME_MAPPING = {
    "Vegan": [
        "vegan", "végane", "végan", "100% végétal", "plant-based",
        "sans produits animaux", "no animal products"
    ],
    "Vegetarien": [
        "végétarien", "vegetarian", "veggie", "sans viande", "no meat"
    ],
    "Pescetarien": [
        "pescétarien", "pescetarian", "poisson mais pas viande",
        "fish but no meat"
    ],
    "Sans_gluten": [
        "sans gluten", "gluten-free", "intolérant gluten", "gluten intolerant",
        "coeliaque", "celiac"
    ],
    "Sans_lactose": [
        "sans lactose", "lactose-free", "intolérant lactose",
        "lactose intolerant"
    ],
    "Aucun": [
        "aucun régime", "no diet", "mange de tout", "eat everything",
        "pas de restriction", "no restriction"
    ]
}

# ============================================================================
# ALLERGIES
# ============================================================================

ALLERGIES_MAPPING = {
    # Alimentaires
    "Gluten": ["allergie gluten", "gluten allergy", "coeliaque"],
    "Lactose": ["allergie lactose", "lactose allergy", "intolérance lait"],
    "Fruits_coque": ["fruits à coque", "nuts", "noix", "amandes", "noisettes", "nut allergy"],
    "Arachides": ["arachide", "peanut", "cacahuète"],
    
    # Cutanées
    "Nickel": ["allergie nickel", "nickel allergy", "sensible nickel"],
    "Latex": ["allergie latex", "latex allergy"],
    "Parfums": ["allergie parfum", "fragrance allergy", "sensible parfums", "fragrance sensitive"],
    "Colorants": ["allergie colorants", "dye allergy", "colorants textiles"],
    "Laine": ["allergie laine", "wool allergy", "sensible laine"],
    "Synthetiques": ["allergie synthétiques", "synthetic allergy"],
    
    "Aucune": ["aucune allergie", "no allergy", "pas d'allergie"]
}

# ============================================================================
# VALEURS
# ============================================================================

VALEURS_MAPPING = {
    # Éthique / Durable
    "Production_responsable": [
        "production responsable", "responsible production", "éthique",
        "ethical", "commerce équitable", "fair trade"
    ],
    "Eco_responsable": [
        "éco-responsable", "eco-friendly", "durable", "sustainable",
        "environnement", "environment", "green"
    ],
    "Bien_etre_animal": [
        "bien-être animal", "animal welfare", "sans cruauté", "cruelty-free",
        "pas de fourrure", "no fur", "vegan"
    ],
    "Engagement_social": [
        "engagement social", "social commitment", "impact social",
        "social impact", "responsabilité sociale"
    ],
    
    # Qualité & Savoir-faire
    "Artisanat": [
        "artisanat", "craftsmanship", "fait main", "handmade",
        "savoir-faire", "artisan"
    ],
    "Made_in": [
        "made in france", "made in europe", "made in italy",
        "fabrication française", "fabrication européenne"
    ],
    "Durabilite": [
        "durable", "durability", "qualité", "quality", "longue durée",
        "long-lasting", "intemporel"
    ],
    
    # Exclusivité
    "Serie_limitee": [
        "série limitée", "limited edition", "édition limitée",
        "limited series", "exclusif"
    ],
    "Sur_mesure": [
        "sur mesure", "bespoke", "custom", "made to measure",
        "personnalisé", "customized"
    ],
    "Rare": [
        "rare", "pièce rare", "rare piece", "unique", "exclusif",
        "exclusive"
    ]
}
