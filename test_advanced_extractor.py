"""
Script de test pour l'extracteur avancé
Test rapide de la taxonomie complète LVMH
"""

import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import direct depuis src
import advanced_extractor

# Test avec un exemple riche
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

print("=" * 80)
print("TEST EXTRACTEUR AVANCÉ - TAXONOMIE COMPLÈTE LVMH")
print("=" * 80)
print()

# Extraction
tags = advanced_extractor.extract_all_tags_advanced(test_text)

# Affichage des résultats par catégorie
print("📋 IDENTITÉ")
print(f"  Genre: {tags.get('genre')}")
print(f"  Langues: {tags.get('langue')}")
print(f"  Statut client: {tags.get('statut_client')}")
print(f"  Profession: {tags.get('profession')}")
print()

print("📍 LOCALISATION")
print(f"  Région: {tags.get('region')}")
print(f"  Ville: {tags.get('ville')}")
print(f"  Détails: {tags.get('localisation')}")
print()

print("👤 DÉMOGRAPHIE")
print(f"  Âge: {tags.get('age')}")
print(f"  Budget: {tags.get('budget')}")
print(f"  Urgence: {tags.get('urgence_score')}/5")
print()

print("🎯 LIFESTYLE")
print(f"  Sport: {tags.get('sport')}")
print(f"  Musique: {tags.get('musique')}")
print(f"  Animaux: {tags.get('animaux')}")
print(f"  Voyage: {tags.get('voyage')}")
print(f"  Art & Culture: {tags.get('art_culture')}")
print(f"  Gastronomie: {tags.get('gastronomie')}")
print()

print("👔 STYLE PERSONNEL")
print(f"  Pièces favorites: {tags.get('pieces_favorites')}")
print(f"  Couleurs: {tags.get('couleurs')}")
print(f"  Matières: {tags.get('matieres')}")
print(f"  Sensibilité mode: {tags.get('sensibilite_mode')}")
print(f"  Tailles: {tags.get('tailles')}")
print()

print("🛍️ PROJET D'ACHAT")
print(f"  Motif: {tags.get('motif_achat')}")
print(f"  Timing: {tags.get('timing')}")
print(f"  Marques préférées: {tags.get('marques_preferees')}")
print(f"  Fréquence: {tags.get('frequence_achat')}")
print()

print("⚙️ PRÉFÉRENCES")
print(f"  Régime: {tags.get('regime')}")
print(f"  Allergies: {tags.get('allergies')}")
print(f"  Valeurs: {tags.get('valeurs')}")
print()

print("📞 SUIVI CRM")
print(f"  Actions: {tags.get('actions_crm')}")
print(f"  Échéances: {tags.get('echeances')}")
print(f"  Canaux: {tags.get('canaux_contact')}")
print()

# Score de complétude
completeness = advanced_extractor.calculate_completeness_advanced(tags)
print("=" * 80)
print(f"📊 SCORE DE COMPLÉTUDE: {completeness:.1f}%")
print("=" * 80)
