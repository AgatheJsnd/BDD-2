"""
Extracteurs Contextuels — Extraction d'éléments actionnables depuis les transcriptions.
Détecte dates clés, produits possédés, projets de vie, demandes en attente, et affinités cross-maison.
"""
import re
from datetime import datetime, timedelta
from typing import Optional


# ============================================================================
# EXTRACTION DE DATES CLÉS
# ============================================================================

DATE_PATTERNS = {
    "anniversaire_epouse": [
        r"anniversaire\s+(?:de\s+)?(?:ma\s+)?(?:femme|épouse|conjointe)",
        r"birthday\s+(?:of\s+)?(?:my\s+)?wife",
    ],
    "anniversaire_mari": [
        r"anniversaire\s+(?:de\s+)?(?:mon\s+)?(?:mari|époux|conjoint)",
        r"birthday\s+(?:of\s+)?(?:my\s+)?husband",
    ],
    "anniversaire_enfant": [
        r"anniversaire\s+(?:de\s+)?(?:mon\s+fils|ma\s+fille|mon\s+enfant)",
        r"birthday\s+(?:of\s+)?(?:my\s+)?(?:son|daughter|child|kid)",
    ],
    "anniversaire_mariage": [
        r"anniversaire\s+(?:de\s+)?(?:notre\s+)?mariage",
        r"(?:wedding|marriage)\s+anniversary",
    ],
    "anniversaire_general": [
        r"(?:son|sa|leur|mon)\s+anniversaire",
        r"(?:pour\s+)?(?:un|l[' ])\s*anniversaire",
        r"birthday",
    ],
    "naissance": [
        r"naissance\s+(?:de\s+)?(?:mon|notre|son|sa)",
        r"(?:attend|enceinte|bébé|nouveau[- ]né|baby\s*shower)",
        r"birth\s+of",
    ],
    "mariage": [
        r"(?:notre|son|leur)\s+mariage",
        r"(?:se\s+)?(?:marier|fiancer)",
        r"(?:wedding|engagement|getting\s+married)",
    ],
    "noel": [
        r"(?:pour\s+)?noël",
        r"christmas",
    ],
    "saint_valentin": [
        r"saint[- ]valentin",
        r"valentine",
    ],
    "fete_meres": [
        r"fête\s+des\s+mères",
        r"mother'?s?\s+day",
    ],
    "fete_peres": [
        r"fête\s+des\s+pères",
        r"father'?s?\s+day",
    ],
    "diplome": [
        r"(?:diplôme|graduation|examen|réussite|fin\s+d'études)",
        r"(?:diploma|graduation|degree)",
    ],
}

# Patterns pour extraire des dates concrètes (jj/mm, mois + jour, etc.)
DATE_EXTRACT_PATTERNS = [
    # "le 12 mai", "le 3 décembre"
    (r"le\s+(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)", "fr"),
    # "12/05", "03/12"
    (r"(\d{1,2})[/\-](\d{1,2})", "numeric"),
    # "dans un mois", "dans 2 semaines"
    (r"dans\s+(\d+)\s+(mois|semaines?|jours?)", "relative"),
    # "le mois prochain", "la semaine prochaine"
    (r"(?:le\s+)?mois\s+prochain", "next_month"),
    (r"(?:la\s+)?semaine\s+prochaine", "next_week"),
]

MOIS_FR = {
    "janvier": 1, "février": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12
}


def extract_dates_cles(text: str, reference_date: datetime = None) -> list:
    """
    Extrait les dates clés mentionnées dans une transcription.
    
    Returns:
        list[dict]: [{type, label, date_str, date_estimee, confidence}]
    """
    if not text:
        return []
    
    ref = reference_date or datetime.now()
    text_lower = text.lower()
    results = []

    for date_type, patterns in DATE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                # Trouver la date associée
                date_str, date_estimee = _extract_nearby_date(text_lower, pattern, ref)
                results.append({
                    "type": date_type,
                    "label": date_type.replace("_", " ").title(),
                    "date_str": date_str,
                    "date_estimee": date_estimee,
                    "confidence": 0.9 if date_str else 0.5
                })
                break  # Un seul match par type

    return results


