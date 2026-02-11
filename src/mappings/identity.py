"""
Module Identity - Détection Genre, Langue, Statut, Profession
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# GENRE
# ============================================================================

GENRE_MAPPING = {
    "Femme": [
        "madame", "mme", "mademoiselle", "mlle", "elle", "sa femme", "ma femme",
        "mrs", "miss", "ms", "she", "her", "woman", "lady", "female",
        "je suis une", "en tant que femme", "cliente", "actrice", "mariée"
    ],
    "Homme": [
        "monsieur", "m.", "il", "son mari", "mon mari", "lui",
        "mr", "mister", "he", "him", "man", "gentleman", "male",
        "je suis un", "en tant qu'homme", "client", "acteur", "marié"
    ],
    "Autre": [
        "non-binaire", "non binaire", "genderfluid", "they", "them", "iel"
    ]
}

# ============================================================================
# LANGUE PARLÉE
# ============================================================================

LANGUE_MAPPING = {
    "Français": [
        "français", "french", "je parle français", "langue maternelle français",
        "francophone", "de france", "parisien", "lyonnais"
    ],
    "Anglais": [
        "anglais", "english", "i speak english", "native english", "anglophone",
        "from usa", "from uk", "american", "british", "australian"
    ],
    "Italien": [
        "italien", "italian", "italiano", "parlo italiano", "di milano",
        "di roma", "from italy", "italian speaker"
    ],
    "Espagnol": [
        "espagnol", "spanish", "español", "hablo español", "de madrid",
        "de barcelona", "from spain", "latin american"
    ],
    "Allemand": [
        "allemand", "german", "deutsch", "ich spreche deutsch", "von berlin",
        "from germany", "austrian", "swiss german"
    ],
    "Portugais": [
        "portugais", "portuguese", "português", "falo português", "brasileiro",
        "from brazil", "from portugal"
    ],
    "Arabe": [
        "arabe", "arabic", "عربي", "je parle arabe", "du moyen-orient",
        "from dubai", "from saudi", "maghrébin"
    ],
    "Russe": [
        "russe", "russian", "русский", "je parle russe", "de moscou",
        "from russia", "from ukraine"
    ],
    "Chinois": [
        "chinois", "chinese", "mandarin", "中文", "je parle chinois",
        "from china", "from beijing", "from shanghai"
    ],
    "Japonais": [
        "japonais", "japanese", "日本語", "je parle japonais",
        "from japan", "from tokyo"
    ],
    "Coréen": [
        "coréen", "korean", "한국어", "je parle coréen",
        "from korea", "from seoul"
    ],
    "Hindi": [
        "hindi", "हिन्दी", "je parle hindi", "from india", "indian"
    ]
}

# ============================================================================
# STATUT RELATIONNEL CLIENT
# ============================================================================

STATUT_MAPPING = {
    "VIP": [
        "vip", "client privilégié", "membre privilège", "carte noire",
        "top client", "meilleur client", "fidélité platine", "platinum member",
        "exclusive member", "private client", "invitation privée"
    ],
    "Fidèle": [
        "fidèle", "régulier", "habitué", "loyal", "depuis des années",
        "loyal customer", "regular customer", "returning customer",
        "carte de fidélité", "programme fidélité", "points fidélité"
    ],
    "Nouveau": [
        "nouveau", "première fois", "first time", "new customer", "découvrir",
        "jamais acheté", "never bought", "première visite", "first visit",
        "nouveau client", "nouvel arrivant"
    ],
    "Régulier": [
        "régulier", "de temps en temps", "occasionally", "sometimes",
        "plusieurs fois", "quelques achats", "few purchases"
    ],
    "Occasionnel": [
        "occasionnel", "rare", "rarement", "rarely", "occasionally",
        "une fois par an", "once a year", "special occasions only"
    ]
}

# ============================================================================
# PROFESSION ENRICHIE (avec sous-catégories)
# ============================================================================

PROFESSIONS_ADVANCED = {
    # Entrepreneur / Dirigeant
    "Entrepreneur": [
        "entrepreneur", "chef d'entreprise", "fondateur", "ceo", "business owner",
        "startup", "founder", "owner", "patron", "dirigeant", "co-founder"
    ],
    
    # Cadre / Manager
    "Cadre": [
        "cadre", "directeur", "manager", "responsable", "exécutif",
        "director", "executive", "vp", "vice president", "head of",
        "chief", "senior manager"
    ],
    
    # Profession libérale
    "Avocat": [
        "avocat", "lawyer", "attorney", "barrister", "solicitor",
        "juriste", "legal counsel"
    ],
    "Médecin": [
        "médecin", "doctor", "physician", "chirurgien", "surgeon",
        "généraliste", "spécialiste", "dermatologue", "cardiologue"
    ],
    "Architecte": [
        "architecte", "architect", "urbaniste", "urban planner"
    ],
    "Consultant": [
        "consultant", "consulting", "conseiller", "advisor", "expert"
    ],
    
    # Finance & Investissement
    "Banquier": [
        "banquier", "banker", "banque", "banking", "private banking"
    ],
    "Trader": [
        "trader", "trading", "bourse", "stock market", "forex"
    ],
    "Gestionnaire_patrimoine": [
        "gestionnaire de patrimoine", "wealth manager", "asset manager",
        "gestion de fortune", "family office"
    ],
    
    # Art & Création
    "Artiste": [
        "artiste", "artist", "peintre", "painter", "sculpteur", "sculptor"
    ],
    "Designer": [
        "designer", "créateur", "creator", "design", "créatif", "creative"
    ],
    "Photographe": [
        "photographe", "photographer", "photo", "photography"
    ],
    "Musicien": [
        "musicien", "musician", "compositeur", "composer", "dj"
    ],
    
    # Mode & Luxe
    "Styliste": [
        "styliste", "stylist", "fashion designer", "créateur de mode"
    ],
    "Acheteur_mode": [
        "acheteur", "buyer", "fashion buyer", "merchandiser"
    ],
    "Retail_luxe": [
        "retail", "vendeur luxe", "luxury retail", "boutique manager",
        "store manager"
    ],
    
    # Tech & Digital
    "Ingénieur": [
        "ingénieur", "engineer", "engineering", "technical"
    ],
    "Développeur": [
        "développeur", "developer", "programmeur", "programmer",
        "software engineer", "dev", "coder"
    ],
    "Data_IA": [
        "data scientist", "data analyst", "ai", "machine learning",
        "intelligence artificielle", "big data", "analytics"
    ],
    "Product_manager": [
        "product manager", "pm", "chef de produit", "product owner"
    ],
    
    # Médias & Communication
    "Journaliste": [
        "journaliste", "journalist", "reporter", "rédacteur", "editor",
        "presse", "media"
    ],
    "Marketing": [
        "marketing", "marketeur", "brand manager", "communication",
        "digital marketing", "social media manager"
    ],
    "Relations_publiques": [
        "relations publiques", "pr", "public relations", "attaché de presse",
        "press officer"
    ],
    
    # Sport
    "Athlète": [
        "athlète", "athlete", "sportif", "joueur professionnel",
        "professional player", "champion"
    ],
    "Coach": [
        "coach", "entraîneur", "trainer", "personal trainer",
        "coach sportif"
    ],
    "Dirigeant_sportif": [
        "dirigeant sportif", "sports director", "club manager",
        "agent sportif", "sports agent"
    ],
    
    # Autres
    "Étudiant": [
        "étudiant", "student", "école", "université", "stage",
        "stagiaire", "intern", "graduate", "phd", "master"
    ],
    "Retraité": [
        "retraité", "retired", "retraite", "retirement", "pension",
        "ancien", "former"
    ]
}
