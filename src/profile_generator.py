"""
Générateur de profils - Sauvegarde et gestion des profils clients
"""
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
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
        
        # Table clients (stable identity)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        # Snapshots de profils (versionnes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_profiles (
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                profile_version TEXT NOT NULL,
                profile_json TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                source_batch_id TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                UNIQUE (client_id, profile_version)
            )
        ''')

        # Sources de donnees
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                source_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type TEXT NOT NULL,
                source_ref TEXT NOT NULL,
                source_hash TEXT NOT NULL,
                ingested_at TEXT NOT NULL,
                UNIQUE (source_type, source_ref, source_hash)
            )
        ''')

        # Transcriptions (optionnel)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transcripts (
                transcript_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                source_id INTEGER NOT NULL,
                language TEXT,
                duration TEXT,
                text_raw TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                FOREIGN KEY (source_id) REFERENCES sources(source_id)
            )
        ''')

        # Regles de tagging
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag_rules (
                rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT NOT NULL,
                rule_version TEXT NOT NULL,
                rule_definition TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE (rule_name, rule_version)
            )
        ''')

        # Catalogue des tags
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subcategory TEXT,
                tag_value TEXT NOT NULL,
                tag_version TEXT NOT NULL,
                UNIQUE (category, subcategory, tag_value, tag_version)
            )
        ''')

        # Attribution des tags
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS taggings (
                tagging_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                tag_id INTEGER NOT NULL,
                rule_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                score REAL NOT NULL,
                evidence TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                FOREIGN KEY (rule_id) REFERENCES tag_rules(rule_id),
                FOREIGN KEY (source_id) REFERENCES sources(source_id)
            )
        ''')

        # Cache stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats_cache (
                stat_name TEXT PRIMARY KEY,
                stat_value TEXT NOT NULL,
                computed_at TEXT NOT NULL
            )
        ''')

        # Indexes utiles
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_updated_at ON clients(updated_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_profiles_client_id ON client_profiles(client_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_profiles_generated_at ON client_profiles(generated_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sources_type_ref ON sources(source_type, source_ref)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rules_active ON tag_rules(is_active)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_category ON tags(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_client_id ON taggings(client_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_tag_id ON taggings(tag_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_rule_id ON taggings(rule_id)')
        
        conn.commit()
        conn.close()
        print("OK - Base de donnees initialisee")

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _table_exists(self, cursor, table_name: str) -> bool:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return cursor.fetchone() is not None

    def _table_has_column(self, cursor, table_name: str, column_name: str) -> bool:
        cursor.execute(f"PRAGMA table_info({table_name})")
        return column_name in [row[1] for row in cursor.fetchall()]

    def _ensure_default_rule_and_source(self, cursor, profile_json: str):
        now = self._now_iso()
        source_type = "manual"
        source_ref = "profile_generator"
        source_hash = self._hash_text(profile_json)

        cursor.execute('''
            INSERT OR IGNORE INTO sources (source_type, source_ref, source_hash, ingested_at)
            VALUES (?, ?, ?, ?)
        ''', (source_type, source_ref, source_hash, now))
        cursor.execute('''
            SELECT source_id FROM sources
            WHERE source_type = ? AND source_ref = ? AND source_hash = ?
        ''', (source_type, source_ref, source_hash))
        source_id = cursor.fetchone()[0]

        rule_name = "system_default"
        rule_version = "v1"
        rule_definition = "{}"
        cursor.execute('''
            INSERT OR IGNORE INTO tag_rules
            (rule_name, rule_version, rule_definition, is_active, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (rule_name, rule_version, rule_definition, 1, now))
        cursor.execute('''
            SELECT rule_id FROM tag_rules
            WHERE rule_name = ? AND rule_version = ?
        ''', (rule_name, rule_version))
        rule_id = cursor.fetchone()[0]

        return rule_id, source_id
    
    def save_profile(self, profile: Dict):
        """Sauvegarde un profil en base de données et JSON"""
        # Sauvegarder en JSON
        json_path = Path(self.json_dir) / f"{profile['client_id']}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder en base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if self._table_has_column(cursor, "clients", "date_conversation"):
            conn.close()
            raise RuntimeError("Legacy DB schema detected. Run: python src/migrate_db.py")
        
        now = self._now_iso()
        profile_json = json.dumps(profile, ensure_ascii=False)
        profile_version = profile.get('metadata', {}).get('profile_version') or f"v_{now}"

        # Client (identity)
        cursor.execute('''
            INSERT OR IGNORE INTO clients (client_id, created_at, updated_at)
            VALUES (?, ?, ?)
        ''', (profile['client_id'], now, now))
        cursor.execute('''
            UPDATE clients SET updated_at = ? WHERE client_id = ?
        ''', (now, profile['client_id']))

        # Snapshot profil
        cursor.execute('''
            INSERT OR REPLACE INTO client_profiles
            (client_id, profile_version, profile_json, generated_at, source_batch_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (profile['client_id'], profile_version, profile_json, now, None))

        # Source + regle par defaut
        rule_id, source_id = self._ensure_default_rule_and_source(cursor, profile_json)

        # Nettoyer les anciens taggings issus de cette source
        cursor.execute('''
            DELETE FROM taggings WHERE client_id = ? AND rule_id = ? AND source_id = ?
        ''', (profile['client_id'], rule_id, source_id))

        # Insertion des tags
        self._insert_tags(cursor, profile, rule_id, source_id, now)
        
        conn.commit()
        conn.close()
    
    def _insert_tags(self, cursor, profile: Dict, rule_id: int, source_id: int, now: str):
        """Insère tous les tags d'un profil dans les tables tags/taggings"""
        client_id = profile['client_id']
        
        # Parcourir toutes les sections du profil
        for category, content in profile.items():
            if category in ['client_id', 'metadata']:
                continue
            
            self._insert_tags_recursive(cursor, client_id, category, '', content, rule_id, source_id, now)
    
    def _insert_tags_recursive(self, cursor, client_id: str, category: str, subcategory: str, content, rule_id: int, source_id: int, now: str):
        """Insère les tags de manière récursive"""
        if isinstance(content, dict):
            for key, value in content.items():
                new_subcategory = f"{subcategory}/{key}" if subcategory else key
                self._insert_tags_recursive(cursor, client_id, category, new_subcategory, value, rule_id, source_id, now)
        elif isinstance(content, list):
            for item in content:
                tag_id = self._get_or_create_tag_id(cursor, category, subcategory, str(item))
                cursor.execute('''
                    INSERT INTO taggings (client_id, tag_id, rule_id, source_id, score, evidence, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (client_id, tag_id, rule_id, source_id, 1.0, None, now))
        elif content:
            tag_id = self._get_or_create_tag_id(cursor, category, subcategory, str(content))
            cursor.execute('''
                INSERT INTO taggings (client_id, tag_id, rule_id, source_id, score, evidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (client_id, tag_id, rule_id, source_id, 1.0, None, now))

    def _get_or_create_tag_id(self, cursor, category: str, subcategory: str, tag_value: str, tag_version: str = "v1") -> int:
        cursor.execute('''
            INSERT OR IGNORE INTO tags (category, subcategory, tag_value, tag_version)
            VALUES (?, ?, ?, ?)
        ''', (category, subcategory, tag_value, tag_version))
        cursor.execute('''
            SELECT tag_id FROM tags
            WHERE category = ? AND subcategory IS ? AND tag_value = ? AND tag_version = ?
        ''', (category, subcategory, tag_value, tag_version))
        return cursor.fetchone()[0]
    
    def get_profile(self, client_id: str) -> Dict:
        """Récupère un profil par ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if self._table_exists(cursor, "client_profiles"):
            cursor.execute('''
                SELECT profile_json FROM client_profiles
                WHERE client_id = ?
                ORDER BY generated_at DESC, profile_id DESC
                LIMIT 1
            ''', (client_id,))
            result = cursor.fetchone()
            if not result and self._table_has_column(cursor, "clients", "date_conversation"):
                cursor.execute('SELECT profile_json FROM clients WHERE client_id = ?', (client_id,))
                result = cursor.fetchone()
        else:
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
        
        if self._table_exists(cursor, "client_profiles"):
            cursor.execute('''
                SELECT cp.profile_json
                FROM client_profiles cp
                INNER JOIN (
                    SELECT client_id, MAX(generated_at) AS max_generated_at
                    FROM client_profiles
                    GROUP BY client_id
                ) latest
                ON cp.client_id = latest.client_id AND cp.generated_at = latest.max_generated_at
            ''')
            results = cursor.fetchall()
            if not results and self._table_has_column(cursor, "clients", "date_conversation"):
                cursor.execute('SELECT profile_json FROM clients')
                results = cursor.fetchall()
        else:
            cursor.execute('SELECT profile_json FROM clients')
            results = cursor.fetchall()
        
        conn.close()
        
        return [json.loads(row[0]) for row in results]

    # === SQL-first analytics for large datasets ===
    def _count_tags(self, category: str, subcategory: str = None, subcategory_like: str = None, statut: str = None) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT t.tag_value, COUNT(DISTINCT tg.client_id)
            FROM taggings tg
            JOIN tags t ON t.tag_id = tg.tag_id
            WHERE t.category = ?
        """
        params = [category]

        if subcategory is not None:
            sql += " AND t.subcategory = ?"
            params.append(subcategory)
        if subcategory_like is not None:
            sql += " AND t.subcategory LIKE ?"
            params.append(subcategory_like)
        if statut:
            sql += """
                AND EXISTS (
                    SELECT 1
                    FROM taggings tg2
                    JOIN tags t2 ON t2.tag_id = tg2.tag_id
                    WHERE tg2.client_id = tg.client_id
                      AND t2.category = 'identite'
                      AND t2.subcategory = 'statut_relationnel'
                      AND t2.tag_value = ?
                )
            """
            params.append(statut)

        sql += " GROUP BY t.tag_value"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return {k: v for k, v in rows}

    def get_kpis_sql(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM clients")
        total = cursor.fetchone()[0] or 0

        segments = self._count_tags("identite", subcategory="statut_relationnel")
        budgets = self._count_tags("projet_achat", subcategory="budget")
        genres = self._count_tags("identite", subcategory="genre")
        ages = self._count_tags("identite", subcategory="age")

        budget_values = {'<5k': 3000, '5-10k': 7500, '10-15k': 12500, '15-25k': 20000, '25k+': 35000}
        pipeline = sum(budget_values.get(k, 0) * v for k, v in budgets.items())

        vip_count = segments.get('VIP', 0)
        high_value = budgets.get('25k+', 0) + budgets.get('15-25k', 0)

        conn.close()

        return {
            'total': total,
            'segments': segments,
            'budgets': budgets,
            'pipeline': pipeline,
            'avg_basket': pipeline / total if total > 0 else 0,
            'genres': genres,
            'ages': ages,
            'vip_count': vip_count,
            'vip_pct': vip_count / total * 100 if total > 0 else 0,
            'high_value': high_value
        }

    def get_stats_sql(self) -> Dict:
        colors = self._count_tags("style_personnel", subcategory="couleurs_preferees")
        sports = self._count_tags("lifestyle_centres_interet", subcategory_like="sport/%")
        regimes = self._count_tags("metadata_client", subcategory="regime_alimentaire")
        return {
            'couleurs_populaires': colors,
            'sports_populaires': sports,
            'regimes_alimentaires': regimes
        }

    def get_matrix_budget_statut(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.tag_value AS statut, b.tag_value AS budget, COUNT(DISTINCT s_tg.client_id) AS count
            FROM taggings s_tg
            JOIN tags s ON s.tag_id = s_tg.tag_id
            JOIN taggings b_tg ON b_tg.client_id = s_tg.client_id
            JOIN tags b ON b.tag_id = b_tg.tag_id
            WHERE s.category = 'identite' AND s.subcategory = 'statut_relationnel'
              AND b.category = 'projet_achat' AND b.subcategory = 'budget'
            GROUP BY s.tag_value, b.tag_value
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{'statut': r[0], 'budget': r[1], 'count': r[2]} for r in rows]

    def get_top_tags(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.tag_value, COUNT(*) AS cnt
            FROM taggings tg
            JOIN tags t ON t.tag_id = tg.tag_id
            GROUP BY t.tag_value
            ORDER BY cnt DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{'tag': r[0], 'count': r[1]} for r in rows]

    def count_clients(self, statut_list=None, budget_list=None, search: str = None, color: str = None, tag_any: List[str] = None, city: str = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        where = ["1=1"]
        params = []

        if search:
            where.append("c.client_id LIKE ?")
            params.append(f"%{search}%")

        if statut_list:
            placeholders = ",".join(["?"] * len(statut_list))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'identite'
                      AND t.subcategory = 'statut_relationnel'
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(statut_list)

        if budget_list:
            placeholders = ",".join(["?"] * len(budget_list))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'projet_achat'
                      AND t.subcategory = 'budget'
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(budget_list)

        if color:
            where.append("""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'style_personnel'
                      AND t.subcategory = 'couleurs_preferees'
                      AND t.tag_value = ?
                )
            """)
            params.append(color)

        if tag_any:
            placeholders = ",".join(["?"] * len(tag_any))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(tag_any)

        if city:
            where.append("""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'localisation'
                      AND t.tag_value = ?
                )
            """)
            params.append(city)

        sql = f"SELECT COUNT(*) FROM clients c WHERE {' AND '.join(where)}"
        cursor.execute(sql, params)
        total = cursor.fetchone()[0] or 0
        conn.close()
        return total

    def get_client_ids_page(self, statut_list=None, budget_list=None, search: str = None, color: str = None, tag_any: List[str] = None, city: str = None, limit: int = 20, offset: int = 0) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        where = ["1=1"]
        params = []

        if search:
            where.append("c.client_id LIKE ?")
            params.append(f"%{search}%")

        if statut_list:
            placeholders = ",".join(["?"] * len(statut_list))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'identite'
                      AND t.subcategory = 'statut_relationnel'
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(statut_list)

        if budget_list:
            placeholders = ",".join(["?"] * len(budget_list))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'projet_achat'
                      AND t.subcategory = 'budget'
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(budget_list)

        if color:
            where.append("""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'style_personnel'
                      AND t.subcategory = 'couleurs_preferees'
                      AND t.tag_value = ?
                )
            """)
            params.append(color)

        if tag_any:
            placeholders = ",".join(["?"] * len(tag_any))
            where.append(f"""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.tag_value IN ({placeholders})
                )
            """)
            params.extend(tag_any)

        if city:
            where.append("""
                EXISTS (
                    SELECT 1 FROM taggings tg
                    JOIN tags t ON t.tag_id = tg.tag_id
                    WHERE tg.client_id = c.client_id
                      AND t.category = 'localisation'
                      AND t.tag_value = ?
                )
            """)
            params.append(city)

        sql = f"""
            SELECT c.client_id
            FROM clients c
            WHERE {' AND '.join(where)}
            ORDER BY c.client_id
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]

    def get_profiles_by_ids(self, client_ids: List[str]) -> List[Dict]:
        if not client_ids:
            return []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(client_ids))
        sql = f"""
            SELECT cp.client_id, cp.profile_json
            FROM client_profiles cp
            JOIN (
                SELECT client_id, MAX(generated_at) AS max_generated_at
                FROM client_profiles
                GROUP BY client_id
            ) latest
            ON cp.client_id = latest.client_id AND cp.generated_at = latest.max_generated_at
            WHERE cp.client_id IN ({placeholders})
        """
        cursor.execute(sql, client_ids)
        rows = cursor.fetchall()
        conn.close()
        by_id = {r[0]: json.loads(r[1]) for r in rows}
        return [by_id.get(cid) for cid in client_ids if cid in by_id]
    
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

        # Cache stats en DB si disponible
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if self._table_exists(cursor, "stats_cache"):
            now = self._now_iso()
            for k, v in stats.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO stats_cache (stat_name, stat_value, computed_at)
                    VALUES (?, ?, ?)
                ''', (k, json.dumps(v, ensure_ascii=False), now))
            conn.commit()
        conn.close()
        
        print(f"OK - Rapport de statistiques sauvegarde : {report_path}")
        
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
        
        print(f"OK - Rapport textuel sauvegarde : {text_report_path}")