def _extract_nearby_date(text: str, trigger_pattern: str, ref: datetime) -> tuple:
    """Cherche une date concrète près du trigger."""
    match = re.search(trigger_pattern, text)
    if not match:
        return None, None
    
    # Chercher dans le contexte autour du match (±100 chars)
    start = max(0, match.start() - 100)
    end = min(len(text), match.end() + 100)
    context = text[start:end]
    
    for pattern, fmt in DATE_EXTRACT_PATTERNS:
        date_match = re.search(pattern, context)
        if date_match:
            if fmt == "fr":
                jour = int(date_match.group(1))
                mois = MOIS_FR.get(date_match.group(2), 1)
                annee = ref.year if mois >= ref.month else ref.year + 1
                try:
                    dt = datetime(annee, mois, jour)
                    return f"{jour:02d}/{mois:02d}", dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass
            elif fmt == "numeric":
                jour = int(date_match.group(1))
                mois = int(date_match.group(2))
                if 1 <= mois <= 12 and 1 <= jour <= 31:
                    annee = ref.year if mois >= ref.month else ref.year + 1
                    try:
                        dt = datetime(annee, mois, jour)
                        return f"{jour:02d}/{mois:02d}", dt.strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            elif fmt == "relative":
                nombre = int(date_match.group(1))
                unite = date_match.group(2)
                if "mois" in unite:
                    dt = ref + timedelta(days=nombre * 30)
                elif "semaine" in unite:
                    dt = ref + timedelta(weeks=nombre)
                else:
                    dt = ref + timedelta(days=nombre)
                return f"+{nombre} {unite}", dt.strftime("%Y-%m-%d")
            elif fmt == "next_month":
                dt = ref + timedelta(days=30)
                return "mois prochain", dt.strftime("%Y-%m-%d")
            elif fmt == "next_week":
                dt = ref + timedelta(weeks=1)
                return "semaine prochaine", dt.strftime("%Y-%m-%d")
    
    return None, None


# ============================================================================
# EXTRACTION DE PRODUITS POSSÉDÉS / MENTIONNÉS
# ============================================================================

PRODUITS_KEYWORDS = {
    "sac": ["sac", "bag", "pochette", "clutch", "tote", "besace", "cabas", "messenger"],
    "portefeuille": ["portefeuille", "wallet", "porte-monnaie", "card holder", "porte-cartes"],
    "ceinture": ["ceinture", "belt"],
    "chaussures": ["chaussures", "shoes", "souliers", "bottines", "boots", "mocassins", 
                   "loafers", "sneakers", "espadrilles", "sandales"],
    "montre": ["montre", "watch", "chrono", "chronographe"],
    "bijou": ["bijou", "jewelry", "bague", "ring", "collier", "necklace", "bracelet", 
              "boucles d'oreilles", "earrings", "pendentif"],
    "lunettes": ["lunettes", "glasses", "sunglasses", "optique"],
    "foulard": ["foulard", "scarf", "écharpe", "châle", "shawl", "carré"],
    "costume": ["costume", "suit", "blazer", "veste", "jacket"],
    "cravate": ["cravate", "tie", "noeud papillon", "bow tie"],
    "parfum": ["parfum", "perfume", "fragrance", "eau de toilette", "cologne"],
    "maroquinerie": ["maroquinerie", "leather goods", "porte-documents", "briefcase"],
    "pull": ["pull", "pullover", "sweater", "cachemire", "cashmere"],
    "manteau": ["manteau", "coat", "trench", "parka", "doudoune"],
    "robe": ["robe", "dress"],
    "chemise": ["chemise", "shirt", "blouse"],
}

