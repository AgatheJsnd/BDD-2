"""
Script de test pour LVMH Client Analytics avec le CSV de 500 clients
Capture toutes les erreurs et génère un rapport
"""
import sys
import traceback
from datetime import datetime
from src.csv_processor import CSVProcessor
from src.text_analyzer import TextAnalyzer
from src.tag_engine import TagEngine
from src.profile_generator import ProfileGenerator
from tqdm import tqdm

def run_test():
    errors = []
    warnings = []
    stats = {
        "total_processed": 0,
        "success": 0,
        "failed": 0,
        "with_warnings": 0,
    }
    
    print("=" * 70)
    print("TEST LVMH CLIENT ANALYTICS - 500 CLIENTS SIMULÉS")
    print("=" * 70)
    print()

    # 1. Initialisation des modules
    print("Initialisation des modules...")
    try:
        csv_processor = CSVProcessor("LVMH_Test_500.csv")
        text_analyzer = TextAnalyzer()
        tag_engine = TagEngine()
        profile_generator = ProfileGenerator(
            db_path="data/test_profiles.db",
            json_dir="output/test_profiles_json"
        )
    except Exception as e:
        errors.append(f"ERREUR INIT: {type(e).__name__}: {e}")
        traceback.print_exc()
        return errors, warnings, stats
    
    print("OK - Modules initialisés")
    print()

    # 2. Chargement des conversations
    print("Chargement des conversations...")
    try:
        conversations = csv_processor.get_conversations()
        print(f"OK - {len(conversations)} conversations chargées")
    except Exception as e:
        errors.append(f"ERREUR CSV: {type(e).__name__}: {e}")
        traceback.print_exc()
        return errors, warnings, stats
    print()

    # 3. Traitement de chaque conversation
    print("Analyse et génération des profils...")
    for i, conversation in enumerate(tqdm(conversations, desc="Traitement")):
        stats["total_processed"] += 1
        client_id = conversation.get("client_id", f"UNKNOWN_{i}")
        
        try:
            # Analyser le texte
            transcription = conversation.get("transcription", "")
            
            if not transcription or len(transcription.strip()) < 5:
                warnings.append(f"{client_id}: Transcription vide ou trop courte")
                stats["with_warnings"] += 1
            
            analysis = text_analyzer.analyze_full_text(transcription)
            
            # Vérifier les résultats d'analyse
            if not analysis.get("budget"):
                warnings.append(f"{client_id}: Budget non extrait")
            if not analysis.get("age"):
                warnings.append(f"{client_id}: Âge non extrait")
            
            # Créer le profil
            profile = tag_engine.create_profile(conversation, analysis)
            
            # Sauvegarder le profil
            profile_generator.save_profile(profile)
            
            stats["success"] += 1
            
        except Exception as e:
            stats["failed"] += 1
            error_msg = f"{client_id}: {type(e).__name__}: {e}"
            errors.append(error_msg)
            # Ne pas arrêter, continuer avec les autres
    
    print()
    print("OK - Traitement terminé")
    print()

    # 4. Génération des statistiques
    print("Génération des statistiques...")
    try:
        final_stats = profile_generator.get_statistics()
        profile_generator.save_statistics_report(final_stats)
    except Exception as e:
        errors.append(f"ERREUR STATS: {type(e).__name__}: {e}")
    print()

    return errors, warnings, stats

def generate_report(errors, warnings, stats):
    """Génère le rapport de test"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Rapport de Test LVMH Client Analytics
Date: {timestamp}

## Résumé
- **Total traité**: {stats['total_processed']}
- **Succès**: {stats['success']}
- **Échecs**: {stats['failed']}
- **Avec avertissements**: {stats['with_warnings']}
- **Taux de succès**: {(stats['success']/max(stats['total_processed'],1))*100:.1f}%

## Erreurs Critiques ({len(errors)})
"""
    
    if errors:
        # Grouper les erreurs par type
        error_types = {}
        for e in errors[:50]:  # Limiter à 50
            error_type = e.split(":")[1].strip() if ":" in e else "Unknown"
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(e)
        
        for error_type, error_list in error_types.items():
            report += f"\n### {error_type} ({len(error_list)} occurrences)\n"
            for e in error_list[:5]:
                report += f"- `{e}`\n"
            if len(error_list) > 5:
                report += f"- ... et {len(error_list) - 5} autres\n"
    else:
        report += "Aucune erreur critique.\n"
    
    report += f"\n## Avertissements (échantillon sur {len(warnings)} total)\n"
    
    if warnings:
        # Grouper par type
        warning_types = {}
        for w in warnings:
            if "Budget non extrait" in w:
                key = "Budget non extrait"
            elif "Âge non extrait" in w:
                key = "Âge non extrait"
            elif "Transcription vide" in w:
                key = "Transcription vide/courte"
            else:
                key = "Autre"
            if key not in warning_types:
                warning_types[key] = 0
            warning_types[key] += 1
        
        for wtype, count in warning_types.items():
            report += f"- **{wtype}**: {count} occurrences\n"
    else:
        report += "Aucun avertissement.\n"
    
    return report

if __name__ == "__main__":
    errors, warnings, stats = run_test()
    report = generate_report(errors, warnings, stats)
    
    # Sauvegarder le rapport
    with open("TEST_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"Total traité: {stats['total_processed']}")
    print(f"Succès: {stats['success']}")
    print(f"Échecs: {stats['failed']}")
    print(f"Avertissements: {len(warnings)}")
    print()
    print(f"Rapport sauvegardé: TEST_REPORT.md")
    print("=" * 70)
