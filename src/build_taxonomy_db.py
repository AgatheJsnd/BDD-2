"""
Script pour construire une base de données dédiée à la taxonomie complète des clients.
Lit les profils JSON et crée une structure tabulaire aplatie pour analyse facile.
"""
import sqlite3
import json
import glob
import os
import pandas as pd
from typing import Dict, Any

DB_PATH = "data/taxonomy.db"
JSON_DIR = "output/profiles_json/"

def flatten_json(y: Dict[str, Any]) -> Dict[str, Any]:
    """Aplatit un objet JSON imbriqué avec des séparateurs _."""
    out = {}

    def flatten(x: Any, name: str = ''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            # Pour les listes, on joint les valeurs par des virgules
            if len(x) > 0:
                out[name[:-1]] = ", ".join([str(i) for i in x])
            else:
                out[name[:-1]] = ""
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def build_database():
    print(f"Création de la base de données taxonomie dans {DB_PATH}...")
    
    # 1. Lire tous les fichiers JSON
    json_files = glob.glob(os.path.join(JSON_DIR, "*.json"))
    if not json_files:
        print("Aucun fichier JSON trouvé. Veuillez exécuter main.py d'abord.")
        return

    all_data = []
    print(f"Traitement de {len(json_files)} profils...")
    
    for fpath in json_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Aplatir le dictionnaire
                flat_data = flatten_json(data)
                
                # S'assurer que client_id est présent
                if 'client_id' not in flat_data and 'id' in data:
                     flat_data['client_id'] = data['id']
                
                all_data.append(flat_data)
        except Exception as e:
            print(f"Erreur avec {fpath}: {e}")

    if not all_data:
        print("Aucune donnée valide extraite.")
        return

    # 2. Convertir en DataFrame pandas
    df = pd.DataFrame(all_data)
    
    # Nettoyer les noms de colonnes (minuscules, pas d'espaces)
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # 3. Sauvegarder en SQLite
    conn = sqlite3.connect(DB_PATH)
    
    # Sauvegarder la table principale
    df.to_sql('client_taxonomy', conn, if_exists='replace', index=False)
    
    # Créer des index sur les colonnes clés
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_client_id ON client_taxonomy(client_id)")
        if 'identite_statut_relationnel' in df.columns:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_statut ON client_taxonomy(identite_statut_relationnel)")
        if 'identite_genre' in df.columns:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON client_taxonomy(identite_genre)")
    except Exception as e:
        print(f"Avertissement index: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"Succès ! Base de données créée avec {len(df)} clients.")
    print(f"Colonnes disponibles ({len(df.columns)}) :")
    for col in list(df.columns)[:10]:
        print(f"  - {col}")
    print("  ...")

    # Export CSV pour vérification rapide
    csv_path = "output/LVMH_Taxonomy_Flat.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';') # excel friendly
    print(f"Export CSV généré : {csv_path}")

if __name__ == "__main__":
    build_database()
