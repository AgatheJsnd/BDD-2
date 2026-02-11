"""
Module d'extraction de tags - Version Python pure "Turbo"
Extrait les tags de la taxonomie LVMH 100% via Algorithme (0% IA)
Optimisé pour la vitesse et la précision des détails.
"""
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

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
    "Cuir": ["cuir", "leather", "veau", "agneau", "vachette"],
    "Cachemire": ["cachemire", "cashmere"],
    "Soie": ["soie", "silk", "satin"],
    "Laine": ["laine", "wool", "mérinos"],
    "Coton": ["coton", "cotton"],
    "Matières_vegan": ["vegan", "végane", "synthétique", "faux cuir", "simili"]
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
    "Casual": ["casual", "décontracté", "cool", "quotidien", "simple", "détente"],
    "Chic": ["chic", "élégant", "soirée", "habillé", "raffiné", "classe"],
    "Business": ["business", "travail", "bureau", "pro", "réunion", "corporate"],
    "Sportswear": ["sportswear", "sport", "athleisure", "sneakers", "baskets"],
    "Haute_couture": ["haute couture", "défilé", "pièce unique", "sur mesure", "exception"]
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
    "Marié(e)": ["marié", "mariée", "mon mari", "ma femme", "époux", "épouse", "married", "husband", "wife"],
    "Couple": ["couple", "copain", "copine", "conjoint", "partenaire", "partner", "boyfriend", "girlfriend"],
    "Avec_enfants": ["enfant", "enfants", "fils", "fille", "bébé", "maman", "papa", "famille", "children", "kids", "son", "daughter"],
    "Célibataire": ["célibataire", "seul", "solo", "single"]
}

# Profession
PROFESSIONS_MAPPING = {
    "Entrepreneur": ["entrepreneur", "chef d'entreprise", "fondateur", "ceo", "business", "start-up"],
    "Cadre": ["cadre", "directeur", "manager", "responsable", "exécutif"],
    "Profession_libérale": ["avocat", "médecin", "architecte", "notaire", "consultant"],
    "Artiste": ["artiste", "designer", "créateur", "musicien", "acteur", "peintre"],
    "Étudiant": ["étudiant", "école", "université", "stage", "stagiaire"]
}

# ============================================================================
# 2. MOTEUR D'EXTRACTION (LE "MUSCLE")
# ============================================================================

def scan_text_for_keywords(text: str, mapping: Dict[str, List[str]]) -> List[str]:
    """Scanne le texte pour trouver les clés correspondantes aux mots-clés"""
    if not text:
        return []
    
    text_lower = text.lower()
    found = []
    
    for category, keywords in mapping.items():
        # Vérification "word boundary" pour éviter les faux positifs (ex: "tour" dans "tourisme")
        for kw in keywords:
            # Recherche simple (plus rapide que regex pour chaque mot)
            # Convertir le keyword en minuscules pour la comparaison
            if kw.lower() in text_lower:
                found.append(category)
                break # On a trouvé cette catégorie, on passe à la suivante
                
    return list(set(found)) # Déduplication

def extract_age_turbo(text: str) -> Optional[str]:
    """Extraction d'âge avancée"""
    if not text: return None
    text_lower = text.lower()
    
    # Regex précises
    patterns = [
        r'\b(\d{2})\s*(?:ans|year|yo|jahre)\b',
        r'\b(\d{2})\s*years?\s*old\b',
        r'\bné[e]?\s*(?:en)?\s*(19\d{2}|20\d{2})\b', # Année naissance
        r'\bage\s*[:]?\s*(\d{2})\b'
    ]
    
    for p in patterns:
        m = re.search(p, text_lower)
        if m:
            val = int(m.group(1))
            if val > 1900: # C'est une année
                val = datetime.now().year - val
            
            # Catégorisation Taxonomie
            if val <= 25: return "18-25"
            if val <= 35: return "26-35"
            if val <= 45: return "36-45"
            if val <= 55: return "46-55"
            return "56+"

    # Mots clés tranches d'âge
    if any(x in text_lower for x in ["vingtaine", "twenties", "etudiant"]): return "18-25"
    if any(x in text_lower for x in ["trentaine", "thirties"]): return "26-35"
    if any(x in text_lower for x in ["quarantaine", "forties"]): return "36-45"
    if any(x in text_lower for x in ["cinquantaine", "fifties"]): return "46-55"
    if any(x in text_lower for x in ["soixantaine", "sixties", "retraité"]): return "56+"
    
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

def extract_urgency_turbo(text: str) -> int:
    """Score d'urgence 1-5 basé sur mots-clés pondérés"""
    score = 1
    text_lower = text.lower()
    
    # Niveau 5 (Critical)
    if any(x in text_lower for x in ["urgent", "demain", "cette semaine", "tout de suite", "immédiat", "asap", "broken", "cassé", "perdu"]):
        return 5
        
    # Niveau 4 (High)
    if any(x in text_lower for x in ["mariage", "anniversaire", "mois prochain", "avant le", "besoin de", "faut que"]):
        score = max(score, 4)
        
    # Niveau 3 (Medium)
    if any(x in text_lower for x in ["cherche", "voudrais", "j'aime", "intéressé", "combien", "stock"]):
        score = max(score, 3)
        
    # Niveau 2 (Low - Exploration)
    if any(x in text_lower for x in ["regarde", "infos", "question", "peut-être", "hésite"]):
        score = max(score, 2)
        
    return score

def extract_all_tags(text: str) -> Dict[str, Any]:
    """
    FONCTION MAÎTRESSE : Extrait tout en une fraction de seconde.
    """
    cleaned_text = clean_text_turbo(text)
    
    return {
        # Texte nettoyé (pour affichage/usage futur)
        "cleaned_text": cleaned_text,
        
        # Données Démographiques
        "age": extract_age_turbo(cleaned_text),
        "profession": scan_text_for_keywords(cleaned_text, PROFESSIONS_MAPPING),
        "ville": scan_text_for_keywords(cleaned_text, CITIES).pop(0) if scan_text_for_keywords(cleaned_text, CITIES) else None,
        "famille": scan_text_for_keywords(cleaned_text, FAMILLE_MAPPING),
        
        # Données Achat
        "budget": extract_budget_turbo(cleaned_text),
        "urgence_score": extract_urgency_turbo(cleaned_text),
        "motif_achat": scan_text_for_keywords(cleaned_text, MOTIF_MAPPING),
        
        # Préférences Produit
        "couleurs": scan_text_for_keywords(cleaned_text, COLORS_MAPPING),
        "matieres": scan_text_for_keywords(cleaned_text, MATERIALS_MAPPING),
        "style": scan_text_for_keywords(cleaned_text, STYLE_MAPPING),
        
        # Lifestyle
        "centres_interet": scan_text_for_keywords(cleaned_text, LIFESTYLE_MAPPING)
    }

# Test rapide quand exécuté directement
if __name__ == "__main__":
    test = "Je suis avocat à Paris, je cherche un cadeau pour les 30 ans de ma femme. Budget environ 8000€. Elle aime le style chic et le cuir noir. C'est assez urgent pour la semaine prochaine."
    print(extract_all_tags(test))
