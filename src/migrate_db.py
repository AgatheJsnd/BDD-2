"""
Migration script: legacy schema -> new schema with traceability.

Usage:
  python src/migrate_db.py
  python src/migrate_db.py data/profiles.db
"""
import sys
import json
import hashlib
import sqlite3
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def table_exists(cursor, table_name: str) -> bool:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def has_column(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table_name})")
    return column_name in [row[1] for row in cursor.fetchall()]


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_schema(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats_cache (
            stat_name TEXT PRIMARY KEY,
            stat_value TEXT NOT NULL,
            computed_at TEXT NOT NULL
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_updated_at ON clients(updated_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_profiles_client_id ON client_profiles(client_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_profiles_generated_at ON client_profiles(generated_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sources_type_ref ON sources(source_type, source_ref)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_rules_active ON tag_rules(is_active)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_category ON tags(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_client_id ON taggings(client_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_tag_id ON taggings(tag_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_taggings_rule_id ON taggings(rule_id)')


def get_or_create_source(cursor, source_type: str, source_ref: str, source_hash: str, ingested_at: str) -> int:
    cursor.execute('''
        INSERT OR IGNORE INTO sources (source_type, source_ref, source_hash, ingested_at)
        VALUES (?, ?, ?, ?)
    ''', (source_type, source_ref, source_hash, ingested_at))
    cursor.execute('''
        SELECT source_id FROM sources
        WHERE source_type = ? AND source_ref = ? AND source_hash = ?
    ''', (source_type, source_ref, source_hash))
    return cursor.fetchone()[0]


def get_or_create_rule(cursor, rule_name: str, rule_version: str, rule_definition: str, is_active: int) -> int:
    cursor.execute('''
        INSERT OR IGNORE INTO tag_rules
        (rule_name, rule_version, rule_definition, is_active, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (rule_name, rule_version, rule_definition, is_active, now_iso()))
    cursor.execute('''
        SELECT rule_id FROM tag_rules
        WHERE rule_name = ? AND rule_version = ?
    ''', (rule_name, rule_version))
    return cursor.fetchone()[0]


def get_or_create_tag_id(cursor, category: str, subcategory: str, tag_value: str, tag_version: str) -> int:
    cursor.execute('''
        INSERT OR IGNORE INTO tags (category, subcategory, tag_value, tag_version)
        VALUES (?, ?, ?, ?)
    ''', (category, subcategory, tag_value, tag_version))
    cursor.execute('''
        SELECT tag_id FROM tags
        WHERE category = ? AND subcategory IS ? AND tag_value = ? AND tag_version = ?
    ''', (category, subcategory, tag_value, tag_version))
    return cursor.fetchone()[0]


def rename_legacy_tables(cursor):
    if table_exists(cursor, "clients") and has_column(cursor, "clients", "date_conversation"):
        cursor.execute("ALTER TABLE clients RENAME TO legacy_clients")
    if table_exists(cursor, "tags") and has_column(cursor, "tags", "client_id"):
        cursor.execute("ALTER TABLE tags RENAME TO legacy_tags")
    if table_exists(cursor, "statistics"):
        cursor.execute("ALTER TABLE statistics RENAME TO legacy_statistics")


def migrate(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    rename_legacy_tables(cursor)
    create_schema(cursor)

    legacy_clients = table_exists(cursor, "legacy_clients")
    legacy_tags = table_exists(cursor, "legacy_tags")
    legacy_stats = table_exists(cursor, "legacy_statistics")

    client_source_map = {}
    rule_id = get_or_create_rule(cursor, "legacy_import", "v1", "{}", 0)

    if legacy_clients:
        cursor.execute('''
            SELECT client_id, date_conversation, duration, language, profile_json
            FROM legacy_clients
        ''')
        rows = cursor.fetchall()
        for client_id, date_conv, duration, language, profile_json in rows:
            created_at = date_conv or now_iso()
            updated_at = created_at

            cursor.execute('''
                INSERT OR IGNORE INTO clients (client_id, created_at, updated_at)
                VALUES (?, ?, ?)
            ''', (client_id, created_at, updated_at))
            cursor.execute('''
                UPDATE clients SET updated_at = ? WHERE client_id = ?
            ''', (updated_at, client_id))

            cursor.execute('''
                INSERT OR IGNORE INTO client_profiles
                (client_id, profile_version, profile_json, generated_at, source_batch_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_id, "legacy_v1", profile_json, created_at, "legacy_import"))

            source_hash = hash_text(profile_json or "")
            source_id = get_or_create_source(
                cursor,
                "legacy",
                f"legacy_clients:{client_id}",
                source_hash,
                now_iso(),
            )
            client_source_map[client_id] = source_id

            # Optional: preserve transcript metadata in transcripts if desired later

    if legacy_tags:
        cursor.execute('''
            SELECT client_id, category, subcategory, tag_value
            FROM legacy_tags
        ''')
        rows = cursor.fetchall()
        for client_id, category, subcategory, tag_value in rows:
            tag_id = get_or_create_tag_id(cursor, category, subcategory, tag_value, "legacy_v1")
            source_id = client_source_map.get(client_id)
            if source_id is None:
                source_id = get_or_create_source(
                    cursor,
                    "legacy",
                    "legacy_tags",
                    hash_text(f"{client_id}:{category}:{subcategory}:{tag_value}"),
                    now_iso(),
                )
            cursor.execute('''
                INSERT INTO taggings (client_id, tag_id, rule_id, source_id, score, evidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (client_id, tag_id, rule_id, source_id, 1.0, None, now_iso()))

    if legacy_stats:
        cursor.execute('SELECT stat_name, stat_value FROM legacy_statistics')
        rows = cursor.fetchall()
        for stat_name, stat_value in rows:
            cursor.execute('''
                INSERT OR REPLACE INTO stats_cache (stat_name, stat_value, computed_at)
                VALUES (?, ?, ?)
            ''', (stat_name, stat_value, now_iso()))

    conn.commit()
    conn.close()
    print("Migration terminee.")


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/profiles.db"
    migrate(db_path)
