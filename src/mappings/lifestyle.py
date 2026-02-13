"""
Module Lifestyle - Sport, Musique, Animaux, Voyage, Art & Culture, Gastronomie
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# SPORT (Restructuré: Collectif / Individuel)
# ============================================================================

SPORT_MAPPING = {
    # Sports Collectifs
    "Football": ["football", "foot", "soccer", "fifa", "champion", "ligue"],
    "Handball": ["handball", "hand"],
    "Basketball": ["basketball", "basket", "nba"],
    "Volleyball": ["volleyball", "volley"],
    "Hockey": ["hockey", "nhl"],
    "Rugby": ["rugby", "ovale"],
    
    # Sports de Raquette
    "Tennis": ["tennis", "roland garros", "wimbledon", "us open"],
    "Padel": ["padel"],
    "Squash": ["squash"],
    "Badminton": ["badminton"],
    
    # Sports Outdoor
    "Golf": ["golf", "golfeur", "club", "green"],
    "Ski": ["ski", "skiing", "montagne", "alpes", "station"],
    "Surf": ["surf", "surfing", "vague", "planche"],
    "Escalade": ["escalade", "climbing", "grimper", "varappe"],
    "Randonnée": ["randonnée", "hiking", "trek", "trekking", "marche"],
    
    # Sports Bien-être
    "Yoga": ["yoga", "yogi", "asana"],
    "Pilates": ["pilates"],
    "Méditation": ["méditation", "meditation", "mindfulness", "pleine conscience"],
    
    # Sports Endurance
    "Running": ["running", "course", "jogging", "marathon", "semi", "trail"],
    "Cyclisme": ["cyclisme", "vélo", "cycling", "bike", "tour de france"],
    "Natation": ["natation", "swimming", "nage", "piscine"],
    
    # Fitness / Musculation
    "Fitness": ["fitness", "gym", "musculation", "crossfit", "bodybuilding", "salle de sport"],
    
    # Sports Mécaniques
    "Formule_1": ["formule 1", "f1", "grand prix", "course automobile"],
    "Moto_GP": ["moto gp", "motogp", "moto", "motard"],
    "Rallye": ["rallye", "rally", "wrc"]
}

# ============================================================================
# MUSIQUE
# ============================================================================

MUSIQUE_MAPPING = {
    # Classique & Élégant
    "Classique": ["classique", "classical", "symphonie", "orchestre", "philharmonie"],
    "Opéra": ["opéra", "opera", "soprano", "ténor"],
    "Instrumentale": ["instrumentale", "instrumental", "piano", "violon", "guitare classique"],
    
    # Moderne & Populaire
    "Pop": ["pop", "pop music", "chanson"],
    "Rock": ["rock", "rock'n'roll", "metal", "punk"],
    "Hip_hop": ["hip-hop", "hip hop", "rap", "rapper", "mc"],
    "RnB": ["r&b", "rnb", "rhythm and blues", "soul music"],
    
    # Électronique
    "Electro": ["electro", "électro", "edm", "electronic"],
    "House": ["house", "deep house", "tech house"],
    "Techno": ["techno", "techno music", "rave"],
    
    # Jazz & Soul
    "Jazz": ["jazz", "be-bop", "swing"],
    "Soul": ["soul", "motown"],
    "Blues": ["blues", "rhythm and blues"],
    
    # Ambiance
    "Chill": ["chill", "chillout", "relax music"],
    "Lounge": ["lounge", "lounge music", "ambient"],
    "Lo_fi": ["lo-fi", "lofi", "lo fi"],
    
    # Musique du Monde
    "Latine": ["latine", "latin", "salsa", "reggaeton", "bachata"],
    "Africaine": ["africaine", "afrobeat", "african music"],
    "Asiatique": ["asiatique", "k-pop", "j-pop", "asian music"]
}

# ============================================================================
# ANIMAUX
# ============================================================================

ANIMAUX_MAPPING = {
    # Domestiques
    "Chien": ["chien", "dog", "canin", "toutou", "chiot", "puppy"],
    "Chat": ["chat", "cat", "félin", "chaton", "kitten"],
    "Cheval": ["cheval", "horse", "équitation", "équestre", "poney"],
    "Oiseaux": ["oiseau", "bird", "perroquet", "canari"],
    
    # Exotiques
    "Reptiles": ["reptile", "serpent", "snake", "lézard", "tortue"],
    "Poissons": ["poisson", "fish", "aquarium", "poisson rouge"],
    
    # Aucun
    "Aucun": ["pas d'animal", "no pet", "sans animal", "aucun animal"]
}

# ============================================================================
# VOYAGE (Enrichi)
# ============================================================================

VOYAGE_MAPPING = {
    # Type d'expérience
    "Voyage_luxe": ["voyage de luxe", "luxury travel", "first class", "classe affaires", "business class", "jet privé", "private jet"],
    "Aventure": ["aventure", "adventure", "safari", "exploration", "trek"],
    "Culturel": ["culturel", "cultural", "patrimoine", "heritage", "musée", "visite guidée"],
    "Détente": ["détente", "relaxation", "spa", "wellness", "repos"],
    "Road_trip": ["road trip", "roadtrip", "route", "van life"],
    "City_trip": ["city trip", "citybreak", "week-end", "escapade urbaine"],
    
    # Style de séjour
    "Hotel_5_etoiles": ["hôtel 5 étoiles", "5 star hotel", "palace", "grand hotel", "luxury hotel"],
    "Resort": ["resort", "club", "all inclusive"],
    "Villa_privee": ["villa privée", "private villa", "location villa"],
    "Croisiere": ["croisière", "cruise", "bateau", "yacht"],
    
    # Préférence destination
    "Plage": ["plage", "beach", "mer", "océan", "bord de mer", "seaside"],
    "Montagne": ["montagne", "mountain", "alpes", "ski resort"],
    "Desert": ["désert", "desert", "dunes", "sahara"],
    "Nature": ["nature", "forêt", "forest", "jungle", "wildlife"],
    "Ville": ["ville", "city", "urbain", "urban", "métropole"],
    
    # Fréquence
    "Voyageur_frequent": ["voyage souvent", "voyager", "voyage", "travel often", "frequent flyer", "plusieurs fois par an", "nomade"],
    "Occasionnel": ["voyage occasionnel", "occasional travel", "une ou deux fois par an"],
    "Rare": ["voyage rare", "rarely travel", "peu de voyages"]
}

# ============================================================================
# ART & CULTURE
# ============================================================================

ART_CULTURE_MAPPING = {
    # Arts visuels
    "Peinture": ["peinture", "painting", "tableau", "toile", "artiste peintre"],
    "Sculpture": ["sculpture", "sculpteur", "sculptor", "statue"],
    "Photographie": ["photographie", "photography", "photo", "photographe"],
    "Art_contemporain": ["art contemporain", "contemporary art", "installation", "performance"],
    
    # Lieux culturels
    "Musees": ["musée", "museum", "exposition", "exhibition", "galerie"],
    "Monuments": ["monument", "patrimoine", "heritage", "site historique"],
    
    # Spectacles
    "Theatre": ["théâtre", "theater", "pièce de théâtre", "comédie", "tragédie"],
    "Danse": ["danse", "dance", "ballet", "chorégraphie"],
    "Concerts": ["concert", "spectacle", "live", "scène"],
    
    # Cinéma & Littérature
    "Cinema": ["cinéma", "cinema", "film", "movie", "festival"],
    "Lecture": ["lecture", "reading", "livre", "book", "roman", "littérature"],
    
    # Mode
    "Defiles": ["défilé", "fashion show", "fashion week", "runway"],
    "Createurs": ["créateur", "designer", "couturier", "maison de couture"],
    "Tendances": ["tendance", "trend", "mode", "fashion"]
}

# ============================================================================
# GASTRONOMIE
# ============================================================================

GASTRONOMIE_MAPPING = {
    # Type de cuisine
    "Fine_dining": ["fine dining", "gastronomie", "haute cuisine", "restaurant gastronomique"],
    "Cuisine_locale": ["cuisine locale", "local food", "terroir", "produits locaux"],
    "Cuisine_monde": ["cuisine du monde", "world cuisine", "international", "fusion"],
    "Street_food": ["street food", "food truck", "marché"],
    
    # Boissons
    "Vins": ["vin", "wine", "sommelier", "cave", "dégustation", "grand cru"],
    "Champagnes": ["champagne", "champagnes", "bulles", "moët", "dom pérignon"],
    "Spiritueux": ["spiritueux", "spirits", "whisky", "cognac", "rhum", "vodka"],
    "Cocktails": ["cocktail", "mixologie", "mixology", "bar"],
    
    # Expériences
    "Etoile_michelin": ["étoilé", "michelin", "étoile", "chef étoilé", "restaurant étoilé"],
    "Diner_prive": ["dîner privé", "private dining", "chef à domicile"],
    "Cours_cuisine": ["cours de cuisine", "cooking class", "atelier culinaire"],
    
    # Préférences
    "Traditionnelle": ["traditionnel", "traditional", "classique", "authentique"],
    "Legere": ["léger", "light", "équilibré", "healthy", "sain"]
}
