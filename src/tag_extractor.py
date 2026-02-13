"""
Module d'extraction de tags - Version Python pure "Turbo"
Extrait les tags de la taxonomie LVMH 100% via Algorithme (0% IA)
Optimisé pour la vitesse et la précision des détails.
"""
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
try:
    from src.mappings.identity import GENRE_MAPPING, LANGUE_MAPPING, STATUT_MAPPING, PROFESSIONS_ADVANCED
    from src.mappings.location import CITIES_ADVANCED
    from src.mappings.lifestyle import SPORT_MAPPING, MUSIQUE_MAPPING, ANIMAUX_MAPPING, VOYAGE_MAPPING, ART_CULTURE_MAPPING, GASTRONOMIE_MAPPING
    from src.mappings.style import PIECES_MAPPING, COULEURS_ADVANCED, MATIERES_ADVANCED, SENSIBILITE_MODE, TAILLES_MAPPING
    from src.mappings.purchase import MOTIF_ADVANCED, TIMING_MAPPING, MARQUES_LVMH, FREQUENCE_ACHAT
    from src.mappings.preferences import REGIME_MAPPING, ALLERGIES_MAPPING, VALEURS_MAPPING
    from src.mappings.tracking import ACTIONS_MAPPING, ECHEANCES_MAPPING, CANAUX_MAPPING
    ADVANCED_TAXONOMY_AVAILABLE = True
except Exception:
    ADVANCED_TAXONOMY_AVAILABLE = False

# ============================================================================
# 0. NETTOYAGE TURBO (REGEX)
# ============================================================================

