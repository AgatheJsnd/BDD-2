"""
Script de Simulation Complète - Test sur Base de Données Sale
Exécute le pipeline de nettoyage et génère un rapport détaillé.
"""
import sys
import json
import os
from datetime import datetime
from collections import defaultdict

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.csv_processor import CSVProcessor
from src.text_analyzer import TextAnalyzer
from src.tag_engine import TagEngine
from src.profile_generator import ProfileGenerator


class SimulationReport:
    """Générateur de rapport de simulation"""
    
    def __init__(self):
        self.total_clients = 0
        self.successful = 0
        self.failed = 0
        self.errors = []
        self.warnings = []
        
        # Métriques d'extraction
        self.age_extracted = 0
        self.age_failed = 0
        self.age_failures = []
        
        self.budget_extracted = 0
        self.budget_failed = 0
        self.budget_failures = []
        
        self.city_extracted = 0
        self.city_failed = 0
        
        self.diet_extracted = 0
        self.allergie_extracted = 0
        
        self.sports_found = defaultdict(int)
        self.colors_found = defaultdict(int)
        self.languages_detected = defaultdict(int)
        
        # Problèmes spécifiques
        self.html_detected = 0
        self.emoji_detected = 0
        self.empty_transcriptions = 0
        self.encoding_issues = 0
        self.short_transcriptions = 0
        self.very_long_transcriptions = 0
        
        # Exemples de problèmes
        self.problem_examples = defaultdict(list)
    
    def add_example(self, category: str, example: dict, max_examples: int = 5):
        """Ajoute un exemple de problème (max 5 par catégorie)"""
        if len(self.problem_examples[category]) < max_examples:
            self.problem_examples[category].append(example)
    
    def generate_markdown_report(self) -> str:
        """Génère le rapport en markdown"""
        report = []
        report.append("# 📊 Rapport de Simulation - Base de Données Sale")
        report.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Fichier testé:** `LVMH_Dirty_Database.csv`")
        report.append(f"\n**Total clients traités:** {self.total_clients}")
        
        # Résumé global
        report.append("\n## 📈 Résumé Global")
        report.append(f"| Métrique | Valeur | % |")
        report.append(f"|----------|--------|---|")
        report.append(f"| ✅ Succès | {self.successful} | {self.successful/max(1,self.total_clients)*100:.1f}% |")
        report.append(f"| ❌ Échecs | {self.failed} | {self.failed/max(1,self.total_clients)*100:.1f}% |")
        
        # Extraction d'âge
        report.append("\n## 🎂 Extraction de l'Âge")
        total_age = self.age_extracted + self.age_failed
        report.append(f"| Métrique | Valeur | % |")
        report.append(f"|----------|--------|---|")
        report.append(f"| ✅ Extraits | {self.age_extracted} | {self.age_extracted/max(1,total_age)*100:.1f}% |")
        report.append(f"| ❌ Échecs | {self.age_failed} | {self.age_failed/max(1,total_age)*100:.1f}% |")
        
        if self.age_failures:
            report.append("\n### ⚠️ Exemples d'échecs d'extraction d'âge:")
            for example in self.age_failures[:10]:
                report.append(f"- `{example[:100]}...`" if len(example) > 100 else f"- `{example}`")
        
        # Extraction du budget
        report.append("\n## 💰 Extraction du Budget")
        total_budget = self.budget_extracted + self.budget_failed
        report.append(f"| Métrique | Valeur | % |")
        report.append(f"|----------|--------|---|")
        report.append(f"| ✅ Extraits | {self.budget_extracted} | {self.budget_extracted/max(1,total_budget)*100:.1f}% |")
        report.append(f"| ❌ Échecs | {self.budget_failed} | {self.budget_failed/max(1,total_budget)*100:.1f}% |")
        
        if self.budget_failures:
            report.append("\n### ⚠️ Exemples d'échecs d'extraction de budget:")
            for example in self.budget_failures[:10]:
                report.append(f"- `{example[:100]}...`" if len(example) > 100 else f"- `{example}`")
        
        # Problèmes détectés
        report.append("\n## 🔍 Problèmes Détectés dans les Données")
        report.append(f"| Type de problème | Occurrences |")
        report.append(f"|------------------|-------------|")
        report.append(f"| 🏷️ HTML/Scripts détectés | {self.html_detected} |")
        report.append(f"| 😀 Émojis détectés | {self.emoji_detected} |")
        report.append(f"| 📭 Transcriptions vides | {self.empty_transcriptions} |")
        report.append(f"| 🔤 Problèmes d'encodage | {self.encoding_issues} |")
        report.append(f"| 📝 Transcriptions trop courtes | {self.short_transcriptions} |")
        report.append(f"| 📜 Transcriptions très longues | {self.very_long_transcriptions} |")
        
        # Sports détectés
        report.append("\n## 🏃 Sports Détectés")
        if self.sports_found:
            report.append(f"| Sport | Occurrences |")
            report.append(f"|-------|-------------|")
            for sport, count in sorted(self.sports_found.items(), key=lambda x: -x[1])[:15]:
                report.append(f"| {sport} | {count} |")
        else:
            report.append("*Aucun sport détecté*")
        
        # Couleurs détectées
        report.append("\n## 🎨 Couleurs Détectées")
        if self.colors_found:
            report.append(f"| Couleur | Occurrences |")
            report.append(f"|---------|-------------|")
            for color, count in sorted(self.colors_found.items(), key=lambda x: -x[1])[:15]:
                report.append(f"| {color} | {count} |")
        else:
            report.append("*Aucune couleur détectée*")
        
        # Langues
        report.append("\n## 🌍 Langues Détectées")
        if self.languages_detected:
            report.append(f"| Langue | Occurrences |")
            report.append(f"|--------|-------------|")
            for lang, count in sorted(self.languages_detected.items(), key=lambda x: -x[1]):
                report.append(f"| {lang} | {count} |")
        
        # Exemples de problèmes
        report.append("\n## 📋 Exemples de Problèmes par Catégorie")
        for category, examples in self.problem_examples.items():
            report.append(f"\n### {category}")
            for ex in examples:
                report.append(f"- **Client:** `{ex.get('client_id', 'N/A')}`")
                if 'issue' in ex:
                    report.append(f"  - Issue: `{ex['issue'][:150]}...`" if len(ex.get('issue', '')) > 150 else f"  - Issue: `{ex.get('issue', '')}`")
        
        # Recommandations
        report.append("\n## 💡 Recommandations d'Amélioration")
        report.append(self._generate_recommendations())
        
        # Erreurs critiques
        if self.errors:
            report.append("\n## ❌ Erreurs Critiques")
            for error in self.errors[:20]:
                report.append(f"- `{error}`")
        
        return "\n".join(report)
    
    def _generate_recommendations(self) -> str:
        """Génère les recommandations basées sur les observations"""
        recs = []
        
        # Âge
        if self.age_failed > self.age_extracted:
            recs.append("""
### 1. 🎂 Améliorer l'Extraction de l'Âge
- **Problème:** Plus de 50% des âges n'ont pas été extraits
- **Causes possibles:**
  - Formats textuels ("quarantaine", "mid-thirties")
  - Années de naissance au lieu d'âge direct
  - Formats multilingues (anni, años, Jahre)
- **Solutions proposées:**
  - Ajouter des regex pour les formats textuels français ("la trentaine" → 35)
  - Calculer l'âge depuis l'année de naissance mentionnée
  - Supporter les formats allemand, italien, espagnol
  - Gérer les approximations (~, environ, around)
""")
        
        # Budget
        if self.budget_failed > self.budget_extracted:
            recs.append("""
### 2. 💰 Améliorer l'Extraction du Budget
- **Problème:** Plus de 50% des budgets n'ont pas été extraits
- **Causes possibles:**
  - Formats avec "k" (5k, 10K€)
  - Fourchettes (5000-8000€)
  - Devises multiples ($, £, ¥, €)
  - Formats européens (5.000,00€) vs US (5,000.00$)
- **Solutions proposées:**
  - Ajouter support des abréviations k/K
  - Parser les fourchettes (prendre moyenne ou min)
  - Convertir les devises vers EUR
  - Gérer les séparateurs de milliers européens et US
""")
        
        # HTML/Injection
        if self.html_detected > 0:
            recs.append(f"""
### 3. 🛡️ Sécurité et Nettoyage
- **Problème:** {self.html_detected} transcriptions contiennent du HTML/scripts
- **Risques:** XSS, injection SQL, corruption des données
- **Solutions proposées:**
  - Nettoyer les balises HTML avec `bleach` ou regex
  - Échapper les caractères dangereux
  - Valider les données avant traitement
""")
        
        # Encodage
        if self.encoding_issues > 0:
            recs.append(f"""
### 4. 🔤 Problèmes d'Encodage
- **Problème:** {self.encoding_issues} transcriptions avec encodage corrompu
- **Symptômes:** Caractères comme Ã©, â‚¬
- **Solutions proposées:**
  - Détecter l'encodage automatiquement (chardet)
  - Normaliser vers UTF-8
  - Nettoyer les séquences d'échappement malformées
""")
        
        # Langues mélangées
        multi_lang = sum(1 for l in self.languages_detected if '/' in l or 'MIX' in l.upper())
        if multi_lang > 0:
            recs.append("""
### 5. 🌍 Gestion Multilingue
- **Problème:** Transcriptions avec langues mélangées
- **Solutions proposées:**
  - Implémenter détection de langue automatique (langdetect)
  - Adapter l'analyse selon la langue dominante
  - Maintenir des dictionnaires de mots-clés par langue
""")
        
        # Transcriptions problématiques
        if self.empty_transcriptions > 5 or self.short_transcriptions > 10:
            recs.append(f"""
### 6. 📝 Qualité des Transcriptions
- **Problème:** {self.empty_transcriptions} vides, {self.short_transcriptions} trop courtes
- **Solutions proposées:**
  - Définir un seuil minimum de caractères
  - Marquer les profils "incomplets" pour revue manuelle  
  - Alerter sur les transcriptions sans données exploitables
""")
        
        if not recs:
            recs.append("""
### ✅ Le script gère bien les cas testés !
Quelques améliorations mineures possibles:
- Ajouter plus de logs de debug
- Améliorer la couverture des cas limites
""")
        
        return "\n".join(recs)


