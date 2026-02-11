"""
Module d'authentification pour LVMH Client Analytics
Gestion des utilisateurs et authentification sécurisée
"""
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict

# Chemin vers le fichier des utilisateurs
USERS_FILE = Path(__file__).parent.parent / "config" / "users.json"


def load_users() -> dict:
    """
    Charge les utilisateurs depuis le fichier JSON
    
    Returns:
        dict: Dictionnaire des utilisateurs
    """
    if not USERS_FILE.exists():
        # Créer le fichier avec l'utilisateur par défaut
        default_users = {
            "analyste": {
                "password": hashlib.sha256("analyste123".encode()).hexdigest(),
                "role": "analyste",
                "name": "Data Analyste"
            }
        }
        
        # Créer le dossier config s'il n'existe pas
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, indent=2, ensure_ascii=False)
        
        return default_users
    
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate(username: str, password: str) -> Optional[Dict]:
    """
    Authentifie un utilisateur
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe en clair
    
    Returns:
        dict: Informations utilisateur si authentifié, None sinon
    """
    users = load_users()
    
    if username not in users:
        return None
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if users[username]["password"] == password_hash:
        return {
            "username": username,
            "role": users[username]["role"],
            "name": users[username]["name"]
        }
    
    return None


def get_role_permissions(role: str) -> dict:
    """
    Retourne les permissions selon le rôle
    
    Args:
        role: Role de l'utilisateur (analyste)
    
    Returns:
        dict: Permissions de l'utilisateur
    """
    permissions = {
        "analyste": {
            "view_clients": True,
            "view_recommendations": True,
            "export_client_list": True,
            "view_analytics": True,
            "manage_data": True,
            "advanced_exports": True,
            "studio_builder": True
        }
    }
    
    return permissions.get(role, permissions["analyste"])


def add_user(username: str, password: str, role: str, name: str) -> bool:
    """
    Ajoute un nouvel utilisateur
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe en clair
        role: Rôle de l'utilisateur
        name: Nom complet
    
    Returns:
        bool: True si ajouté avec succès
    """
    users = load_users()
    
    if username in users:
        return False
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    users[username] = {
        "password": password_hash,
        "role": role,
        "name": name
    }
    
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    return True
