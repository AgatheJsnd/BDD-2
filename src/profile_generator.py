"""
Générateur de profils - Sauvegarde et gestion des profils clients
"""
import json
import sqlite3
from typing import Dict, List
from pathlib import Path

class ProfileGenerator:
    """Classe pour générer et sauvegarder les profils clients"""
    
    def __init__(self, db_path: str = "data/profiles.db", json_dir: str = "output/profiles_json"):
        self.db_path = db_path
        self.json_dir = json_dir
        self.ensure_directories()
        self.init_database()
    
    def ensure_directories(self):
        """Crée les répertoires nécessaires"""
        Path(self.json_dir).mkdir(parents=True, exist_ok=True)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def init_database(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY,
                date_conversation TEXT,
                duration TEXT,
                language TEXT,
                profile_json TEXT
            )
        ''')
        
        # Table tags
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                category TEXT,
                subcategory TEXT,
                tag_value TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
            )
        ''')
        
        # Table statistiques
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                stat_name TEXT PRIMARY KEY,
                stat_value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de données initialisée")
    
    def save_profile(self, profile: Dict):
        """Sauvegarde un profil en base de données et JSON"""
        # Sauvegarder en JSON
        json_path = Path(self.json_dir) / f"{profile['client_id']}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder en base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insertion client
        cursor.execute('''
            INSERT OR REPLACE INTO clients (client_id, date_conversation, duration, language, profile_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            profile['client_id'],
            profile['metadata'].get('date_conversation', ''),
            profile['metadata'].get('duration', ''),
            profile['metadata'].get('language', ''),
            json.dumps(profile, ensure_ascii=False)
        ))
        
        # Suppression des anciens tags
        cursor.execute('DELETE FROM tags WHERE client_id = ?', (profile['client_id'],))
        
        # Insertion des tags
        self._insert_tags(cursor, profile)
        
        conn.commit()
        conn.close()
    
    def _insert_tags(self, cursor, profile: Dict):
        """Insère tous les tags d'un profil dans la table tags"""
        client_id = profile['client_id']
        
        # Parcourir toutes les sections du profil
        for category, content in profile.items():
            if category in ['client_id', 'metadata']:
                continue
            
            self._insert_tags_recursive(cursor, client_id, category, '', content)
    
    def _insert_tags_recursive(self, cursor, client_id: str, category: str, subcategory: str, content):
        """Insère les tags de manière récursive"""
        if isinstance(content, dict):
            for key, value in content.items():
                new_subcategory = f"{subcategory}/{key}" if subcategory else key
                self._insert_tags_recursive(cursor, client_id, category, new_subcategory, value)
        elif isinstance(content, list):
            for item in content:
                cursor.execute('''
                    INSERT INTO tags (client_id, category, subcategory, tag_value)
                    VALUES (?, ?, ?, ?)
                ''', (client_id, category, subcategory, str(item)))
        elif content:
            cursor.execute('''
                INSERT INTO tags (client_id, category, subcategory, tag_value)
                VALUES (?, ?, ?, ?)
            ''', (client_id, category, subcategory, str(content)))
    
    def get_profile(self, client_id: str) -> Dict:
        """Récupère un profil par ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile_json FROM clients WHERE client_id = ?', (client_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def get_all_profiles(self) -> List[Dict]:
        """Récupère tous les profils"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile_json FROM clients')
        results = cursor.fetchall()
        
        conn.close()
        
        return [json.loads(row[0]) for row in results]
    
    def get_statistics(self) -> Dict:
        """Calcule des statistiques sur tous les profils"""
        profiles = self.get_all_profiles()
        
        stats = {
            'total_clients': len(profiles),
            'par_genre': {},
            'par_age': {},
            'par_statut': {},
            'par_budget': {},
            'sports_populaires': {},
            'couleurs_populaires': {},
            'regimes_alimentaires': {}
        }
        
        for profile in profiles:
            # Genre
            genre = profile.get('identite', {}).get('genre')
            if genre:
                stats['par_genre'][genre] = stats['par_genre'].get(genre, 0) + 1
            
            # Âge
            age = profile.get('identite', {}).get('age')
            if age:
                stats['par_age'][age] = stats['par_age'].get(age, 0) + 1
            
            # Statut
            statut = profile.get('identite', {}).get('statut_relationnel')
            if statut:
                stats['par_statut'][statut] = stats['par_statut'].get(statut, 0) + 1
            
            # Budget
            budget = profile.get('projet_achat', {}).get('budget')
            if budget:
                stats['par_budget'][budget] = stats['par_budget'].get(budget, 0) + 1
            
            # Sports
            sports = profile.get('lifestyle_centres_interet', {}).get('sport', {})
            for sport_type, sport_list in sports.items():
                if isinstance(sport_list, list):
                    for sport in sport_list:
                        stats['sports_populaires'][sport] = stats['sports_populaires'].get(sport, 0) + 1
            
            # Couleurs
            couleurs = profile.get('style_personnel', {}).get('couleurs_preferees', [])
            for couleur in couleurs:
                stats['couleurs_populaires'][couleur] = stats['couleurs_populaires'].get(couleur, 0) + 1
            
            # Régimes
            regime = profile.get('metadata_client', {}).get('regime_alimentaire')
            if regime:
                stats['regimes_alimentaires'][regime] = stats['regimes_alimentaires'].get(regime, 0) + 1
        
        return stats
    
    def save_statistics_report(self, stats: Dict):
        """Sauvegarde un rapport de statistiques"""
        report_path = Path("output/reports/statistics.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Rapport de statistiques sauvegardé : {report_path}")
        
        # Créer également un rapport lisible
        text_report_path = Path("output/reports/statistics.txt")
        with open(text_report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RAPPORT STATISTIQUES - PROFILS CLIENTS LVMH\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total clients : {stats['total_clients']}\n\n")
            
            f.write("Répartition par genre :\n")
            for k, v in sorted(stats['par_genre'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {k}: {v} ({v/stats['total_clients']*100:.1f}%)\n")
            
            f.write("\nRépartition par âge :\n")
            for k, v in sorted(stats['par_age'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {k}: {v} ({v/stats['total_clients']*100:.1f}%)\n")
            
            f.write("\nRépartition par statut :\n")
            for k, v in sorted(stats['par_statut'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {k}: {v} ({v/stats['total_clients']*100:.1f}%)\n")
            
            f.write("\nTop 5 sports :\n")
            top_sports = sorted(stats['sports_populaires'].items(), key=lambda x: x[1], reverse=True)[:5]
            for sport, count in top_sports:
                f.write(f"  - {sport}: {count} clients\n")
            
            f.write("\nTop 5 couleurs :\n")
            top_couleurs = sorted(stats['couleurs_populaires'].items(), key=lambda x: x[1], reverse=True)[:5]
            for couleur, count in top_couleurs:
                f.write(f"  - {couleur}: {count} clients\n")
            
            f.write("\nRégimes alimentaires :\n")
            for k, v in sorted(stats['regimes_alimentaires'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {k}: {v} clients\n")
        
        print(f"✅ Rapport textuel sauvegardé : {text_report_path}")