MARQUES_KEYWORDS = {
    "Louis Vuitton": ["louis vuitton", "lv", "vuitton", "monogram", "damier", "speedy", "neverfull", "keepall", "alma"],
    "Dior": ["dior", "christian dior", "lady dior", "book tote", "saddle", "miss dior", "sauvage"],
    "Gucci": ["gucci", "gg", "marmont", "dionysus", "jackie"],
    "Loro Piana": ["loro piana", "vicuña", "vicuna"],
    "Bulgari": ["bulgari", "bvlgari", "serpenti", "b.zero1"],
    "Givenchy": ["givenchy", "antigona", "l'interdit"],
    "Tiffany": ["tiffany", "tiffany & co", "blue box"],
    "Celine": ["celine", "céline", "luggage", "classic bag"],
    "Fendi": ["fendi", "baguette", "peekaboo", "ff logo"],
    "Berluti": ["berluti", "alessandro"],
    "TAG Heuer": ["tag heuer", "carrera", "monaco", "aquaracer"],
    "Hublot": ["hublot", "big bang", "classic fusion"],
    "Zenith": ["zenith", "el primero", "defy"],
    "Dom Pérignon": ["dom pérignon", "dom perignon"],
    "Moët": ["moët", "moet", "moët & chandon"],
    "Ruinart": ["ruinart"],
    "Hennessy": ["hennessy", "cognac hennessy"],
    "Krug": ["krug", "champagne krug"],
    "Chaumet": ["chaumet", "joséphine"],
    "Fred": ["fred", "force 10"],
    "Rimowa": ["rimowa", "valise rimowa"],
    "Loewe": ["loewe", "puzzle bag"],
}

COULEURS_KEYWORDS = {
    "noir": ["noir", "black", "noire"],
    "blanc": ["blanc", "white", "blanche", "crème", "cream", "ivoire", "ivory"],
    "marron": ["marron", "brown", "camel", "cognac", "chocolat", "taupe", "beige", "tan"],
    "bleu": ["bleu", "blue", "marine", "navy", "indigo"],
    "rouge": ["rouge", "red", "bordeaux", "burgundy", "cerise", "carmin"],
    "vert": ["vert", "green", "olive", "kaki", "émeraude", "emerald"],
    "rose": ["rose", "pink", "fuchsia", "magenta"],
    "gris": ["gris", "grey", "gray", "anthracite", "charcoal"],
    "or": ["or", "gold", "doré", "golden"],
    "argent": ["argent", "silver", "argenté"],
}

MATIERES_KEYWORDS = {
    "cuir": ["cuir", "leather", "veau", "calf", "agneau", "lamb"],
    "toile": ["toile", "canvas", "monogram canvas"],
    "cachemire": ["cachemire", "cashmere", "vicuña"],
    "soie": ["soie", "silk"],
    "laine": ["laine", "wool", "tweed"],
    "coton": ["coton", "cotton", "denim", "jean"],
    "daim": ["daim", "suede", "nubuck"],
    "crocodile": ["crocodile", "croco", "alligator", "exotic"],
    "lin": ["lin", "linen"],
    "métal": ["métal", "metal", "acier", "steel", "titane", "titanium"],
}


def extract_produits_possedes(text: str) -> list:
    """
    Extrait les produits mentionnés avec leur marque, couleur et matière.
    
    Returns:
        list[dict]: [{produit, marque, couleur, matiere, contexte}]
    """
    if not text:
        return []
    
    text_lower = text.lower()
    results = []
    
    # Détecter produits
    produits_trouves = []
    for produit, keywords in PRODUITS_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                produits_trouves.append(produit)
                break
    
    # Détecter marques
    marques_trouvees = []
    for marque, keywords in MARQUES_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                marques_trouvees.append(marque)
                break
    
    # Détecter couleurs
    couleurs_trouvees = []
    for couleur, keywords in COULEURS_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                couleurs_trouvees.append(couleur)
                break
    
    # Détecter matières
    matieres_trouvees = []
    for matiere, keywords in MATIERES_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                matieres_trouvees.append(matiere)
                break
    
    # Combiner les infos
    if produits_trouves:
        for produit in produits_trouves:
            results.append({
                "produit": produit,
                "marque": marques_trouvees[0] if marques_trouvees else None,
                "couleur": couleurs_trouvees[0] if couleurs_trouvees else None,
                "matiere": matieres_trouvees[0] if matieres_trouvees else None,
            })
    elif marques_trouvees:
        # Marque mentionnée sans produit spécifique
        results.append({
            "produit": "non spécifié",
            "marque": marques_trouvees[0],
            "couleur": couleurs_trouvees[0] if couleurs_trouvees else None,
            "matiere": matieres_trouvees[0] if matieres_trouvees else None,
        })

    return results


