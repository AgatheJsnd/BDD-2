"""
Script de test pour vérifier l'extraction de tags sur la base de test
"""
import pandas as pd
import sys
import json
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from tag_extractor import extract_all_tags

def test_tag_extraction():
    """Teste l'extraction de tags sur la base de données de test"""
    
    print("=" * 80)
    print("TEST D'EXTRACTION DE TAGS - BASE DE DONNÉES CONNUE")
    print("=" * 80)
    print()
    
    # Charger la base de test
    df = pd.read_csv('test_database_known_tags.csv')
    
    print(f"📊 Base de données chargée: {len(df)} clients")
    print()
    
    results = []
    errors = []
    
    for idx, row in df.iterrows():
        client_id = row['client_id']
        transcription = row['transcription']
        
        print(f"\n{'='*80}")
        print(f"🔍 TEST CLIENT: {client_id}")
        print(f"{'='*80}")
        print(f"\n📝 TRANSCRIPTION:")
        print(f"{transcription[:200]}..." if len(transcription) > 200 else transcription)
        print()
        
        try:
            # Extraire les tags
            tags = extract_all_tags(transcription)
            
            # Afficher les résultats
            print("✅ TAGS EXTRAITS:")
            print(f"   • Âge: {tags.get('age', 'Non détecté')}")
            print(f"   • Profession: {tags.get('profession', [])}")
            print(f"   • Ville: {tags.get('ville', 'Non détecté')}")
            print(f"   • Famille: {tags.get('famille', [])}")
            print(f"   • Budget: {tags.get('budget', 'Non détecté')}")
            print(f"   • Urgence (1-5): {tags.get('urgence_score', 1)}")
            print(f"   • Motif d'achat: {tags.get('motif_achat', [])}")
            print(f"   • Couleurs: {tags.get('couleurs', [])}")
            print(f"   • Matières: {tags.get('matieres', [])}")
            print(f"   • Style: {tags.get('style', [])}")
            print(f"   • Centres d'intérêt: {tags.get('centres_interet', [])}")
            
            # Calculer un score de complétude
            completeness = 0
            total_fields = 11
            
            if tags.get('age'): completeness += 1
            if tags.get('profession'): completeness += 1
            if tags.get('ville'): completeness += 1
            if tags.get('famille'): completeness += 1
            if tags.get('budget'): completeness += 1
            if tags.get('urgence_score', 0) > 1: completeness += 1
            if tags.get('motif_achat'): completeness += 1
            if tags.get('couleurs'): completeness += 1
            if tags.get('matieres'): completeness += 1
            if tags.get('style'): completeness += 1
            if tags.get('centres_interet'): completeness += 1
            
            completeness_pct = (completeness / total_fields) * 100
            
            print(f"\n📈 SCORE DE COMPLÉTUDE: {completeness}/{total_fields} ({completeness_pct:.1f}%)")
            
            results.append({
                'client_id': client_id,
                'completeness': completeness_pct,
                'tags': tags
            })
            
        except Exception as e:
            print(f"❌ ERREUR: {str(e)}")
            errors.append({
                'client_id': client_id,
                'error': str(e)
            })
    
    # Rapport final
    print("\n" + "=" * 80)
    print("📊 RAPPORT FINAL")
    print("=" * 80)
    print()
    
    if results:
        avg_completeness = sum(r['completeness'] for r in results) / len(results)
        print(f"✅ Clients traités avec succès: {len(results)}/{len(df)}")
        print(f"📈 Score moyen de complétude: {avg_completeness:.1f}%")
        print()
        
        # Top 5 meilleurs scores
        print("🏆 TOP 5 MEILLEURS SCORES:")
        sorted_results = sorted(results, key=lambda x: x['completeness'], reverse=True)
        for i, r in enumerate(sorted_results[:5], 1):
            print(f"   {i}. {r['client_id']}: {r['completeness']:.1f}%")
        print()
        
        # Statistiques par catégorie
        print("📊 STATISTIQUES PAR CATÉGORIE:")
        categories = {
            'age': 0, 'profession': 0, 'ville': 0, 'famille': 0,
            'budget': 0, 'urgence': 0, 'motif_achat': 0,
            'couleurs': 0, 'matieres': 0, 'style': 0, 'centres_interet': 0
        }
        
        for r in results:
            tags = r['tags']
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
        
        total = len(results)
        for cat, count in categories.items():
            pct = (count / total) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"   {cat:20s} [{bar}] {count}/{total} ({pct:.1f}%)")
    
    if errors:
        print(f"\n❌ Erreurs rencontrées: {len(errors)}")
        for err in errors:
            print(f"   • {err['client_id']}: {err['error']}")
    
    print("\n" + "=" * 80)
    print("✅ TEST TERMINÉ")
    print("=" * 80)
    
    # Sauvegarder les résultats
    output_file = 'test_extraction_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_clients': len(df),
                'successful': len(results),
                'errors': len(errors),
                'avg_completeness': avg_completeness if results else 0
            },
            'results': results,
            'errors': errors
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés dans: {output_file}")

if __name__ == "__main__":
    test_tag_extraction()
