"""
Script principal - Système d'automatisation des profils clients LVMH
"""
from src.csv_processor import CSVProcessor
from src.text_analyzer import TextAnalyzer
from src.tag_engine import TagEngine
from src.profile_generator import ProfileGenerator
from tqdm import tqdm

def main():
    print("=" * 70)
    print("SYSTÈME D'AUTOMATISATION - PROFILS CLIENTS LVMH")
    print("=" * 70)
    print()
    
    # 1. Initialisation des modules
    print("📋 Initialisation des modules...")
    csv_processor = CSVProcessor("LVMH_Realistic_Merged_CA001-100.csv")
    text_analyzer = TextAnalyzer()
    tag_engine = TagEngine()
    profile_generator = ProfileGenerator()
    print()
    
    # 2. Chargement des conversations
    print("📂 Chargement des conversations...")
    conversations = csv_processor.get_conversations()
    print(f"✅ {len(conversations)} conversations chargées")
    print()
    
    # 3. Traitement de chaque conversation
    print("🔍 Analyse et génération des profils...")
    for conversation in tqdm(conversations, desc="Traitement"):
        # Analyser le texte
        analysis = text_analyzer.analyze_full_text(conversation['transcription'])
        
        # Créer le profil
        profile = tag_engine.create_profile(conversation, analysis)
        
        # Sauvegarder le profil
        profile_generator.save_profile(profile)
    
    print()
    print("✅ Tous les profils ont été générés et sauvegardés !")
    print()
    
    # 4. Génération des statistiques
    print("📊 Génération des statistiques...")
    stats = profile_generator.get_statistics()
    profile_generator.save_statistics_report(stats)
    print()
    
    # 5. Affichage du résumé
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Profils créés : {stats['total_clients']}")
    print(f"✅ Base de données : data/profiles.db")
    print(f"✅ Profils JSON : output/profiles_json/")
    print(f"✅ Rapports : output/reports/")
    print()
    
    print("Répartition par statut client :")
    for statut, count in sorted(stats['par_statut'].items(), key=lambda x: x[1], reverse=True):
        percent = (count / stats['total_clients']) * 100
        print(f"  • {statut}: {count} ({percent:.1f}%)")
    print()
    
    print("Top 5 sports mentionnés :")
    top_sports = sorted(stats['sports_populaires'].items(), key=lambda x: x[1], reverse=True)[:5]
    for sport, count in top_sports:
        print(f"  • {sport}: {count} clients")
    print()
    
    print("=" * 70)
    print("✨ Traitement terminé avec succès !")
    print("=" * 70)

if __name__ == "__main__":
    main()
