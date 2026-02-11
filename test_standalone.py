"""
Test Standalone - Extracteur Avancé LVMH
Test direct sans imports complexes
"""

# Copier directement le code nécessaire
import re
from typing import Dict, List, Any
from datetime import datetime
import sys
import os

# Ajouter src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importer les mappings directement
from mappings.identity import GENRE_MAPPING, LANGUE_MAPPING, STATUT_MAPPING, PROFESSIONS_ADVANCED
from mappings.location import CITIES_ADVANCED
from mappings.lifestyle import SPORT_MAPPING, MUSIQUE_MAPPING, ANIMAUX_MAPPING, VOYAGE_MAPPING, ART_CULTURE_MAPPING, GASTRONOMIE_MAPPING
from mappings.style import PIECES_MAPPING, COULEURS_ADVANCED, MATIERES_ADVANCED, SENSIBILITE_MODE, TAILLES_MAPPING
from mappings.purchase import MOTIF_ADVANCED, TIMING_MAPPING, MARQUES_LVMH, FREQUENCE_ACHAT
from mappings.preferences import REGIME_MAPPING, ALLERGIES_MAPPING, VALEURS_MAPPING
from mappings.tracking import ACTIONS_MAPPING, ECHEANCES_MAPPING, CANAUX_MAPPING

# Importer fonctions de base
from tag_extractor import clean_text_turbo, extract_age_turbo, extract_budget_turbo, calculate_urgency_score

# Fonctions utilitaires copiées
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

# Test
print("=" * 80)
print("TEST EXTRACTEUR AVANCÉ - TAXONOMIE COMPLÈTE LVMH")
print("=" * 80)
print()

test_text = """
Bonjour, je suis Marie, une femme de 35 ans, mariée avec deux enfants. 
Je suis avocate à Paris et je parle français et anglais. 
Je suis une cliente fidèle et j'adore le tennis et le yoga.
J'écoute beaucoup de jazz et de musique classique.
J'ai un chien et un chat à la maison.

Je cherche un sac Louis Vuitton en cuir noir, style chic et élégant.
Mon budget est d'environ 3000 euros et c'est assez urgent, j'en ai besoin pour un mariage le mois prochain.
J'aime aussi les pièces en cachemire et les couleurs neutres comme le beige et le gris.

Je suis végétarienne et sensible aux matières éco-responsables.
Je préfère qu'on me contacte par email ou WhatsApp.
J'aimerais une invitation pour la prochaine preview privée.
"""

# Nettoyage
cleaned = clean_text_turbo(test_text)

# Extraction
print("✅ Extraction en cours...")
genre = scan_text_for_keywords(cleaned, GENRE_MAPPING)
langue = scan_text_for_keywords(cleaned, LANGUE_MAPPING)
statut = scan_text_for_keywords(cleaned, STATUT_MAPPING)
profession = scan_text_for_keywords(cleaned, PROFESSIONS_ADVANCED)
localisation = scan_nested_mapping(cleaned, CITIES_ADVANCED)
sport = scan_text_for_keywords(cleaned, SPORT_MAPPING)
musique = scan_text_for_keywords(cleaned, MUSIQUE_MAPPING)
animaux = scan_text_for_keywords(cleaned, ANIMAUX_MAPPING)
pieces = scan_text_for_keywords(cleaned, PIECES_MAPPING)
couleurs = scan_text_for_keywords(cleaned, COULEURS_ADVANCED)
matieres = scan_text_for_keywords(cleaned, MATIERES_ADVANCED)
marques = scan_text_for_keywords(cleaned, MARQUES_LVMH)
regime = scan_text_for_keywords(cleaned, REGIME_MAPPING)
valeurs = scan_text_for_keywords(cleaned, VALEURS_MAPPING)
canaux = scan_text_for_keywords(cleaned, CANAUX_MAPPING)
actions = scan_text_for_keywords(cleaned, ACTIONS_MAPPING)

age = extract_age_turbo(cleaned)
budget = extract_budget_turbo(cleaned)
urgence = calculate_urgency_score(cleaned)

print()
print("📋 RÉSULTATS D'EXTRACTION")
print("=" * 80)
print()
print(f"👤 Genre: {genre}")
print(f"🌍 Langues: {langue}")
print(f"⭐ Statut client: {statut}")
print(f"💼 Profession: {profession}")
print(f"📍 Localisation: {localisation}")
print(f"🎾 Sport: {sport}")
print(f"🎵 Musique: {musique}")
print(f"🐾 Animaux: {animaux}")
print(f"👜 Pièces favorites: {pieces}")
print(f"🎨 Couleurs: {couleurs}")
print(f"🧵 Matières: {matieres}")
print(f"🏷️ Marques LVMH: {marques}")
print(f"🥗 Régime: {regime}")
print(f"💚 Valeurs: {valeurs}")
print(f"📞 Canaux: {canaux}")
print(f"📅 Actions CRM: {actions}")
print()
print(f"📊 Âge: {age}")
print(f"💰 Budget: {budget}")
print(f"⚡ Urgence: {urgence}/5")
print()

# Compter les catégories remplies
categories_filled = sum([
    1 if genre else 0,
    1 if langue else 0,
    1 if statut else 0,
    1 if profession else 0,
    1 if localisation else 0,
    1 if sport else 0,
    1 if musique else 0,
    1 if animaux else 0,
    1 if pieces else 0,
    1 if couleurs else 0,
    1 if matieres else 0,
    1 if marques else 0,
    1 if regime else 0,
    1 if valeurs else 0,
    1 if canaux else 0,
    1 if actions else 0,
    1 if age else 0,
    1 if budget else 0,
    1 if urgence > 0 else 0
])

total_categories = 30
completeness = (categories_filled / total_categories) * 100

print("=" * 80)
print(f"📊 SCORE DE COMPLÉTUDE: {completeness:.1f}% ({categories_filled}/{total_categories} catégories)")
print("=" * 80)
print()
print("✅ Test terminé avec succès!")
