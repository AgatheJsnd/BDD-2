"""
Advanced Tag Extractor - Taxonomie Complète LVMH
Orchestrateur principal pour extraction de 30 catégories
Version 2.0 - Refonte complète
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import des mappings
from mappings.identity import GENRE_MAPPING, LANGUE_MAPPING, STATUT_MAPPING, PROFESSIONS_ADVANCED
from mappings.location import CITIES_ADVANCED
from mappings.lifestyle import SPORT_MAPPING, MUSIQUE_MAPPING, ANIMAUX_MAPPING, VOYAGE_MAPPING, ART_CULTURE_MAPPING, GASTRONOMIE_MAPPING
from mappings.style import PIECES_MAPPING, COULEURS_ADVANCED, MATIERES_ADVANCED, SENSIBILITE_MODE, TAILLES_MAPPING
from mappings.purchase import MOTIF_ADVANCED, TIMING_MAPPING, MARQUES_LVMH, FREQUENCE_ACHAT
from mappings.preferences import REGIME_MAPPING, ALLERGIES_MAPPING, VALEURS_MAPPING
from mappings.tracking import ACTIONS_MAPPING, ECHEANCES_MAPPING, CANAUX_MAPPING

# Import fonction de nettoyage de l'ancien module
from tag_extractor import clean_text_turbo, extract_age_turbo, extract_budget_turbo, extract_urgency_turbo

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def scan_text_for_keywords(text: str, mapping: Dict[str, List[str]]) -> List[str]:
    """Scanne le texte pour trouver les clés correspondantes aux mots-clés"""
    if not text:
        return []
    
    text_lower = text.lower()
    found = []
    
    for category, keywords in mapping.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(category)
                break
                
    return list(set(found))


def scan_nested_mapping(text: str, nested_mapping: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
    """Scanne un mapping imbriqué (ex: CITIES_ADVANCED)"""
    if not text:
        return {}
    
    text_lower = text.lower()
    results = {}
    
    for region, cities in nested_mapping.items():
        found_cities = []
        for city, keywords in cities.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    found_cities.append(city)
                    break
        if found_cities:
            results[region] = found_cities
    
    return results


# ============================================================================
# EXTRACTION AVANCÉE
# ============================================================================

def extract_all_tags_advanced(text: str) -> Dict[str, Any]:
    """
    Extraction complète de la taxonomie LVMH (30 catégories)
    
    Returns:
        dict: Tous les tags extraits selon la taxonomie complète
    """
    
    # Nettoyage du texte
    cleaned = clean_text_turbo(text)
    
    # ========================================================================
    # IDENTITÉ
    # ========================================================================
    genre = scan_text_for_keywords(cleaned, GENRE_MAPPING)
    langue = scan_text_for_keywords(cleaned, LANGUE_MAPPING)
    statut = scan_text_for_keywords(cleaned, STATUT_MAPPING)
    profession = scan_text_for_keywords(cleaned, PROFESSIONS_ADVANCED)
    
    # ========================================================================
    # LOCALISATION
    # ========================================================================
    localisation = scan_nested_mapping(cleaned, CITIES_ADVANCED)
    
    # ========================================================================
    # LIFESTYLE
    # ========================================================================
    sport = scan_text_for_keywords(cleaned, SPORT_MAPPING)
    musique = scan_text_for_keywords(cleaned, MUSIQUE_MAPPING)
    animaux = scan_text_for_keywords(cleaned, ANIMAUX_MAPPING)
    voyage = scan_text_for_keywords(cleaned, VOYAGE_MAPPING)
    art_culture = scan_text_for_keywords(cleaned, ART_CULTURE_MAPPING)
    gastronomie = scan_text_for_keywords(cleaned, GASTRONOMIE_MAPPING)
    
    # ========================================================================
    # STYLE PERSONNEL
    # ========================================================================
    pieces = scan_text_for_keywords(cleaned, PIECES_MAPPING)
    couleurs = scan_text_for_keywords(cleaned, COULEURS_ADVANCED)
    matieres = scan_text_for_keywords(cleaned, MATIERES_ADVANCED)
    sensibilite_mode = scan_text_for_keywords(cleaned, SENSIBILITE_MODE)
    tailles = scan_text_for_keywords(cleaned, TAILLES_MAPPING)
    
    # ========================================================================
    # PROJET D'ACHAT
    # ========================================================================
    motif = scan_text_for_keywords(cleaned, MOTIF_ADVANCED)
    timing = scan_text_for_keywords(cleaned, TIMING_MAPPING)
    marques = scan_text_for_keywords(cleaned, MARQUES_LVMH)
    frequence = scan_text_for_keywords(cleaned, FREQUENCE_ACHAT)
    
    # Réutiliser les fonctions existantes pour âge et budget
    age = extract_age_turbo(cleaned)
    budget = extract_budget_turbo(cleaned)
    urgence_score = extract_urgency_turbo(cleaned)
    
    # ========================================================================
    # PRÉFÉRENCES & CONTRAINTES
    # ========================================================================
    regime = scan_text_for_keywords(cleaned, REGIME_MAPPING)
    allergies = scan_text_for_keywords(cleaned, ALLERGIES_MAPPING)
    valeurs = scan_text_for_keywords(cleaned, VALEURS_MAPPING)
    
    # ========================================================================
    # SUIVI CRM
    # ========================================================================
    actions = scan_text_for_keywords(cleaned, ACTIONS_MAPPING)
    echeances = scan_text_for_keywords(cleaned, ECHEANCES_MAPPING)
    canaux = scan_text_for_keywords(cleaned, CANAUX_MAPPING)
    
    # ========================================================================
    # RÉSULTAT COMPLET
    # ========================================================================
    return {
        # Identité
        "genre": genre[0] if genre else None,
        "langue": langue,
        "statut_client": statut[0] if statut else None,
        "profession": profession,
        
        # Localisation
        "localisation": localisation,
        "ville": next(iter(localisation.values()))[0] if localisation and next(iter(localisation.values())) else None,
        "region": next(iter(localisation.keys())) if localisation else None,
        
        # Démographie (existant)
        "age": age,
        "budget": budget,
        "urgence_score": urgence_score,
        
        # Lifestyle
        "sport": sport,
        "musique": musique,
        "animaux": animaux[0] if animaux else None,
        "voyage": voyage,
        "art_culture": art_culture,
        "gastronomie": gastronomie,
        
        # Style Personnel
        "pieces_favorites": pieces,
        "couleurs": couleurs,
        "matieres": matieres,
        "sensibilite_mode": sensibilite_mode[0] if sensibilite_mode else None,
        "tailles": tailles,
        
        # Projet d'Achat
        "motif_achat": motif,
        "timing": timing[0] if timing else None,
        "marques_preferees": marques,
        "frequence_achat": frequence[0] if frequence else None,
        
        # Préférences
        "regime": regime,
        "allergies": allergies,
        "valeurs": valeurs,
        
        # Suivi CRM
        "actions_crm": actions,
        "echeances": echeances,
        "canaux_contact": canaux,
        
        # Métadonnées
        "cleaned_text": cleaned,
        "extraction_date": datetime.now().isoformat()
    }


def calculate_completeness_advanced(tags: Dict[str, Any]) -> float:
    """
    Calcule le score de complétude pour la taxonomie avancée
    
    Returns:
        float: Score de complétude (0-100%)
    """
    total_categories = 30
    filled_categories = 0
    
    # Vérifier chaque catégorie
    categories_to_check = [
        "genre", "langue", "statut_client", "profession",
        "localisation", "age", "budget", "urgence_score",
        "sport", "musique", "animaux", "voyage", "art_culture", "gastronomie",
        "pieces_favorites", "couleurs", "matieres", "sensibilite_mode", "tailles",
        "motif_achat", "timing", "marques_preferees", "frequence_achat",
        "regime", "allergies", "valeurs",
        "actions_crm", "echeances", "canaux_contact"
    ]
    
    for cat in categories_to_check:
        value = tags.get(cat)
        if value:
            # Vérifier si la valeur n'est pas vide
            if isinstance(value, list) and len(value) > 0:
                filled_categories += 1
            elif isinstance(value, dict) and len(value) > 0:
                filled_categories += 1
            elif isinstance(value, str):
                filled_categories += 1
            elif isinstance(value, (int, float)) and value > 0:
                filled_categories += 1
    
    return (filled_categories / total_categories) * 100
