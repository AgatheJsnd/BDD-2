# LVMH Client Analytics

Dashboard interactif pour l'analyse des profils clients LVMH, propulsé par Streamlit et Mistral AI.

## Fonctionnalités
- **Vue d'ensemble** : KPIs et graphiques de distribution.
- **Clients** : Recherche avancée et fiches clients détaillées avec badges (Lifestyle, Style, etc.).
- **Analyses** : Croisement de données (Budget vs Statut, etc.).
- **Actions** : Recommandations marketing et CRM.
- **IA Mistral** : Analyse sémantique des conversations clients.

## Installation

### Prérequis
- Python 3.10+
- Clé API Mistral (pour les fonctionnalités IA)

### 1. Cloner et installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration
Créez un fichier `.env` à la racine du projet et ajoutez votre clé API :
```
MISTRAL_API_KEY=votre_cle_api_ici
```

## Lancement Local

Pour lancer l'application :
```bash
streamlit run app.py
```
Accédez ensuite à `http://localhost:8501`.


## Maintenance DB

### Migration du schema (legacy -> nouveau)
Si la base utilise l'ancien schema, lancer :
```bash
python src/migrate_db.py
```

### Nettoyage des snapshots
Conserver uniquement le dernier profil par client :
```bash
python src/cleanup_snapshots.py
```

## Déploiement Docker

### 1. Construire l'image
```bash
docker build -t lvmh-dashboard .
```

### 2. Lancer le conteneur
```bash
docker run -p 8501:8501 --env-file .env lvmh-dashboard
```

## Structure du Projet
- `app.py` : Point d'entrée de l'application.
- `src/` : Modules de traitement (CSV, Profils, IA).
- `data/` : Base de données SQLite.
- `output/` : Profils JSON générés.
