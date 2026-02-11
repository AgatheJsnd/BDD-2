"""
Script d'analyse détaillée des résultats de test
"""
import json

# Charger les résultats
with open('test_extraction_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("ANALYSE DÉTAILLÉE DES RÉSULTATS")
print("=" * 80)
print()

# Résumé global
summary = data['summary']
print(f"📊 RÉSUMÉ GLOBAL")
print(f"   Score moyen: {summary['avg_completeness']:.1f}%")
print(f"   Clients traités: {summary['successful']}/{summary['total_clients']}")
print(f"   Erreurs: {summary['errors']}")
print()

# Statistiques par catégorie
categories = {
    'age': 0, 'profession': 0, 'ville': 0, 'famille': 0,
    'budget': 0, 'urgence': 0, 'motif_achat': 0,
    'couleurs': 0, 'matieres': 0, 'style': 0, 'centres_interet': 0
}

for result in data['results']:
    tags = result['tags']
    if tags.get('age'): categories['age'] += 1
    if tags.get('profession'): categories['profession'] += 1
    if tags.get('ville'): categories['ville'] += 1
    if tags.get('famille'): categories['famille'] += 1
    if tags.get('budget'): categories['budget'] += 1
    if tags.get('urgence_score', 0) > 1: categories['urgence'] += 1
    if tags.get('motif_achat'): categories['motif_achat'] += 1
    if tags.get('couleurs'): categories['couleurs'] += 1
    if tags.get('matieres'): categories['matieres'] += 1
    if tags.get('style'): categories['style'] += 1
    if tags.get('centres_interet'): categories['centres_interet'] += 1

total = summary['successful']

print(f"📈 STATISTIQUES PAR CATÉGORIE")
print()
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    pct = (count / total) * 100
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    status = "✅" if pct >= 90 else "⚠️" if pct >= 70 else "❌"
    print(f"   {status} {cat:20s} [{bar}] {count:2d}/{total} ({pct:5.1f}%)")

print()

# Top 5 meilleurs scores
print(f"🏆 TOP 5 MEILLEURS SCORES")
print()
sorted_results = sorted(data['results'], key=lambda x: x['completeness'], reverse=True)
for i, r in enumerate(sorted_results[:5], 1):
    print(f"   {i}. {r['client_id']}: {r['completeness']:.1f}%")

print()

# Détails des villes détectées
print(f"🌍 VILLES DÉTECTÉES")
print()
villes_detectees = []
for result in data['results']:
    if result['tags'].get('ville'):
        villes_detectees.append({
            'client': result['client_id'],
            'ville': result['tags']['ville']
        })

if villes_detectees:
    for v in villes_detectees:
        print(f"   ✅ {v['client']}: {v['ville']}")
else:
    print(f"   ❌ Aucune ville détectée")

print()
print("=" * 80)
