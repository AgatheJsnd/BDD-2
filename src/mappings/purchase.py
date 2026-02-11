"""
Module Purchase - Motif, Timing, Marques LVMH, Fréquence
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# MOTIF D'ACHAT (Restructuré: Offrir / Pour soi)
# ============================================================================

MOTIF_ADVANCED = {
    # Achat pour offrir
    "Cadeau": ["cadeau", "offrir", "pour ma", "pour mon", "surprise", "gift", "présent"],
    "Anniversaire": ["anniversaire", "birthday", "bday", "fêter", "30 ans", "40 ans", "50 ans"],
    "Mariage": ["mariage", "wedding", "mariée", "cérémonie", "fiançailles", "noces"],
    "Diplôme": ["diplôme", "graduation", "examen", "réussite", "promo", "fin d'études"],
    "Naissance": ["naissance", "birth", "bébé", "nouveau-né", "baby shower"],
    "Fetes": ["noël", "christmas", "saint-valentin", "valentine", "fête des mères", "fête des pères"],
    
    # Achat pour soi
    "Plaisir_personnel": ["pour moi", "me faire plaisir", "j'ai envie", "je me fais plaisir", "self-gift"],
    "Renouvellement": ["renouveler", "remplacer", "garde-robe", "wardrobe", "refresh"],
    "Evenement_special": ["événement", "event", "gala", "soirée", "occasion spéciale"],
    "Voyage": ["voyage", "vacances", "partir", "valise", "trip"],
    "Investissement": ["investissement", "investment", "pièce iconique", "iconic piece", "intemporel"]
}

# ============================================================================
# TIMING
# ============================================================================

TIMING_MAPPING = {
    "Urgent": [
        "urgent", "urgence", "vite", "rapidement", "quickly", "asap",
        "aujourd'hui", "today", "demain", "tomorrow", "cette semaine", "this week",
        "besoin maintenant", "need now", "immédiatement", "immediately"
    ],
    "Date_fixee": [
        "date fixée", "fixed date", "pour le", "avant le", "by",
        "dans 2 semaines", "in 2 weeks", "le mois prochain", "next month",
        "date précise", "specific date", "deadline"
    ],
    "Long_terme": [
        "long terme", "long term", "pas pressé", "no rush", "quand j'aurai trouvé",
        "je prends mon temps", "take my time", "projet", "project",
        "dans quelques mois", "in a few months"
    ]
}

# ============================================================================
# MARQUES LVMH
# ============================================================================

MARQUES_LVMH = {
    "Louis_Vuitton": [
        "louis vuitton", "lv", "vuitton", "monogram", "damier",
        "speedy", "neverfull", "keepall", "alma"
    ],
    "Dior": [
        "dior", "christian dior", "lady dior", "book tote", "saddle",
        "dior homme", "miss dior", "sauvage"
    ],
    "Gucci": [
        "gucci", "gg", "marmont", "dionysus", "jackie", "horsebit"
    ],
    "Loro_Piana": [
        "loro piana", "cachemire", "cashmere", "vicuña", "vicuna",
        "the suitcase", "textiles rares"
    ],
    "Bulgari": [
        "bulgari", "bvlgari", "serpenti", "b.zero1", "divas' dream",
        "haute joaillerie", "octo"
    ],
    "Givenchy": [
        "givenchy", "antigona", "gentleman", "l'interdit", "irresistible"
    ],
    "Tiffany": [
        "tiffany", "tiffany & co", "tiffany co", "blue box",
        "tiffany setting", "return to tiffany"
    ],
    "Celine": [
        "celine", "céline", "luggage", "trio", "classic bag", "phoebe philo"
    ],
    "Fendi": [
        "fendi", "baguette", "peekaboo", "ff logo", "zucca", "fourrure"
    ],
    "Sephora": [
        "sephora", "make-up", "makeup", "cosmétiques", "beauty", "beauté"
    ]
}

# ============================================================================
# FRÉQUENCE D'ACHAT
# ============================================================================

FREQUENCE_ACHAT = {
    "Reguliere": [
        "régulier", "regular", "souvent", "often", "fréquent", "frequent",
        "plusieurs fois par an", "several times a year", "tous les mois", "monthly"
    ],
    "Occasionnelle": [
        "occasionnel", "occasional", "de temps en temps", "sometimes",
        "une ou deux fois par an", "once or twice a year"
    ],
    "Rare": [
        "rare", "rarely", "rarement", "très peu", "exceptionnellement",
        "première fois", "first time"
    ]
}