# ============================================================================
# EXTRACTION DE PROJETS DE VIE (Voyages, Événements)
# ============================================================================

DESTINATIONS = {
    "Tokyo": ["tokyo", "japon", "japan"],
    "Paris": ["paris"],
    "Milan": ["milan", "milano", "italie"],
    "Londres": ["londres", "london", "angleterre"],
    "New York": ["new york", "nyc", "manhattan"],
    "Dubai": ["dubai", "dubaï", "émirats", "abu dhabi"],
    "Monaco": ["monaco", "monte carlo", "monte-carlo"],
    "Saint-Tropez": ["saint-tropez", "st tropez", "côte d'azur", "riviera"],
    "Courchevel": ["courchevel", "méribel", "val d'isère", "chamonix", "megève"],
    "Maldives": ["maldives"],
    "Marrakech": ["marrakech", "maroc", "morocco"],
    "Rome": ["rome", "roma"],
    "Los Angeles": ["los angeles", "la", "hollywood", "beverly hills"],
    "Hong Kong": ["hong kong"],
    "Singapour": ["singapour", "singapore"],
    "Genève": ["genève", "geneva", "suisse"],
}

EVENEMENTS = {
    "gala": ["gala", "soirée de gala", "charity event"],
    "mariage": ["mariage", "wedding", "cérémonie", "noces"],
    "cocktail": ["cocktail", "réception", "reception"],
    "diner_affaires": ["dîner d'affaires", "business dinner", "déjeuner d'affaires"],
    "vernissage": ["vernissage", "exposition", "exhibition", "opening"],
    "festival": ["festival", "cannes", "fashion week"],
    "voyage_affaires": ["voyage d'affaires", "business trip", "déplacement professionnel"],
    "vacances": ["vacances", "holiday", "holidays", "congés"],
}


def extract_projets_vie(text: str, reference_date: datetime = None) -> list:
    """
    Détecte les projets de vie : voyages planifiés, événements à venir.
    
    Returns:
        list[dict]: [{type, destination/evenement, timing, date_estimee}]
    """
    if not text:
        return []
    
    ref = reference_date or datetime.now()
    text_lower = text.lower()
    results = []
    
    # Chercher voyages
    for dest, keywords in DESTINATIONS.items():
        for kw in keywords:
            if kw in text_lower:
                timing = _extract_timing(text_lower)
                date_est = _estimate_date(timing, ref)
                results.append({
                    "type": "voyage",
                    "destination": dest,
                    "timing": timing,
                    "date_estimee": date_est,
                })
                break
    
    # Chercher événements
    for evt, keywords in EVENEMENTS.items():
        for kw in keywords:
            if kw in text_lower:
                timing = _extract_timing(text_lower)
                date_est = _estimate_date(timing, ref)
                results.append({
                    "type": "evenement",
                    "evenement": evt.replace("_", " ").title(),
                    "timing": timing,
                    "date_estimee": date_est,
                })
                break
    
    return results