def detect_issues(text: str) -> dict:
    """Détecte les problèmes dans une transcription"""
    import re
    issues = {
        'has_html': bool(re.search(r'<[^>]+>', text)),
        'has_emoji': bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]', text)),
        'has_encoding_issues': 'Ã' in text or 'â‚¬' in text or 'Ã©' in text,
        'is_empty': len(text.strip()) < 10,
        'is_short': 10 <= len(text.strip()) < 50,
        'is_very_long': len(text) > 3000,
        'has_sql_injection': 'DROP TABLE' in text.upper() or "'; --" in text,
    }
    return issues


def run_simulation():
    """Exécute la simulation complète"""
    print("=" * 70)
    print("🧪 SIMULATION COMPLÈTE - TEST SUR BASE DE DONNÉES SALE")
    print("=" * 70)
    print()
    
    report = SimulationReport()
    
    # Initialisation des modules
    print("📦 Initialisation des modules...")
    csv_processor = CSVProcessor("LVMH_Dirty_Database.csv")
    text_analyzer = TextAnalyzer()
    tag_engine = TagEngine()
    profile_generator = ProfileGenerator()
    print()
    
    # Chargement des conversations
    print("📂 Chargement des conversations...")
    try:
        conversations = csv_processor.get_conversations()
        report.total_clients = len(conversations)
        print(f"OK - {report.total_clients} conversations chargées")
    except Exception as e:
        print(f"❌ ERREUR lors du chargement: {e}")
        report.errors.append(f"Chargement CSV: {str(e)}")
        return report
    print()
    
    # Traitement de chaque conversation
    print("🔄 Analyse et génération des profils...")
    for i, conversation in enumerate(conversations):
        client_id = conversation.get('client_id', f'UNKNOWN_{i}')
        transcription = conversation.get('transcription', '')
        
        # Détecter les problèmes
        issues = detect_issues(transcription)
        
        if issues['has_html']:
            report.html_detected += 1
            report.add_example("HTML/Script Injection", {
                'client_id': client_id,
                'issue': transcription[:200]
            })
        
        if issues['has_emoji']:
            report.emoji_detected += 1
        
        if issues['has_encoding_issues']:
            report.encoding_issues += 1
            report.add_example("Problèmes d'Encodage", {
                'client_id': client_id,
                'issue': transcription[:200]
            })
        
        if issues['is_empty']:
            report.empty_transcriptions += 1
            report.add_example("Transcription Vide/Quasi-vide", {
                'client_id': client_id,
                'issue': transcription
            })
        elif issues['is_short']:
            report.short_transcriptions += 1
        
        if issues['is_very_long']:
            report.very_long_transcriptions += 1
        
        # Langue
        lang = conversation.get('language', 'UNKNOWN')
        report.languages_detected[lang] += 1
        
        try:
            # Analyser le texte
            analysis = text_analyzer.analyze_full_text(transcription)
            
            # Vérifier extraction d'âge
            if analysis.get('age'):
                report.age_extracted += 1
            else:
                report.age_failed += 1
                # Extraire un aperçu du format d'âge non compris
                import re
                age_patterns = re.findall(r'\d+\s*(?:ans?|years?|anni|años|Jahre)', transcription, re.IGNORECASE)
                vague_patterns = re.findall(r'(?:trentaine|quarantaine|cinquantaine|mid-|early |late )\w*', transcription, re.IGNORECASE)
                if age_patterns:
                    report.age_failures.append(age_patterns[0])
                elif vague_patterns:
                    report.age_failures.append(vague_patterns[0])
                else:
                    # Chercher d'autres formats
                    born_pattern = re.findall(r'(?:né en|born)\s*\d{4}', transcription, re.IGNORECASE)
                    if born_pattern:
                        report.age_failures.append(born_pattern[0])
            
            # Vérifier extraction budget
            if analysis.get('budget'):
                report.budget_extracted += 1
            else:
                report.budget_failed += 1
                # Extraire un aperçu du format budget non compris
                import re
                budget_patterns = re.findall(r'(?:\d+[\d\s,.]*\s*[€$£¥]|[€$£¥]\s*\d+[\d\s,.]*|\d+\s*[kK](?:\s*€)?|budget\s+\w+)', transcription, re.IGNORECASE)
                if budget_patterns:
                    report.budget_failures.append(budget_patterns[0])
            
            # Collecter sports
            for sport in analysis.get('sports', []):
                if sport and sport.lower() not in ['???', 'n/a', '']:
                    report.sports_found[sport] += 1
            
            # Collecter couleurs
            for color in analysis.get('couleurs', []):
                if color and color.lower() not in ['???', 'n/a', '', 'undefined']:
                    report.colors_found[color] += 1
            
            # Créer le profil
            profile = tag_engine.create_profile(conversation, analysis)
            
            # Sauvegarder le profil
            profile_generator.save_profile(profile)
            
            report.successful += 1
            
        except Exception as e:
            report.failed += 1
            report.errors.append(f"Client {client_id}: {str(e)}")
            report.add_example("Erreurs de Traitement", {
                'client_id': client_id,
                'issue': str(e)
            })
        
        # Progress
        if (i + 1) % 25 == 0:
            print(f"   Traité: {i + 1}/{report.total_clients}")
    
    print(f"\n✅ Traitement terminé: {report.successful} succès, {report.failed} échecs")
    print()
    
    # Génération du rapport
    print("📝 Génération du rapport de simulation...")
    markdown_report = report.generate_markdown_report()
    
    # Sauvegarder le rapport
    report_path = "SIMULATION_DIRTY_DATABASE_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"✅ Rapport sauvegardé: {report_path}")
    print()
    
    # Afficher le résumé
    print("=" * 70)
    print("📊 RÉSUMÉ RAPIDE")
    print("=" * 70)
    print(f"Total clients:       {report.total_clients}")
    print(f"Traitement réussi:   {report.successful} ({report.successful/max(1,report.total_clients)*100:.1f}%)")
    print(f"Échecs:              {report.failed} ({report.failed/max(1,report.total_clients)*100:.1f}%)")
    print(f"Âges extraits:       {report.age_extracted}/{report.age_extracted+report.age_failed} ({report.age_extracted/max(1,report.age_extracted+report.age_failed)*100:.1f}%)")
    print(f"Budgets extraits:    {report.budget_extracted}/{report.budget_extracted+report.budget_failed} ({report.budget_extracted/max(1,report.budget_extracted+report.budget_failed)*100:.1f}%)")
    print(f"HTML/Scripts:        {report.html_detected}")
    print(f"Émojis:              {report.emoji_detected}")
    print(f"Problèmes encodage:  {report.encoding_issues}")
    print()
    
    return report


if __name__ == "__main__":
    run_simulation()
