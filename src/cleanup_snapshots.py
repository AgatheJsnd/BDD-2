"""
Cleanup script: keep only the latest profile snapshot per client.

Usage:
  python src/cleanup_snapshots.py
  python src/cleanup_snapshots.py data/profiles.db
"""
import sys
import sqlite3


def cleanup(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='client_profiles'"
    )
    if cursor.fetchone() is None:
        conn.close()
        print("Aucune table client_profiles. Rien a nettoyer.")
        return

    # Keep the latest snapshot per client_id (by generated_at, then profile_id)
    cursor.execute(
        """
        DELETE FROM client_profiles
        WHERE profile_id NOT IN (
            SELECT profile_id FROM (
                SELECT
                    profile_id,
                    ROW_NUMBER() OVER (
                        PARTITION BY client_id
                        ORDER BY generated_at DESC, profile_id DESC
                    ) AS rn
                FROM client_profiles
            ) ranked
            WHERE rn = 1
        )
        """
    )

    conn.commit()
    conn.close()
    print("Nettoyage termine: un snapshot conserve par client.")


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/profiles.db"
    cleanup(db_path)