def clean_text_turbo(text: str) -> str:
    """
    Nettoie le texte instantanément sans IA.
    Supprime: 
    - HTML tags
    - Hésitations (euh, bah, hum)
    - Espaces multiples
    - Caractères de contrôle dangereux
    
    PRÉSERVE:
    - Chiffres (pour âge et budget)
    - Majuscules (pour villes et noms propres)
    - Symboles monétaires (€, $)
    """
    if not isinstance(text, str): return ""
    
    # 1. Supprimer HTML / balises (protection XSS côté extraction)
    text = re.sub(r'(?is)<script.*?>.*?</script>', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Supprimer uniquement les caractères de contrôle dangereux (pas les chiffres/lettres)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', ' ', text)
    
    # 2. Supprimer hésitations courantes (case insensitive)
    hesitations = [r'\beuh\b', r'\bhum+?\b', r'\bben\b', r'\bbah\b', r'\bgenre\b', r'\bdu coup\b']
    for h in hesitations:
        text = re.sub(h, '', text, flags=re.IGNORECASE)
        
    # 3. Nettoyer espaces et sauts de ligne (mais garder le reste)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# ============================================================================
# 1. DICTIONNAIRES DE DÉTECTION (LE "CERVEAU" DES MOTS-CLÉS)
# ============================================================================

# Localisation
CITIES = {
    "europe": ["Paris", "Berlin", "Milan", "Madrid", "London", "Lyon", "Barcelona", "Rome", "Amsterdam", "Bruxelles", "Munich", "Genève", "Zurich", "Monaco"],
    "amerique": ["New York", "Los Angeles", "Miami", "Toronto", "Montreal", "Chicago", "San Francisco", "Boston"],
    "moyen_orient_asie": ["Dubai", "Tokyo", "Hong Kong", "Singapore", "Shanghai", "Doha", "Abu Dhabi", "Seoul", "Beijing"],
    "afrique": ["Maroc", "Tunisie", "Algérie", "Égypte", "Afrique du Sud", "Nigeria", "Kenya", "Casablanca", "Marrakech"]
}

# Couleurs
COLORS_MAPPING = {
    "Noir": ["noir", "black", "noire", "noirs", "sombre"],
    "Beige": ["beige", "écru", "crème", "cream", "sable", "nude"],
    "Cognac": ["cognac", "caramel", "tan", "camel", "marron clair"],
    "Bordeaux": ["bordeaux", "burgundy", "vin", "rouge sombre"],
    "Bleu_marine": ["navy", "bleu marine", "marine", "dark blue", "bleu nuit"],
    "Blanc": ["blanc", "white", "ivoire", "ivory", "neige"],
    "Gris": ["gris", "grey", "gray", "anthracite", "argent", "silver"],
    "Rose_gold": ["rose gold", "or rose", "rosé", "pink gold"],
    "Rouge": ["rouge", "red", "vermillon"]
}

# Matières
MATERIALS_MAPPING = {
    "Cuir": ["cuir", "leather", "veau", "agneau", "vachette", "peau", "daim", "suede", "nubuck"],
    "Cachemire": ["cachemire", "cashmere", "mohair", "angora"],
    "Soie": ["soie", "silk", "satin", "velours", "velvet"],
    "Laine": ["laine", "wool", "mérinos", "tweed", "flanelle"],
    "Coton": ["coton", "cotton", "lin", "linen", "denim", "toile"],
    "Matières_vegan": ["vegan", "végane", "synthétique", "faux cuir", "simili", "polyester", "nylon", "recyclé"]
}

# Sports & Lifestyle
LIFESTYLE_MAPPING = {
    "Golf": ["golf", "golfeur", "club"],
    "Tennis": ["tennis", "roland garros", "wimbledon"],
    "Yoga": ["yoga", "pilates", "méditation"],
    "Running": ["running", "course", "jogging", "marathon"],
    "Fitness": ["fitness", "gym", "musculation", "crossfit"],
    "Ski": ["ski", "skiing", "montagne", "alpes"],
    "Football": ["football", "foot", "soccer"],
    "Voyage": ["voyage", "travel", "avion", "aéroport", "vacances", "trip", "tour du monde"],
    "Art_Culture": ["musée", "galerie", "peinture", "art", "exposition", "vernissage", "opéra", "théâtre"],
    "Gastronomie": ["restaurant", "gastronomie", "vin", "chef", "étoilé", "diner", "cuisine"]
}

# Style Personnel
STYLE_MAPPING = {
    "Casual": ["casual", "décontracté", "cool", "quotidien", "simple", "détente", "relaxed", "comfortable", "everyday", "laid-back"],
    "Chic": ["chic", "élégant", "soirée", "habillé", "raffiné", "classe", "elegant", "sophisticated", "stylish", "fashionable", "trendy"],
    "Business": ["business", "travail", "bureau", "pro", "réunion", "corporate", "professional", "formal", "office", "work"],
    "Sportswear": ["sportswear", "sport", "athleisure", "sneakers", "baskets", "athletic", "active", "gym", "training"],
    "Haute_couture": ["haute couture", "défilé", "pièce unique", "sur mesure", "exception", "luxury", "exclusive", "bespoke", "custom", "designer"]
}

# Motif d'Achat
MOTIF_MAPPING = {
    "Cadeau": ["cadeau", "offrir", "pour ma", "pour mon", "surprise", "gift"],
    "Mariage": ["mariage", "wedding", "mariée", "cérémonie", "fiançailles"],
    "Anniversaire": ["anniversaire", "birthday", "bday", "fêter", "30 ans", "40 ans", "50 ans"],
    "Diplôme": ["diplôme", "graduation", "examen", "réussite", "promo"],
    "Voyage": ["voyage", "vacances", "partir", "valise"],
    "Achat_personnel": ["pour moi", "me faire plaisir", "j'ai besoin", "je cherche", "perso"]
}

# Situation Familiale
FAMILLE_MAPPING = {
    "Marié(e)": ["marié", "mariée", "mon mari", "ma femme", "époux", "épouse", "married", "husband", "wife", "spouse", "wedding ring", "alliance"],
    "Couple": ["couple", "copain", "copine", "conjoint", "partenaire", "partner", "boyfriend", "girlfriend", "fiancé", "fiancée", "relationship", "together"],
    "Avec_enfants": ["enfant", "enfants", "fils", "fille", "bébé", "maman", "papa", "famille", "children", "kids", "son", "daughter", "parent", "father", "mother", "dad", "mom"],
    "Célibataire": ["célibataire", "seul", "solo", "single", "alone", "independent"]
}

# Profession
PROFESSIONS_MAPPING = {
    "Entrepreneur": ["entrepreneur", "chef d'entreprise", "fondateur", "ceo", "business", "start-up", "startup", "founder", "owner", "patron"],
    "Cadre": ["cadre", "directeur", "manager", "responsable", "exécutif", "director", "executive", "vp", "vice president", "head of"],
    "Profession_libérale": ["avocat", "médecin", "architecte", "notaire", "consultant", "lawyer", "doctor", "physician", "dentist", "pharmacien"],
    "Artiste": ["artiste", "designer", "créateur", "musicien", "acteur", "peintre", "artist", "photographer", "influencer", "créatif"],
    "Étudiant": ["étudiant", "école", "université", "stage", "stagiaire", "student", "intern", "graduate", "phd"]
}

# ============================================================================
# 2. MOTEUR D'EXTRACTION (LE "MUSCLE")
# ============================================================================

def scan_text_for_keywords(text: str, mapping: Dict[str, List[str]]) -> List[str]:
    """Scanne le texte pour trouver les clés correspondantes aux mots-clés"""
    if not text:
        return []

    found = []

    for category, keywords in mapping.items():
        for kw in keywords:
            if _keyword_in_text(text, kw):
                found.append(category)
                break

    return list(dict.fromkeys(found))  # Déduplication stable

def scan_text_for_keywords_advanced(text: str, mapping: Dict[str, Any]) -> List[str]:
    """
    Scan générique pour mappings avancés:
    - {Categorie: [keywords]}
    - {Region: {Categorie: [keywords]}}
    """
    if not text:
        return []

    found = []

    for key, value in mapping.items():
        if isinstance(value, dict):
            # Mapping imbriqué (ex: villes par région)
            for sub_key, sub_keywords in value.items():
                for kw in sub_keywords:
                    if _keyword_in_text(text, kw):
                        found.append(sub_key)
                        break
        elif isinstance(value, list):
            for kw in value:
                if _keyword_in_text(text, kw):
                    found.append(key)
                    break

    # Déduplication en conservant l'ordre
    seen = set()
    ordered = []
    for item in found:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered

def _is_ambiguous_keyword(kw: str) -> bool:
    """
    Mots trop ambigus causant des faux positifs (ex: 'or' dans une phrase FR).
    """
    bad = {
        "or", "ai", "pr", "s", "m", "l", "xs", "xl", "xxs",
        "lv", "cb", "la", "le", "de", "jean"
    }
    return kw.strip().lower() in bad

def _keyword_in_text(text: str, keyword: str) -> bool:
    """
    Matching robuste:
    - mot entier (pas sous-chaîne)
    - ignore les mots trop courts/ambigus
    - gère les expressions multi-mots
    """
    if not text or not keyword:
        return False

    kw = keyword.strip().lower()
    if not kw:
        return False

    if _is_ambiguous_keyword(kw):
        return False

    # Évite les mots trop courts qui génèrent trop de bruit
    if len(kw) <= 2:
        return False

    escaped = re.escape(kw)
    pattern = rf"(?<!\w){escaped}(?!\w)"
    return re.search(pattern, text.lower()) is not None

def extract_genre_precise(text: str) -> List[str]:
    """
    Détection genre STRICTE (uniquement auto-déclaration explicite du client).
    Exemple: "acheter un sac à sa femme" NE doit PAS impliquer "Femme".
    """
    if not text:
        return []

    t = text.lower()
    # On ne garde que les formulations en "je/moi" pour éviter les faux positifs contextuels.
    male_patterns = [
        r"\bje\s+suis\s+un\s+homme\b",
        r"\bje\s+suis\s+monsieur\b",
        r"\bje\s+suis\s+mr\b",
        r"\bmoi[, ]+\s*je\s+suis\s+un\s+homme\b",
    ]
    female_patterns = [
        r"\bje\s+suis\s+une\s+femme\b",
        r"\bje\s+suis\s+madame\b",
        r"\bje\s+suis\s+mme\b",
        r"\bje\s+suis\s+mademoiselle\b",
        r"\bmoi[, ]+\s*je\s+suis\s+une\s+femme\b",
    ]

    if any(re.search(p, t) for p in male_patterns):
        return ["Homme"]
    if any(re.search(p, t) for p in female_patterns):
        return ["Femme"]
    return []

def extract_age_turbo(text: str) -> Optional[str]:
    """Extraction d'âge avancée (tolérante, évite les faux négatifs)."""
    if not text:
        return None
    text_lower = text.lower()
    
    # Regex précises (chiffres)
    patterns = [
        r"\bj[' ]?ai\s*(\d{1,2})\s*ans\b",
        r"\bj[' ]?ai\s*(\d{1,2})\b",
        r"\b(\d{1,2})\s*(?:ans|an|year|yo|jahre)\b",
        r"\b(\d{1,2})\s*years?\s*old\b",
        r"\bage\s*(?:de)?\s*(\d{1,2})\b",
        r'\bné[e]?\s*(?:en)?\s*(19\d{2}|20\d{2})\b', # Année naissance
        r"\bage\s*[:]?\s*(\d{1,2})\b"
    ]
    
    for p in patterns:
        m = re.search(p, text_lower)
        if m:
            val = int(m.group(1))
            if val > 1900: # C'est une année
                val = datetime.now().year - val
            
            # Garde-fou simple sur les âges plausibles
            if val < 15 or val > 99:
                continue

            # Catégorisation taxonomie
            if val <= 25: return "18-25"
            if val <= 35: return "26-35"
            if val <= 45: return "36-45"
            if val <= 55: return "46-55"
            return "56+"

    # Âges en lettres FR (ex: "quarante-cinq ans")
    word_to_num = {
        "dix-huit": 18, "dix huit": 18, "dix-neuf": 19, "dix neuf": 19,
        "vingt": 20, "vingt-et-un": 21, "vingt et un": 21, "vingt-deux": 22, "vingt deux": 22,
        "vingt-trois": 23, "vingt trois": 23, "vingt-quatre": 24, "vingt quatre": 24,
        "vingt-cinq": 25, "vingt cinq": 25, "trente": 30, "quarante": 40, "cinquante": 50,
        "soixante": 60,
    }

    units = {
        "zero": 0, "zéro": 0, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4,
        "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9
    }
    tens = {
        "dix": 10, "vingt": 20, "trente": 30, "quarante": 40, "cinquante": 50, "soixante": 60
    }

    def _parse_simple_french_age_words(raw_age: str) -> Optional[int]:
        s = raw_age.strip().lower().replace("’", "'")
        if s in word_to_num:
            return word_to_num[s]

        # Normalise séparateurs: "quarante-cinq", "quarante cinq", "quarante et cinq"
        tokens = [t for t in re.split(r"[\s\-']+", s) if t and t != "et"]
        if not tokens:
            return None

        # Ignore préfixes de contexte fréquents: "il a", "elle a", "j ai", etc.
        stopwords = {"il", "elle", "a", "j", "je", "ai", "ans", "age", "âge", "de"}
        tokens = [t for t in tokens if t not in stopwords]
        if not tokens:
            return None

        # Cas direct unitaire (ex: "quarante")
        if len(tokens) == 1:
            if tokens[0] in tens:
                return tens[tokens[0]]
            if tokens[0] in units:
                return units[tokens[0]]
            return None

        # Cas dizaine + unité (ex: "quarante cinq")
        if len(tokens) == 2 and tokens[0] in tens and tokens[1] in units:
            return tens[tokens[0]] + units[tokens[1]]

        # Cas avec contexte résiduel: on tente les 2 derniers puis le dernier token
        if len(tokens) >= 3:
            last_two = tokens[-2:]
            if last_two[0] in tens and last_two[1] in units:
                return tens[last_two[0]] + units[last_two[1]]
            if tokens[-1] in tens:
                return tens[tokens[-1]]
            if tokens[-1] in units:
                return units[tokens[-1]]

        return None
    age_words = re.search(r"\b([a-zàâçéèêëîïôûùüÿœæ' -]{3,25})\s+ans\b", text_lower)
    if age_words:
        raw = " ".join(age_words.group(1).strip().split())
        raw = raw.replace("’", "'")
        parsed_age = _parse_simple_french_age_words(raw)
        if parsed_age is not None and 15 <= parsed_age <= 99:
            val = parsed_age
            if val <= 25: return "18-25"
            if val <= 35: return "26-35"
            if val <= 45: return "36-45"
            if val <= 55: return "46-55"
            return "56+"

    # IMPORTANT: pas d'inférence implicite (ex: "étudiant" => tranche d'âge).
    # On n'affiche l'âge que s'il est explicitement mentionné.
    return None

def extract_budget_turbo(text: str) -> Optional[str]:
    """Extraction budget normalisée"""
    if not text: return None
    text_lower = text.lower()

    # 1. Détection "Illimité"
    if any(x in text_lower for x in ["illimité", "no limit", "flexible", "pas de budget", "gros budget"]):
        return "25k+"

    # 2. Extraction numérique
    # Cherche 5000€, 5k, 5000 euros...
    matches = re.findall(r'(\d+[.,]?\d*)\s*(?:k|m|€|\$|euros?|dollars?|francs?)', text_lower)
    
    amount = 0
    if matches:
        # Prendre le plus grand nombre trouvé (souvent le budget max)
        vals = []
        for m in matches:
            val_str = m.replace(',', '.')
            try:
                val = float(val_str)
                # Gestion du "k" (ex: 5k)
                if "k" in text_lower[text_lower.find(m):text_lower.find(m)+5]: 
                    val *= 1000
                elif val < 100: # Probablement k non détecté ou abréviation
                    val *= 1000
                vals.append(val)
            except: pass
        
        if vals: amount = max(vals)

    # Si pas de symbole, essai regex simple nombre > 1000
    if amount == 0:
        nums = re.findall(r'\b(\d{4,6})\b', text)
        if nums:
            amount = max([int(n) for n in nums])

    # 3. Mapping Taxonomie
    if amount == 0: return None
    if amount < 5000: return "<5k"
    if amount < 10000: return "5-10k"
    if amount < 15000: return "10-15k"
    if amount < 25000: return "15-25k"
    return "25k+"

def extract_urgency_turbo(text: str) -> Optional[int]:
    """Score d'urgence 1-5 UNIQUEMENT si urgence explicitement mentionnée."""
    if not text:
        return None
    text_lower = text.lower()

    # Mention explicite de non-urgence: on n'affiche pas d'urgence.
    if any(x in text_lower for x in ["pas urgent", "aucune urgence", "sans urgence", "quand vous voulez", "plus tard"]):
        return None

    # Niveau 5 (très urgent explicite)
    if any(x in text_lower for x in ["urgent", "urgence", "tout de suite", "immédiat", "immediat", "asap", "au plus vite"]):
        return 5

    # Niveau 4 (contrainte temporelle explicite)
    if any(x in text_lower for x in ["demain", "aujourd'hui", "ce soir", "cette semaine", "avant le", "d'ici", "pour ce week-end", "pour weekend"]):
        return 4

    # Niveau 3 (urgence modérée explicitée)
    if any(x in text_lower for x in ["rapidement", "vite", "dans les prochains jours", "mois prochain"]):
        return 3

    # Sinon: aucune urgence explicite détectée.
    return None

def extract_motif_precise(text: str) -> List[str]:
    """
    Détection motif plus fiable et explicite (évite les oublis).
    """
    if not text:
        return []

    t = text.lower()
    motifs = []

    # Cadeau / achat pour quelqu'un
    cadeau_patterns = [
        r"\bcadeau\b",
        r"\boffrir\b",
        r"\bpour\s+(ma|mon|sa|son)\s+(femme|mari|copine|copain|mère|mere|père|pere|enfant|fils|fille)\b",
        r"\b[aà]\s+(ma|mon|sa|son)\s+(femme|mari|copine|copain|mère|mere|père|pere|enfant|fils|fille)\b",
    ]
    if any(re.search(p, t) for p in cadeau_patterns):
        motifs.append("Cadeau")

    if re.search(r"\banniversaire|birthday|bday\b", t):
        motifs.append("Anniversaire")
    if re.search(r"\bmariage|wedding|fianc[aé]illes\b", t):
        motifs.append("Mariage")
    if re.search(r"\bnaissance|nouveau[- ]n[ée]|baby shower\b", t):
        motifs.append("Naissance")
    if re.search(r"\bpour moi\b|\bme faire plaisir\b|\bself[- ]gift\b", t):
        motifs.append("Plaisir_personnel")
    # Voyage seulement si contexte d'achat réel
    if re.search(r"(pour|avant|spécial|special|achat).{0,25}\b(voyage|vacances|trip)\b|\b(valise)\b", t):
        motifs.append("Voyage")

    # Déduplication stable
    return list(dict.fromkeys(motifs))

def extract_country_precise(text: str) -> Optional[str]:
    """Détecte le pays mentionné (utile quand aucune ville n'est donnée)."""
    if not text:
        return None

    t = text.lower()
    country_aliases = {
        "États-Unis": ["états-unis", "etats-unis", "etats unis", "usa", "u.s.a", "united states"],
        "France": ["france"],
        "Italie": ["italie", "italy"],
        "Espagne": ["espagne", "spain"],
        "Allemagne": ["allemagne", "germany"],
        "Royaume-Uni": ["royaume-uni", "uk", "united kingdom", "angleterre", "england"],
        "Suisse": ["suisse", "switzerland"],
        "Belgique": ["belgique", "belgium"],
        "Portugal": ["portugal", "portugais"],
        "Canada": ["canada"],
        "Maroc": ["maroc", "morocco"],
    }

    for country, aliases in country_aliases.items():
        for alias in aliases:
            if _keyword_in_text(t, alias):
                return country
    return None

def extract_famille_precise(text: str) -> List[str]:
    """Détection famille sans faux positif sur le mot générique 'famille'."""
    if not text:
        return []
    t = text.lower()
    out = []
    if re.search(r"\b(couple|en couple|partenaire|copain|copine|conjoint)\b", t):
        out.append("Couple")
    if re.search(r"\b(enfant|enfants|fils|fille|kids|children)\b", t):
        out.append("Avec_enfants")
    if re.search(r"\b(célibataire|single|seul)\b", t):
        out.append("Célibataire")
    if re.search(r"\b(mari[ée]|époux|épouse|husband|wife)\b", t):
        out.append("Marié(e)")
    return list(dict.fromkeys(out))

def extract_marques_precises(text: str) -> List[str]:
    """Marques: seulement mentions explicites de marque, sans inférence matière."""
    if not text:
        return []
    t = text.lower()
    brand_terms = {
        "Louis_Vuitton": ["louis vuitton", " vuitton", " lv "],
        "Dior": ["dior", "christian dior"],
        "Gucci": ["gucci"],
        "Loro_Piana": ["loro piana"],
        "Bulgari": ["bulgari", "bvlgari"],
        "Givenchy": ["givenchy"],
        "Tiffany": ["tiffany", "tiffany & co", "tiffany co"],
        "Celine": ["celine", "céline"],
        "Fendi": ["fendi"],
        "Sephora": ["sephora"],
    }
    out = []
    for brand, terms in brand_terms.items():
        if any(_keyword_in_text(t, term) for term in terms):
            out.append(brand)
    return out

def extract_gastronomie_precise(text: str) -> List[str]:
    """Gastronomie uniquement si contexte alimentaire/boisson explicite."""
    if not text:
        return []
    t = text.lower()
    out = []
    if re.search(r"\b(vin|wine|dégustation|degustation|sommelier)\b", t):
        out.append("Vins")
    if re.search(r"\b(champagne|champagnes)\b", t):
        out.append("Champagnes")
    # Spiritueux: exclure faux positif 'cognac' couleur
    if re.search(r"\b(whisky|rhum|vodka|spiritueux|cocktail|mixologie)\b", t):
        out.append("Spiritueux")
    elif re.search(r"\bcognac\b", t) and re.search(r"\b(boire|boisson|drink|dégust|alcool)\b", t):
        out.append("Spiritueux")
    if re.search(r"\b(restaurant|gastronomie|fine dining|chef|étoilé|etoile)\b", t):
        out.append("Fine_dining")
    return list(dict.fromkeys(out))

def extract_tailles_precise(text: str) -> List[str]:
    """Tailles explicites (XS/S/M/L) + pointure explicite."""
    if not text:
        return []
    t = text.lower()
    out = []

    # XS/S/M/L explicites
    if re.search(r"\b(x\s*s|xs|extra small)\b", t):
        out.append("XS")
    if re.search(r"\b(small|taille s| s )\b", f" {t} "):
        out.append("S")
    if re.search(r"\b(medium|taille m| m )\b", f" {t} "):
        out.append("M")
    if re.search(r"\b(large|taille l| l )\b", f" {t} "):
        out.append("L")

    # Pointures chiffrées directes UNIQUEMENT en contexte taille/chaussure
    size_context_spans = re.findall(r"(?:taille|pointure|chausse|chaussure)s?\s*(?:du|de|:)?\s*([^.!?\n]{0,80})", t)
    for span in size_context_spans:
        for p in re.findall(r"\b(3[5-9]|4[0-6])\b", span):
            val = int(p)
            if 35 <= val <= 37 and "35_37" not in out:
                out.append("35_37")
            elif 38 <= val <= 40 and "38_40" not in out:
                out.append("38_40")
            elif 41 <= val <= 43 and "41_43" not in out:
                out.append("41_43")
            elif 44 <= val <= 46 and "44_46" not in out:
                out.append("44_46")

    # Pointures en lettres (ex: "pointure trente-cinq trente-sept")
    number_words = {
        "trente-cinq": 35, "trente cinq": 35,
        "trente-six": 36, "trente six": 36,
        "trente-sept": 37, "trente sept": 37,
        "trente-huit": 38, "trente huit": 38,
        "trente-neuf": 39, "trente neuf": 39,
        "quarante": 40,
        "quarante-et-un": 41, "quarante et un": 41,
        "quarante-deux": 42, "quarante deux": 42,
        "quarante-trois": 43, "quarante trois": 43,
        "quarante-quatre": 44, "quarante quatre": 44,
        "quarante-cinq": 45, "quarante cinq": 45,
        "quarante-six": 46, "quarante six": 46,
    }

    pointure_spans = re.findall(r"(?:pointure|chausse)\s*(?:du|de|:)?\s*([^.!?\n]{0,80})", t)
    for span in pointure_spans:
        s = " ".join(span.split())
        for w, val in number_words.items():
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", s):
                if 35 <= val <= 37 and "35_37" not in out:
                    out.append("35_37")
                elif 38 <= val <= 40 and "38_40" not in out:
                    out.append("38_40")
                elif 41 <= val <= 43 and "41_43" not in out:
                    out.append("41_43")
                elif 44 <= val <= 46 and "44_46" not in out:
                    out.append("44_46")

    return out

def _extract_piece_by_context(text: str, context_patterns: List[str]) -> List[str]:
    """
    Extrait les pièces en filtrant par contexte:
    - favori (préférence)
    - recherché (besoin d'achat)
    """
    if not text:
        return []

    t = text.lower()
    found = []

    for piece, keywords in PIECES_MAPPING.items():
        # Vérifie que la pièce est présente
        has_piece = any(_keyword_in_text(t, kw) for kw in keywords if len(kw.strip()) > 2)
        if not has_piece:
            continue

        # Vérifie qu'il y a un contexte valide autour
        is_contextual = False
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if len(kw_clean) <= 2 or _is_ambiguous_keyword(kw_clean):
                continue
            for ctx in context_patterns:
                # contexte avant ou après le mot-clé
                p1 = rf"{ctx}.{{0,40}}(?<!\w){re.escape(kw_clean)}(?!\w)"
                p2 = rf"(?<!\w){re.escape(kw_clean)}(?!\w).{{0,40}}{ctx}"
                if re.search(p1, t) or re.search(p2, t):
                    is_contextual = True
                    break
            if is_contextual:
                break

        if is_contextual:
            found.append(piece)

    return list(dict.fromkeys(found))

def extract_sensibilite_mode_precise(text: str) -> List[str]:
    """
    Sensibilité mode stricte:
    - évite de classer "classique" musical/culturel comme style vestimentaire.
    """
    if not text:
        return []

    t = text.lower()
    out = []
    # Termes de contexte mode/look/vestimentaire autour du mot-clé
    context = r"(style|look|mode|vestimentaire|tenue|porter|habill[eé]|garde-robe|silhouette)"

    for category, keywords in SENSIBILITE_MODE.items():
        matched = False
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if len(kw_clean) <= 2 or _is_ambiguous_keyword(kw_clean):
                continue
            p1 = rf"{context}.{{0,35}}(?<!\w){re.escape(kw_clean)}(?!\w)"
            p2 = rf"(?<!\w){re.escape(kw_clean)}(?!\w).{{0,35}}{context}"
            if re.search(p1, t) or re.search(p2, t):
                matched = True
                break
        if matched:
            out.append(category)
    return out

def extract_canaux_contact_precis(text: str) -> List[str]:
    """
    Canaux de contact stricts:
    - garde seulement les préférences de canal explicites
    - évite le faux positif "numéro de téléphone"
    """
    if not text:
        return []

    t = text.lower()
    out = []

    # Exclusions explicites (donnée RGPD ou mention descriptive sans préférence)
    if re.search(r"\bnum[ée]ro\s+de\s+t[ée]l[ée]phone\b", t):
        t = re.sub(r"\bnum[ée]ro\s+de\s+t[ée]l[ée]phone\b", " ", t)

    channel_patterns = {
        "Email": [
            r"\bpar\s+(mail|email|e-mail|courriel)\b",
            r"\b(contact|joindre|recontacter).{0,25}(mail|email|e-mail|courriel)\b",
            r"\bcanaux?\s+de\s+contact.{0,25}(mail|email|e-mail|courriel)\b",
        ],
        "Telephone": [
            r"\bpar\s+t[ée]l[ée]phone\b",
            r"\b(appel(?:er)?|m[' ]?appeler|joindre).{0,25}(t[ée]l[ée]phone)\b",
            r"\bcanaux?\s+de\s+contact.{0,25}(t[ée]l[ée]phone)\b",
        ],
        "SMS": [
            r"\bpar\s+sms\b",
            r"\b(texto|sms)\b",
            r"\bcanaux?\s+de\s+contact.{0,25}sms\b",
        ],
        "WhatsApp": [
            r"\b(par\s+)?whats\s?app\b",
            r"\bcanaux?\s+de\s+contact.{0,25}whats\s?app\b",
        ],
        "Reseaux_sociaux": [
            r"\b(par|via)\s+(instagram|facebook|linkedin|r[ée]seaux?\s+sociaux)\b",
            r"\b(dm|message priv[ée])\b",
        ],
        "Site_web": [
            r"\b(par|via)\s+(site web|website|internet|en ligne)\b",
            r"\bformulaire\s+en\s+ligne\b",
        ],
    }

    for channel, patterns in channel_patterns.items():
        if any(re.search(p, t) for p in patterns):
            out.append(channel)

    return list(dict.fromkeys(out))

def extract_pieces_favorites_precise(text: str) -> List[str]:
    """Pièces favorites = préférences (pas achat ponctuel)."""
    favorite_context = [
        r"\bj[' ]?aime\b", r"\bil aime\b", r"\belle aime\b",
        r"\bj[' ]?adore\b", r"\bil adore\b", r"\belle adore\b",
        r"\bpr[eé]f[eè]re\b", r"\bpr[eé]f[eè]rent\b",
        r"\bpr[eé]f[eé]r[ée]e?s?\b", r"\bfavori(?:te)?s?\b",
        r"\bpi[eè]ce[s]?\s+(?:pr[eé]f[eé]r[ée]e?s?|favori(?:te)?s?)\b",
        r"\bfan de\b", r"\bporte\b", r"\bstyle\b", r"\bprivil[eé]gie\b"
    ]
    if not text:
        return []

    t = text.lower()
    found = []
    max_window = 80

    # Ajouter des pièces génériques pour mieux capter la phrase naturelle
    piece_catalog = dict(PIECES_MAPPING)
    piece_catalog["Chaussures"] = ["chaussure", "chaussures", "souliers", "shoes", "footwear"]

    purchase_context = [
        r"\bcherche\b", r"\brecherche\b", r"\bvoudrai[st]?\b", r"\bveut\b",
        r"\bbesoin de\b", r"\bvenir acheter\b", r"\bvenu acheter\b",
        r"\bacheter\b", r"\bachat\b", r"\boffrir\b", r"\bcadeau\b", r"\blooking for\b"
    ]

    for piece, keywords in piece_catalog.items():
        piece_is_favorite = False
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if len(kw_clean) <= 2 or _is_ambiguous_keyword(kw_clean):
                continue

            for m in re.finditer(rf"(?<!\w){re.escape(kw_clean)}(?!\w)", t):
                left_ctx = t[max(0, m.start() - max_window):m.start()]

                # Contexte de préférence et d'achat
                has_favorite_ctx = any(re.search(ctx, left_ctx) for ctx in favorite_context)
                has_purchase_ctx = any(re.search(ctx, left_ctx) for ctx in purchase_context)

                # Si achat explicite sans préférence explicite, ne pas classer en favori
                if has_purchase_ctx and not has_favorite_ctx:
                    continue

                if has_favorite_ctx:
                    piece_is_favorite = True
                    break
            if piece_is_favorite:
                break

        if piece_is_favorite:
            found.append(piece)

    return list(dict.fromkeys(found))

def extract_pieces_recherchees_precise(text: str) -> List[str]:
    """Pièces recherchées = objectif d'achat actuel."""
    purchase_context = [
        r"\bcherche\b", r"\brecherche\b", r"\bvoudrai[st]?\b", r"\bveut\b",
        r"\bbesoin de\b", r"\bvenir acheter\b", r"\bvenu acheter\b",
        r"\bacheter\b", r"\bachat\b", r"\blooking for\b"
    ]
    if not text:
        return []

    t = text.lower()
    found = []
    max_window = 100

    piece_catalog = dict(PIECES_MAPPING)
    piece_catalog["Chaussures"] = ["chaussure", "chaussures", "souliers", "shoes", "footwear"]

    for piece, keywords in piece_catalog.items():
        matched = False
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if len(kw_clean) <= 2 or _is_ambiguous_keyword(kw_clean):
                continue

            # Contexte d'achat AVANT le mot-clé
            for m in re.finditer(rf"(?<!\w){re.escape(kw_clean)}(?!\w)", t):
                left_ctx = t[max(0, m.start() - max_window):m.start()]
                if any(re.search(ctx, left_ctx) for ctx in purchase_context):
                    matched = True
                    break
            if matched:
                break
        if matched:
            found.append(piece)

    return list(dict.fromkeys(found))

def extract_all_tags(text: str) -> Dict[str, Any]:
    """
    FONCTION MAÎTRESSE : Extrait tout en une fraction de seconde.
    """
    cleaned_text = clean_text_turbo(text)

    # Base minimale toujours disponible
    result = {
        "cleaned_text": cleaned_text,
        "age": extract_age_turbo(cleaned_text),
        "budget": extract_budget_turbo(cleaned_text),
        "urgence_score": extract_urgency_turbo(cleaned_text),
    }

    # Taxonomie simple (fallback)
    if not ADVANCED_TAXONOMY_AVAILABLE:
        result.update({
            "profession": scan_text_for_keywords(cleaned_text, PROFESSIONS_MAPPING),
            "ville": scan_text_for_keywords(cleaned_text, CITIES).pop(0) if scan_text_for_keywords(cleaned_text, CITIES) else None,
            "famille": scan_text_for_keywords(cleaned_text, FAMILLE_MAPPING),
            "motif_achat": scan_text_for_keywords(cleaned_text, MOTIF_MAPPING),
            "couleurs": scan_text_for_keywords(cleaned_text, COLORS_MAPPING),
            "matieres": scan_text_for_keywords(cleaned_text, MATERIALS_MAPPING),
            "style": scan_text_for_keywords(cleaned_text, STYLE_MAPPING),
            "centres_interet": scan_text_for_keywords(cleaned_text, LIFESTYLE_MAPPING),
        })
        return result

    # Taxonomie avancée complète
    sport = scan_text_for_keywords_advanced(cleaned_text, SPORT_MAPPING)
    musique = scan_text_for_keywords_advanced(cleaned_text, MUSIQUE_MAPPING)
    animaux = scan_text_for_keywords_advanced(cleaned_text, ANIMAUX_MAPPING)
    voyage = scan_text_for_keywords_advanced(cleaned_text, VOYAGE_MAPPING)
    art_culture = scan_text_for_keywords_advanced(cleaned_text, ART_CULTURE_MAPPING)
    gastronomie = extract_gastronomie_precise(cleaned_text)

    centres_interet = []
    for group in [sport, musique, voyage, art_culture, gastronomie]:
        centres_interet.extend(group)
    centres_interet = list(dict.fromkeys(centres_interet))

    villes_detectees = scan_text_for_keywords_advanced(cleaned_text, CITIES_ADVANCED)

    matieres_detectees = scan_text_for_keywords_advanced(cleaned_text, MATIERES_ADVANCED)
    # Évite le faux positif Denim sur le prénom "Jean"
    if "Denim" in matieres_detectees and not re.search(r"\b(denim|jeans?)\b", cleaned_text.lower()):
        matieres_detectees = [m for m in matieres_detectees if m != "Denim"]

    motifs_precis = extract_motif_precise(cleaned_text)

    pieces_favorites_precise = extract_pieces_favorites_precise(cleaned_text)
    pieces_recherchees_precise = extract_pieces_recherchees_precise(cleaned_text)
    pays_detecte = extract_country_precise(cleaned_text)
    famille_precise = extract_famille_precise(cleaned_text)
    marques_precises = extract_marques_precises(cleaned_text)
    tailles_precises = extract_tailles_precise(cleaned_text)
    if not pays_detecte and villes_detectees:
        city_country_map = {
            "Paris": "France", "Lyon": "France", "Milan": "Italie", "Rome": "Italie",
            "Madrid": "Espagne", "Barcelona": "Espagne", "London": "Royaume-Uni",
            "Berlin": "Allemagne", "Munich": "Allemagne", "Genève": "Suisse",
            "Zurich": "Suisse", "Bruxelles": "Belgique", "New York": "États-Unis",
            "Los Angeles": "États-Unis", "Miami": "États-Unis", "Chicago": "États-Unis",
            "San Francisco": "États-Unis", "Boston": "États-Unis", "Toronto": "Canada",
            "Montreal": "Canada",
        }
        pays_detecte = city_country_map.get(villes_detectees[0])

    result.update({
        # Identité
        "genre": extract_genre_precise(cleaned_text),
        "langue": scan_text_for_keywords_advanced(cleaned_text, LANGUE_MAPPING),
        "statut_client": scan_text_for_keywords_advanced(cleaned_text, STATUT_MAPPING),

        # Démographiques
        "profession": scan_text_for_keywords_advanced(cleaned_text, PROFESSIONS_ADVANCED),
        "ville": villes_detectees[0] if villes_detectees else None,
        "pays": pays_detecte,
        "famille": famille_precise,

        # Lifestyle
        "sport": sport,
        "musique": musique,
        "animaux": animaux,
        "voyage": voyage,
        "art_culture": art_culture,
        "gastronomie": gastronomie,
        "centres_interet": centres_interet,

        # Style
        "pieces_favorites": pieces_favorites_precise,
        "pieces_recherchees": pieces_recherchees_precise,
        "couleurs": scan_text_for_keywords_advanced(cleaned_text, COULEURS_ADVANCED),
        "matieres": matieres_detectees,
        "sensibilite_mode": extract_sensibilite_mode_precise(cleaned_text),
        "tailles": tailles_precises,
        "style": scan_text_for_keywords(cleaned_text, STYLE_MAPPING),

        # Achat
        "motif_achat": motifs_precis if motifs_precis else scan_text_for_keywords_advanced(cleaned_text, MOTIF_ADVANCED),
        "timing": scan_text_for_keywords_advanced(cleaned_text, TIMING_MAPPING),
        "marques_preferees": marques_precises,
        "frequence_achat": scan_text_for_keywords_advanced(cleaned_text, FREQUENCE_ACHAT),

        # Préférences
        "regime": scan_text_for_keywords_advanced(cleaned_text, REGIME_MAPPING),
        "allergies": scan_text_for_keywords_advanced(cleaned_text, ALLERGIES_MAPPING),
        "valeurs": scan_text_for_keywords_advanced(cleaned_text, VALEURS_MAPPING),

        # CRM
        "actions_crm": scan_text_for_keywords_advanced(cleaned_text, ACTIONS_MAPPING),
        "echeances": scan_text_for_keywords_advanced(cleaned_text, ECHEANCES_MAPPING),
        "canaux_contact": extract_canaux_contact_precis(cleaned_text),
    })

    return result

# Test rapide quand exécuté directement
if __name__ == "__main__":
    test = "Je suis avocat à Paris, je cherche un cadeau pour les 30 ans de ma femme. Budget environ 8000€. Elle aime le style chic et le cuir noir. C'est assez urgent pour la semaine prochaine."
    print(extract_all_tags(test))
