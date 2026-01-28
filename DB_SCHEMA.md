# DB Schema - Profils Clients LVMH (v1 cible)

But: garantir la tracabilite des tags (source + regle) et la reproductibilite des profils.

## Principes
- Chaque tag est lie a une source (CSV, transcription) et a une regle.
- Les profils sont versionnes (snapshot), pas ecrases sans trace.
- Les tables sont normalisees pour audit et evolution.

---

## Tables (cible)

### clients
Identite stable du client.

Champs:
- client_id TEXT PRIMARY KEY
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Contraintes:
- client_id unique

Index:
- idx_clients_updated_at (updated_at)

---

### client_profiles
Snapshot du profil a une date (JSON complet).

Champs:
- profile_id INTEGER PRIMARY KEY AUTOINCREMENT
- client_id TEXT NOT NULL
- profile_version TEXT NOT NULL
- profile_json TEXT NOT NULL
- generated_at TEXT NOT NULL
- source_batch_id TEXT

Contraintes:
- FOREIGN KEY (client_id) REFERENCES clients(client_id)
- UNIQUE (client_id, profile_version)

Index:
- idx_profiles_client_id (client_id)
- idx_profiles_generated_at (generated_at)

---

### sources
Origine des donnees (CSV, transcription, CRM).

Champs:
- source_id INTEGER PRIMARY KEY AUTOINCREMENT
- source_type TEXT NOT NULL  -- csv | transcript | crm | manual
- source_ref TEXT NOT NULL   -- ex: nom_fichier:ligne, transcript_id
- source_hash TEXT NOT NULL  -- checksum pour reproductibilite
- ingested_at TEXT NOT NULL

Contraintes:
- UNIQUE (source_type, source_ref, source_hash)

Index:
- idx_sources_type_ref (source_type, source_ref)

---

### transcripts
Transcriptions clientes (optionnel).

Champs:
- transcript_id INTEGER PRIMARY KEY AUTOINCREMENT
- client_id TEXT NOT NULL
- source_id INTEGER NOT NULL
- language TEXT
- duration TEXT
- text_raw TEXT NOT NULL

Contraintes:
- FOREIGN KEY (client_id) REFERENCES clients(client_id)
- FOREIGN KEY (source_id) REFERENCES sources(source_id)

Index:
- idx_transcripts_client_id (client_id)

---

### tag_rules
Regles de tagging versionnees.

Champs:
- rule_id INTEGER PRIMARY KEY AUTOINCREMENT
- rule_name TEXT NOT NULL
- rule_version TEXT NOT NULL
- rule_definition TEXT NOT NULL  -- JSON ou DSL
- is_active INTEGER NOT NULL     -- 0/1
- created_at TEXT NOT NULL

Contraintes:
- UNIQUE (rule_name, rule_version)

Index:
- idx_rules_active (is_active)

---

### tags
Catalogue des tags (taxonomie).

Champs:
- tag_id INTEGER PRIMARY KEY AUTOINCREMENT
- category TEXT NOT NULL
- subcategory TEXT
- tag_value TEXT NOT NULL
- tag_version TEXT NOT NULL

Contraintes:
- UNIQUE (category, subcategory, tag_value, tag_version)

Index:
- idx_tags_category (category)

---

### taggings
Attribution d'un tag a un client + traceabilite.

Champs:
- tagging_id INTEGER PRIMARY KEY AUTOINCREMENT
- client_id TEXT NOT NULL
- tag_id INTEGER NOT NULL
- rule_id INTEGER NOT NULL
- source_id INTEGER NOT NULL
- score REAL NOT NULL
- evidence TEXT               -- extrait texte / justification
- created_at TEXT NOT NULL

Contraintes:
- FOREIGN KEY (client_id) REFERENCES clients(client_id)
- FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
- FOREIGN KEY (rule_id) REFERENCES tag_rules(rule_id)
- FOREIGN KEY (source_id) REFERENCES sources(source_id)

Index:
- idx_taggings_client_id (client_id)
- idx_taggings_tag_id (tag_id)
- idx_taggings_rule_id (rule_id)

---

### stats_cache
Cache des stats calculees.

Champs:
- stat_name TEXT PRIMARY KEY
- stat_value TEXT NOT NULL
- computed_at TEXT NOT NULL

---

## Mappings essentiels
- Tag = (tags) + (taggings)
- Justification = taggings.evidence + tag_rules.rule_definition
- Profil = clients + client_profiles + taggings
- Audit complet = source + rule + tag

---

## Migration minimale depuis le schema actuel
Schema actuel:
- clients(client_id, date_conversation, duration, language, profile_json)
- tags(client_id, category, subcategory, tag_value)
- statistics(stat_name, stat_value)

Migration cible (resume):
1) Creer les nouvelles tables (clients, client_profiles, sources, transcripts, tag_rules, tags, taggings, stats_cache).
2) Importer clients existants dans clients + client_profiles.
3) Importer tags existants dans tags + taggings (sans rule/source => valeurs "legacy").
4) Deprecier les anciennes tables apres verification.

---

## Decisions a confirmer
- Format exact des timestamps (ISO 8601 recommande).
- Format rule_definition (JSON vs DSL).
- Granularite des sources CSV (fichier entier vs ligne).
