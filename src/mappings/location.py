"""
Module Location - Détection géographique enrichie
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# LOCALISATION AVANCÉE (Régions + Villes détaillées)
# ============================================================================

CITIES_ADVANCED = {
    # Europe
    "europe": {
        "Paris": ["paris", "parisien", "parisienne", "île-de-france", "idf"],
        "Berlin": ["berlin", "berlinois", "allemagne"],
        "Milan": ["milan", "milano", "milanais", "lombardie"],
        "Madrid": ["madrid", "madrilène", "espagne"],
        "London": ["london", "londres", "londonien", "uk", "royaume-uni"],
        "Lyon": ["lyon", "lyonnais", "rhône"],
        "Barcelona": ["barcelona", "barcelone", "barcelonais", "catalogne"],
        "Rome": ["rome", "roma", "romain", "italie"],
        "Amsterdam": ["amsterdam", "amsterdamois", "pays-bas", "netherlands"],
        "Bruxelles": ["bruxelles", "brussels", "bruxellois", "belgique"],
        "Munich": ["munich", "münchen", "munichois", "bavière"],
        "Genève": ["genève", "geneva", "genevois", "suisse"],
        "Zurich": ["zurich", "zürich", "zurichois", "suisse"],
        "Monaco": ["monaco", "monégasque", "monte-carlo"]
    },
    
    # Amérique
    "amerique": {
        "New York": ["new york", "ny", "nyc", "manhattan", "brooklyn", "new-yorkais"],
        "Los Angeles": ["los angeles", "la", "hollywood", "beverly hills", "californie"],
        "Miami": ["miami", "florida", "floride", "south beach"],
        "Toronto": ["toronto", "torontois", "canada", "ontario"],
        "Montreal": ["montreal", "montréal", "montréalais", "québec"],
        "Chicago": ["chicago", "illinois", "chicagoan"],
        "San Francisco": ["san francisco", "sf", "bay area", "silicon valley"],
        "Boston": ["boston", "massachusetts", "bostonien"]
    },
    
    # Moyen-Orient / Asie
    "moyen_orient_asie": {
        "Dubai": ["dubai", "dubaï", "émirats", "uae", "emirates"],
        "Tokyo": ["tokyo", "tōkyō", "tokyoïte", "japon"],
        "Hong Kong": ["hong kong", "hongkong", "hk"],
        "Singapore": ["singapore", "singapour", "singaporien"],
        "Shanghai": ["shanghai", "shanghaï", "chine"],
        "Doha": ["doha", "qatar", "qatari"],
        "Abu Dhabi": ["abu dhabi", "abou dhabi", "émirats"],
        "Seoul": ["seoul", "séoul", "corée", "korea"],
        "Beijing": ["beijing", "pékin", "peking", "chine"]
    },
    
    # Afrique
    "afrique": {
        "Maroc": ["maroc", "morocco", "marocain", "casablanca", "marrakech", "rabat"],
        "Tunisie": ["tunisie", "tunisia", "tunisien", "tunis"],
        "Algérie": ["algérie", "algeria", "algérien", "alger"],
        "Égypte": ["égypte", "egypt", "égyptien", "le caire", "cairo"],
        "Afrique du Sud": ["afrique du sud", "south africa", "johannesburg", "cape town"],
        "Nigeria": ["nigeria", "nigérian", "lagos"],
        "Kenya": ["kenya", "kenyan", "nairobi"],
        "Casablanca": ["casablanca", "casa", "casablancais"],
        "Marrakech": ["marrakech", "marrakesh", "marrakchi"]
    }
}