def _extract_timing(text: str) -> Optional[str]:
    """Extrait un indicateur de timing depuis le texte."""
    timing_patterns = [
        (r"demain", "demain"),
        (r"cette semaine", "cette semaine"),
        (r"la semaine prochaine", "semaine prochaine"),
        (r"le mois prochain", "mois prochain"),
        (r"dans (\d+) (jours?|semaines?|mois)", None),
        (r"dans quelques (jours|semaines|mois)", None),
        (r"(bientôt|prochainement|soon)", "bientôt"),
    ]
    for pattern, label in timing_patterns:
        m = re.search(pattern, text)
        if m:
            if label:
                return label
            return m.group(0)
    return None


def _estimate_date(timing: str, ref: datetime) -> Optional[str]:
    """Estime une date à partir d'un timing textuel."""
    if not timing:
        return None
    
    if "demain" in timing:
        return (ref + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "semaine prochaine" in timing:
        return (ref + timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif "mois prochain" in timing:
        return (ref + timedelta(days=30)).strftime("%Y-%m-%d")
    elif "bientôt" in timing or "prochainement" in timing:
        return (ref + timedelta(days=14)).strftime("%Y-%m-%d")
    
    m = re.search(r"dans (\d+) (jours?|semaines?|mois)", timing)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        if "mois" in unit:
            return (ref + timedelta(days=n * 30)).strftime("%Y-%m-%d")
        elif "semaine" in unit:
            return (ref + timedelta(weeks=n)).strftime("%Y-%m-%d")
        else:
            return (ref + timedelta(days=n)).strftime("%Y-%m-%d")
    
    return None


# ============================================================================
# EXTRACTION DE DEMANDES EN ATTENTE (Rupture de stock)
# ============================================================================

RUPTURE_PATTERNS = [
    r"(?:vous\s+)?(?:n'avez|n'avez)\s+plus",
    r"(?:plus\s+)?(?:en\s+)?(?:stock|disponible)",
    r"(?:pas|plus)\s+(?:disponible|dispo)",
    r"rupture",
    r"out\s+of\s+stock",
    r"en\s+rupture",
    r"(?:avez[- ]vous|est-ce que)\s+(?:encore|toujours)",
    r"(?:j'attends|je\s+cherche|je\s+voudrais)\s+(?:le|la|les|un|une)",
    r"waitlist|liste\s+d'attente",
]

TAILLE_PATTERNS = [
    r"(?:taille|size)\s+(\w+)",
    r"(?:en\s+)?(\d{2})\b",  # 36, 38, 40...
    r"(?:en\s+)?(XS|S|M|L|XL|XXL)\b",
]


def extract_demandes_attente(text: str) -> list:
    """
    Détecte les produits demandés qui sont en rupture ou indisponibles.
    
    Returns:
        list[dict]: [{produit, marque, taille, couleur, statut}]
    """
    if not text:
        return []
    
    text_lower = text.lower()
    results = []
    
    is_rupture = False
    for pattern in RUPTURE_PATTERNS:
        if re.search(pattern, text_lower):
            is_rupture = True
            break
    
    if not is_rupture:
        return []
    
    # Quoi est en rupture ?
    produits = extract_produits_possedes(text)
    
    # Taille demandée ?
    taille = None
    for pattern in TAILLE_PATTERNS:
        m = re.search(pattern, text_lower)
        if m:
            taille = m.group(1)
            break
    
    if produits:
        for p in produits:
            results.append({
                "produit": p["produit"],
                "marque": p.get("marque"),
                "taille": taille,
                "couleur": p.get("couleur"),
                "statut": "rupture"
            })
    else:
        results.append({
            "produit": "non spécifié",
            "marque": None,
            "taille": taille,
            "couleur": None,
            "statut": "rupture"
        })
    
    return results


# ============================================================================
# EXTRACTION D'AFFINITÉS CROSS-MAISON
# ============================================================================

AFFINITES_MAPPING = {
    "vins_spiritueux": {
        "keywords": ["champagne", "vin", "wine", "cognac", "whisky", "dégustation", 
                     "sommelier", "vignoble", "vineyard", "œnologie", "millésime"],
        "maisons": ["Dom Pérignon", "Moët & Chandon", "Ruinart", "Krug", "Hennessy"],
    },
    "art_culture": {
        "keywords": ["art", "musée", "museum", "galerie", "gallery", "expo", "exposition",
                     "peinture", "sculpture", "artiste", "collection d'art", "vernissage",
                     "fondation", "contemporain"],
        "maisons": ["Fondation Louis Vuitton", "Artycapucines"],
    },
    "horlogerie": {
        "keywords": ["montre", "watch", "horlog", "chronographe", "mouvement",
                     "complication", "tourbillon", "calibre"],
        "maisons": ["TAG Heuer", "Hublot", "Zenith", "Chaumet"],
    },
    "joaillerie": {
        "keywords": ["bijou", "jewelry", "bague", "ring", "collier", "necklace",
                     "diamant", "diamond", "émeraude", "saphir", "rubis",
                     "haute joaillerie", "bracelet"],
        "maisons": ["Tiffany & Co.", "Bulgari", "Chaumet", "Fred"],
    },
    "beaute_parfum": {
        "keywords": ["parfum", "perfume", "maquillage", "makeup", "soin", "skincare",
                     "cosmétique", "beauty", "fragrance", "rouge à lèvres"],
        "maisons": ["Guerlain", "Sephora", "Givenchy Beauty", "Dior Beauty", "Fenty Beauty"],
    },
    "gastronomie": {
        "keywords": ["gastronomie", "restaurant", "chef", "étoilé", "michelin",
                     "cuisine", "gourmet", "dégustation", "caviar", "truffe"],
        "maisons": ["Cheval Blanc (Restaurant)", "Les Crayères"],
    },
    "voyage_luxe": {
        "keywords": ["hôtel", "hotel", "palace", "resort", "yacht", "croisière",
                     "first class", "première classe", "jet privé", "concierge"],
        "maisons": ["Cheval Blanc", "Belmond"],
    },
}


def extract_preferences_croisees(text: str, tags: dict = None) -> list:
    """
    Détecte les affinités du client pouvant mener à une recommandation cross-maison.
    
    Returns:
        list[dict]: [{affinite, maisons_cibles, confidence, keywords_detectes}]
    """
    if not text:
        return []
    
    text_lower = text.lower()
    
    # Ajouter les tags lifestyle si disponibles
    extra_keywords = []
    if tags:
        for field in ["sport", "musique", "art_culture", "gastronomie", "voyage"]:
            val = tags.get(field, [])
            if isinstance(val, list):
                extra_keywords.extend([v.lower() for v in val])
            elif isinstance(val, str) and val:
                extra_keywords.append(val.lower())
    
    combined = text_lower + " " + " ".join(extra_keywords)
    results = []
    
    for affinite, data in AFFINITES_MAPPING.items():
        matched_kw = [kw for kw in data["keywords"] if kw in combined]
        if matched_kw:
            results.append({
                "affinite": affinite.replace("_", " ").title(),
                "maisons_cibles": data["maisons"],
                "confidence": min(1.0, 0.5 + 0.15 * len(matched_kw)),
                "keywords_detectes": matched_kw,
            })
    
    return results


# ============================================================================
# FONCTION PRINCIPALE D'EXTRACTION
# ============================================================================

def extract_all_actionable(text: str, tags: dict = None, reference_date: datetime = None) -> dict:
    """
    Exécute toutes les extractions contextuelles sur une transcription.
    
    Returns:
        dict: {dates_cles, produits, projets_vie, demandes_attente, affinites_cross}
    """
    return {
        "dates_cles": extract_dates_cles(text, reference_date),
        "produits": extract_produits_possedes(text),
        "projets_vie": extract_projets_vie(text, reference_date),
        "demandes_attente": extract_demandes_attente(text),
        "affinites_cross": extract_preferences_croisees(text, tags),
    }
