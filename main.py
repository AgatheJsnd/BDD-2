"""
Script principal - Systeme d'automatisation des profils clients LVMH
"""
from src.csv_processor import CSVProcessor
from src.text_analyzer import TextAnalyzer
from src.tag_engine import TagEngine
from src.profile_generator import ProfileGenerator
from tqdm import tqdm


def main():
    print("=" * 70)
    print("SYSTEME D'AUTOMATISATION - PROFILS CLIENTS LVMH")
    print("=" * 70)
    print()

    import argparse
    
    parser = argparse.ArgumentParser(description="Systeme d'automatisation - Profils Clients LVMH")
    parser.add_argument("--input", default="LVMH_sample_multilang_FULL_cleaned.csv", help="Chemin du fichier CSV d'entrée")
    args = parser.parse_args()

    # 1. Initialisation des modules
    print("Initialisation des modules...")
    # Utilisation du fichier passé en argument ou par défaut
    input_file = args.input
    print(f"Fichier d'entrée : {input_file}")
    
    csv_processor = CSVProcessor(input_file)
    text_analyzer = TextAnalyzer()
    tag_engine = TagEngine()
    profile_generator = ProfileGenerator()
    print()

    # 2. Chargement des conversations
    print("Chargement des conversations...")
    conversations = csv_processor.get_conversations()
    print(f"OK - {len(conversations)} conversations chargees")
    print()

    # 3. Traitement de chaque conversation
    print("Analyse et generation des profils...")
    for conversation in tqdm(conversations, desc="Traitement"):
        # Nettoyage de sécurité (XSS / HTML) avant tout traitement
        if "transcription" in conversation:
            conversation["transcription"] = text_analyzer.clean_text(conversation["transcription"])

        # Analyser le texte
        analysis = text_analyzer.analyze_full_text(conversation["transcription"])

        # Creer le profil
        profile = tag_engine.create_profile(conversation, analysis)

        # Sauvegarder le profil
        profile_generator.save_profile(profile)

    print()
    print("OK - Tous les profils ont ete generes et sauvegardes !")
    print()

    # 4. Generation des statistiques
    print("Generation des statistiques...")
    stats = profile_generator.get_statistics()
    profile_generator.save_statistics_report(stats)
    print()

    # 5. Affichage du resume
    print("=" * 70)
    print("RESUME")
    print("=" * 70)
    print(f"OK - Profils crees : {stats['total_clients']}")
    print("OK - Base de donnees : data/profiles.db")
    print("OK - Profils JSON : output/profiles_json/")
    print("OK - Rapports : output/reports/")
    print()

    print("Repartition par statut client :")
    for statut, count in sorted(stats["par_statut"].items(), key=lambda x: x[1], reverse=True):
        percent = (count / stats["total_clients"]) * 100
        print(f"  - {statut}: {count} ({percent:.1f}%)")
    print()

    print("Top 5 sports mentionnes :")
    top_sports = sorted(stats["sports_populaires"].items(), key=lambda x: x[1], reverse=True)[:5]
    for sport, count in top_sports:
        print(f"  - {sport}: {count} clients")
    print()

    print("=" * 70)
    print("Traitement termine avec succes !")
    print("=" * 70)


if __name__ == "__main__":
    main()
