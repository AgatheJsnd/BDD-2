# BDD-2 - Analyse Données LVMH

Projet d'analyse de données clients LVMH.

## Installation

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

## Structure du projet

```
BDD-2/
├── .venv/              # Environnement virtuel (ignoré par git)
├── .gitignore          # Fichiers à ignorer
├── main.py             # Script principal
├── requirements.txt    # Dépendances Python
├── README.md           # Documentation
└── LVMH_Realistic_Merged_CA001-100.csv  # Données
```

## Données

Le fichier CSV contient 100 transcriptions de rendez-vous clients avec :
- **ID** : Identifiant unique (CA_001 à CA_100)
- **Date** : Date du rendez-vous
- **Duration** : Durée en minutes
- **Language** : Langue (FR, EN, IT, ES, DE)
- **Length** : Catégorie (short, medium, long)
- **Transcription** : Contenu du rendez-vous
