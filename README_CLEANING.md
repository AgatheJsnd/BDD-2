# 🧹 Nettoyeur de Transcriptions avec Mistral AI

Script Python professionnel pour nettoyer des transcriptions de conversations commerciales en utilisant l'API Mistral AI.

## 📋 Fonctionnalités

- ✅ Suppression des hésitations (euh, hum, ben, etc.)
- ✅ Élimination des répétitions et bégaiements
- ✅ Nettoyage des mots parasites
- ✅ Préservation du sens et du ton original
- ✅ Gestion automatique des erreurs et retry logic
- ✅ Barre de progression en temps réel
- ✅ Support CSV et Excel
- ✅ Statistiques détaillées

## 🚀 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements_cleaning.txt
```

### 2. Configurer la clé API Mistral

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Puis éditez `.env` et ajoutez votre clé API Mistral :

```
MISTRAL_API_KEY=votre_vraie_clé_api_ici
```

**Comment obtenir une clé API Mistral :**
1. Allez sur [console.mistral.ai](https://console.mistral.ai)
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Créez une nouvelle clé

## 📂 Configuration du fichier source

Dans `clean_transcriptions_mistral.py`, modifiez ces variables selon vos besoins :

```python
INPUT_FILE = 'votre_fichier.csv'  # Fichier source
OUTPUT_FILE = 'votre_fichier_cleaned.csv'  # Fichier de sortie
COLUMN_NAME = 'Transcription'  # Nom de la colonne à nettoyer
```

## ▶️ Utilisation

### Lancement simple

```bash
python clean_transcriptions_mistral.py
```

### Exemple de sortie

```
============================================================
🚀 NETTOYEUR DE TRANSCRIPTIONS AVEC MISTRAL AI
============================================================

📂 Chargement de LVMH_Notes_CA101-400.csv...
✅ Fichier chargé : 300 lignes

🤖 Initialisation de Mistral AI (mistral-small-latest)...

🧹 Nettoyage de 300 transcriptions...
Progression: 100%|████████████████████| 300/300 [05:23<00:00,  1.08s/it]

💾 Sauvegarde dans LVMH_Notes_CA101-400_cleaned.csv...
✅ Fichier sauvegardé : LVMH_Notes_CA101-400_cleaned.csv

============================================================
📊 STATISTIQUES DE NETTOYAGE
============================================================
Total de transcriptions : 300
✅ Nettoyées avec succès : 298
⏭️  Ignorées (vides)      : 0
❌ Erreurs              : 2

🎯 Taux de réussite : 99.3%
============================================================

✨ Traitement terminé avec succès !
```

## 🎛️ Options avancées

### Changer le modèle Mistral

Dans le script, modifiez :

```python
MISTRAL_MODEL = 'mistral-large-latest'  # Pour plus de qualité
# ou
MISTRAL_MODEL = 'mistral-small-latest'  # Pour plus de rapidité
```

### Ajuster les paramètres de retry

```python
MAX_RETRIES = 5  # Nombre de tentatives en cas d'échec
RETRY_DELAY = 3  # Délai entre les tentatives (secondes)
```

## 📊 Format des fichiers

### Fichier d'entrée (CSV ou Excel)

Doit contenir au minimum une colonne avec les transcriptions :

| ID | Date | Transcription |
|----|------|---------------|
| CA_001 | 2024-01-15 | Euh... ben je cherche euh un sac... |
| CA_002 | 2024-01-16 | Bonjour, hum, je voudrais... |

### Fichier de sortie

Ajoute une colonne `Transcription_cleaned` :

| ID | Date | Transcription | Transcription_cleaned |
|----|------|---------------|----------------------|
| CA_001 | 2024-01-15 | Euh... ben je cherche euh un sac... | Je cherche un sac. |
| CA_002 | 2024-01-16 | Bonjour, hum, je voudrais... | Bonjour, je voudrais... |

## 🛡️ Gestion des erreurs

Le script gère automatiquement :
- **Rate limiting** : Pause automatique si trop de requêtes
- **Timeouts** : Retry automatique
- **Erreurs API** : Tentatives multiples avec délai exponentiel
- **Textes vides** : Ignorés automatiquement
- **Interruption utilisateur** : Sauvegarde de l'état

## 💡 Conseils d'utilisation

1. **Testez d'abord sur un petit échantillon** (10-20 lignes) pour valider le résultat
2. **Vérifiez votre quota API** Mistral avant de traiter de gros volumes
3. **Sauvegardez votre fichier original** avant traitement
4. **Utilisez `mistral-small`** pour des volumes importants (plus rapide et moins cher)
5. **Utilisez `mistral-large`** pour une qualité maximale sur des textes complexes

## 📝 Structure du code

```
clean_transcriptions_mistral.py
├── Configuration (lignes 1-50)
├── Prompt système (lignes 52-75)
├── Classe TranscriptionCleaner
│   ├── __init__()
│   ├── clean_text()          # Nettoyage d'un texte
│   ├── process_dataframe()   # Traitement du DataFrame
│   └── print_stats()         # Affichage des stats
├── Fonctions utilitaires
│   ├── load_data()           # Chargement CSV/Excel
│   └── save_data()           # Sauvegarde
└── main()                    # Point d'entrée
```

## 🔧 Dépannage

### Erreur : "Clé API manquante"
→ Vérifiez que le fichier `.env` existe et contient `MISTRAL_API_KEY=...`

### Erreur : "Rate limit exceeded"
→ Attendez quelques minutes ou augmentez `RETRY_DELAY`

### Erreur : "Column not found"
→ Vérifiez que `COLUMN_NAME` correspond au nom exact de votre colonne

### Textes trop courts après nettoyage
→ Le script affiche un avertissement. Vérifiez le prompt système.

## 📄 Licence

Ce script est fourni tel quel pour usage professionnel.

## 👨‍💻 Support

Pour toute question, consultez la documentation Mistral AI :
- [Documentation API](https://docs.mistral.ai)
- [Console Mistral](https://console.mistral.ai)
