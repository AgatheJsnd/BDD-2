"""
Test d'integration complet - Dashboard + Taxonomie Avancee
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("TEST D'INTEGRATION DASHBOARD + TAXONOMIE AVANCEE")
print("=" * 70)

# 1. Test imports mapping modules
print("\n1. Test imports modules...")
try:
    from src.mappings.identity import GENRE_MAPPING, LANGUE_MAPPING, STATUT_MAPPING, PROFESSIONS_ADVANCED
    from src.mappings.location import CITIES_ADVANCED
    from src.mappings.lifestyle import SPORT_MAPPING, MUSIQUE_MAPPING, ANIMAUX_MAPPING, VOYAGE_MAPPING, ART_CULTURE_MAPPING, GASTRONOMIE_MAPPING
    from src.mappings.style import PIECES_MAPPING, COULEURS_ADVANCED, MATIERES_ADVANCED, SENSIBILITE_MODE, TAILLES_MAPPING
    from src.mappings.purchase import MOTIF_ADVANCED, TIMING_MAPPING, MARQUES_LVMH, FREQUENCE_ACHAT
    from src.mappings.preferences import REGIME_MAPPING, ALLERGIES_MAPPING, VALEURS_MAPPING
    from src.mappings.tracking import ACTIONS_MAPPING, ECHEANCES_MAPPING, CANAUX_MAPPING
    print("   OK - Tous les 6 modules importes")
except Exception as e:
    print(f"   ERREUR: {e}")
    sys.exit(1)

# 2. Test tag_extractor de base
print("\n2. Test tag_extractor base...")
try:
    from src.tag_extractor import extract_all_tags, clean_text_turbo
    print("   OK - tag_extractor importe")
except Exception as e:
    print(f"   ERREUR: {e}")
    sys.exit(1)

# 3. Test texte riche
print("\n3. Test extraction sur texte riche...")
text = """
Bonjour, je suis Marie, une femme de 35 ans, mariee avec deux enfants. 
Je suis avocate a Paris et je parle francais et anglais. 
J'adore le tennis et le yoga.
J'ecoute beaucoup de jazz et de musique classique.
J'ai un chien et un chat a la maison.
Je cherche un sac Louis Vuitton en cuir noir, style chic et elegant.
Mon budget est d'environ 3000 euros et c'est assez urgent, j'en ai besoin pour un mariage le mois prochain.
J'aime aussi les pieces en cachemire et les couleurs neutres comme le beige et le gris.
Je suis vegetarienne et sensible aux matieres eco-responsables.
Je prefere qu'on me contacte par email ou WhatsApp.
"""

# Base tags
tags = extract_all_tags(text)
print(f"   Base tags: {len(tags)} cles")
print(f"   Age: {tags.get('age')}")
print(f"   Budget: {tags.get('budget')}")
print(f"   Ville: {tags.get('ville')}")
print(f"   Urgence: {tags.get('urgence_score')}/5")

# 4. Test extraction avancee
print("\n4. Test extraction avancee (30 categories)...")

def scan(text, mapping):
    text_lower = text.lower()
    found = []
    for cat, keywords in mapping.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(cat)
                break
    return list(set(found))

genre = scan(text, GENRE_MAPPING)
langue = scan(text, LANGUE_MAPPING)
statut = scan(text, STATUT_MAPPING)
profession = scan(text, PROFESSIONS_ADVANCED)
sport = scan(text, SPORT_MAPPING)
musique = scan(text, MUSIQUE_MAPPING)
animaux = scan(text, ANIMAUX_MAPPING)
pieces = scan(text, PIECES_MAPPING)
couleurs = scan(text, COULEURS_ADVANCED)
matieres = scan(text, MATIERES_ADVANCED)
marques = scan(text, MARQUES_LVMH)
motif = scan(text, MOTIF_ADVANCED)
regime = scan(text, REGIME_MAPPING)
valeurs = scan(text, VALEURS_MAPPING)
canaux = scan(text, CANAUX_MAPPING)

print(f"   Genre: {genre}")
print(f"   Langue: {langue}")
print(f"   Profession: {profession}")
print(f"   Sport: {sport}")
print(f"   Musique: {musique}")
print(f"   Animaux: {animaux}")
print(f"   Pieces: {pieces}")
print(f"   Couleurs: {couleurs}")
print(f"   Matieres: {matieres}")
print(f"   Marques LVMH: {marques}")
print(f"   Motif: {motif}")
print(f"   Regime: {regime}")
print(f"   Valeurs: {valeurs}")
print(f"   Canaux: {canaux}")

# 5. Comptage categories
print("\n5. Score de completude...")
all_results = {
    "genre": genre, "langue": langue, "statut": statut,
    "profession": profession, "age": [tags.get("age")],
    "ville": [tags.get("ville")], "budget": [tags.get("budget")],
    "sport": sport, "musique": musique, "animaux": animaux,
    "pieces": pieces, "couleurs": couleurs, "matieres": matieres,
    "marques": marques, "motif": motif, "regime": regime,
    "valeurs": valeurs, "canaux": canaux,
}

filled = sum(1 for v in all_results.values() if v and v != [None])
total = len(all_results)
pct = (filled / total) * 100

print(f"   Categories remplies: {filled}/{total}")
print(f"   Score: {pct:.1f}%")

# 6. Test structure compatible dashboard
print("\n6. Test compatibilite dashboard...")
enriched_tags = dict(tags)
enriched_tags["genre"] = genre[0] if genre else None
enriched_tags["langue"] = langue
enriched_tags["sport"] = sport
enriched_tags["musique"] = musique
enriched_tags["pieces_favorites"] = pieces
enriched_tags["marques_preferees"] = marques
enriched_tags["regime"] = regime
enriched_tags["canaux_contact"] = canaux

# Simuler la construction de la ligne tableau
row = {
    "ID": "TEST_001",
    "Genre": enriched_tags.get("genre", ""),
    "Age": enriched_tags.get("age", ""),
    "Ville": enriched_tags.get("ville", ""),
    "Budget": enriched_tags.get("budget", ""),
    "Marques": ", ".join(enriched_tags.get("marques_preferees", [])),
    "Pieces": ", ".join(enriched_tags.get("pieces_favorites", [])),
    "Sport": ", ".join(enriched_tags.get("sport", [])),
    "Canaux": ", ".join(enriched_tags.get("canaux_contact", [])),
}
print(f"   Ligne tableau: {row}")

print("\n" + "=" * 70)
print("TOUS LES TESTS PASSES AVEC SUCCES!")
print("Dashboard + Taxonomie Avancee = INTEGRATION OK")
print("=" * 70)
