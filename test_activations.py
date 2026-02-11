"""Test complet du système d'activation client."""
import sys
sys.path.insert(0, 'src')

from activations.extractors import extract_all_actionable
from activations.engine import ActivationEngine

# Simuler des résultats de scan
mock_results = [
    {
        "client_id": "C001",
        "transcription_originale": "Mon anniversaire de mariage est le 12 mai. Je pars a Tokyo le mois prochain pour un voyage d affaires. J ai un sac Louis Vuitton noir en cuir.",
        "cleaned_text": "Mon anniversaire de mariage est le 12 mai. Je pars a Tokyo le mois prochain pour un voyage d affaires. J ai un sac Louis Vuitton noir en cuir.",
        "tags_extracted": {
            "genre": "M", "couleurs": ["noir"], "matieres": ["cuir"],
            "marques_preferees": ["Louis Vuitton"], "pieces_favorites": ["sac"],
            "canaux_contact": ["WhatsApp"], "voyage": ["Tokyo"],
        }
    },
    {
        "client_id": "C002",
        "transcription_originale": "Je cherche un cadeau pour l anniversaire de ma femme. Elle adore le vert emeraude. Vous n avez plus la Speedy en 35? Je suis passionne de champagne.",
        "cleaned_text": "Je cherche un cadeau pour l anniversaire de ma femme. Elle adore le vert emeraude. Vous n avez plus la Speedy en 35? Je suis passionne de champagne.",
        "tags_extracted": {
            "genre": "M", "couleurs": ["vert"], "matieres": [],
            "marques_preferees": [], "pieces_favorites": [],
            "canaux_contact": ["Email"],
        }
    },
    {
        "client_id": "C003",
        "transcription_originale": "J ai achete des souliers Berluti il y a un an. Je vais a un gala la semaine prochaine. J adore l art contemporain.",
        "cleaned_text": "J ai achete des souliers Berluti il y a un an. Je vais a un gala la semaine prochaine. J adore l art contemporain.",
        "tags_extracted": {
            "genre": "M", "couleurs": [], "matieres": ["cuir"],
            "marques_preferees": ["Berluti"], "pieces_favorites": ["chaussures"],
            "canaux_contact": ["Telephone"], "art_culture": ["Art contemporain"],
        }
    },
]

print("=" * 60)
print("TEST 1: Extraction contextuelle")
print("=" * 60)

for r in mock_results:
    extracted = extract_all_actionable(r["cleaned_text"], r["tags_extracted"])
    print(f"\n--- {r['client_id']} ---")
    print(f"  Dates cles: {len(extracted['dates_cles'])}")
    for d in extracted['dates_cles']:
        print(f"    -> {d['type']}: {d.get('date_str', 'N/A')}")
    print(f"  Produits: {len(extracted['produits'])}")
    for p in extracted['produits']:
        print(f"    -> {p['produit']} ({p.get('marque', 'N/A')})")
    print(f"  Projets vie: {len(extracted['projets_vie'])}")
    for p in extracted['projets_vie']:
        print(f"    -> {p['type']}: {p.get('destination', p.get('evenement', 'N/A'))}")
    print(f"  Demandes attente: {len(extracted['demandes_attente'])}")
    for d in extracted['demandes_attente']:
        print(f"    -> {d['produit']} taille {d.get('taille', 'N/A')}")
    print(f"  Affinites cross: {len(extracted['affinites_cross'])}")
    for a in extracted['affinites_cross']:
        print(f"    -> {a['affinite']}: {', '.join(a['maisons_cibles'][:2])}")

print("\n" + "=" * 60)
print("TEST 2: Moteur d'activation")
print("=" * 60)

engine = ActivationEngine(mock_results)
activations = engine.run_all_activations()

print(f"\nTotal activations: {len(activations)}")
print(f"Stats: {engine.stats}")

by_type = engine.get_activations_by_type()
for t, acts in by_type.items():
    print(f"\n  {t}: {len(acts)} activations")
    for a in acts[:2]:
        print(f"    [{a['priority']}] {a['client_id']}: {a['message_vendeur'][:80]}...")

print("\n" + "=" * 60)
print("TEST 3: Brief hebdomadaire")
print("=" * 60)

brief = engine.generate_weekly_brief()
print(brief)

print("\n" + "=" * 60)
print("RESULTAT: SUCCES!")
print("=" * 60)
