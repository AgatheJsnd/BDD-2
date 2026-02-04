# 🎯 LVMH Client Analytics - Mistral AI

## Description
Application Streamlit automatisée qui analyse les transcriptions clients LVMH avec Mistral AI et génère des insights marketing actionnables.

## ✨ Fonctionnalités

- **Nettoyage IA automatique** : Supprime le bruit, garde l'essentiel
- **Analyse sémantique complète** : Utilise la taxonomie LVMH stricte
- **Insights marketing** : Génère automatiquement :
  - Opportunités de vente
  - Produits recommandés
  - Timing optimal de contact
  - Segments cibles
  - Actions suggérées
- **Export multi-format** : Excel complet + CSV Looker Studio
- **Interface intuitive** : Dashboard Streamlit responsive

## 📋 Prérequis

1. **Python 3.9+**
2. **Clé API Mistral AI** : [Obtenir ici](https://console.mistral.ai/)

## 🚀 Installation

### 1. Installer les dépendances
```bash
cd c:\Users\oanse\OneDrive\Bureau\BDD2\BDD-2
pip install -r requirements.txt
```

### 2. Configurer l'API Mistral
Créez un fichier `.env` :
```bash
MISTRAL_API_KEY=votre_clé_api_ici
```

> **Astuce** : Copiez `.env.example` et renommez-le en `.env`

### 3. Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

## 📊 Utilisation

### Étape 1 : Upload CSV
- Glissez-déposez votre fichier CSV
- Le CSV doit contenir une colonne **"Transcription"**

### Étape 2 : Analyse
- Choisissez le nombre de clients à analyser
- Vérifiez le coût estimé
- Cliquez sur **"🚀 Lancer l'Analyse"**

### Étape 3 : Consulter les résultats
- **Métriques globales** : Urgence moyenne, nombre de tags
- **Détails par client** : Résumé complet, insights marketing
- **Section Looker Studio** : Format copiable pour dashboards

### Étape 4 : Export
- **Excel** : Fichier complet avec toutes les colonnes
- **Looker Studio CSV** : Format optimisé pour import direct

## 📁 Structure des Données

### Colonnes du CSV Export Excel
| Colonne | Description |
|---------|-------------|
| `client_id` | Identifiant unique |
| `resume_complet` | Résumé détaillé de la conversation |
| `resume_court` | Synthèse en 1 phrase |
| `urgency_score` | Score d'urgence (1-5) |
| `tags` | Tags client (séparés par virgule) |
| `opportunites` | Opportunités de vente identifiées |
| `produits_recommandes` | Produits suggérés |
| `actions_suggerees` | Actions marketing à prendre |
| `objections` | Freins à l'achat |
| `looker_studio_summary` | Résumé court (≤100 car) |
| `transcription_nettoyee` | Texte nettoyé par l'IA |

## 💰 Coûts API

**Mistral Large** : ~0.002$ par client analysé (nettoyage + analyse)

Exemple : 
- 10 clients = ~0.02$
- 100 clients = ~0.20$
- 500 clients = ~1.00$

## 🎯 Cas d'Usage

### Import Looker Studio
1. Téléchargez le CSV Looker Studio
2. Dans Looker Studio, créez une nouvelle source de données
3. Importez le CSV
4. Créez vos visualisations :
   - Graphique urgence par segment
   - Top opportunités
   - Distribution des tags

### Workflow Marketing
1. **Analyser** : Upload du CSV quotidien
2. **Prioriser** : Filtrer par urgence ≥ 4
3. **Activer** : Consulter "actions_suggerees"
4. **Mesurer** : Exporter dans CRM/Dashboard

## 🛠️ Troubleshooting

### Erreur "MISTRAL_API_KEY non trouvée"
- Vérifiez que le fichier `.env` existe
- Vérifiez que la clé est correcte
- Redémarrez l'application

### "Colonne Transcription introuvable"
- Vérifiez l'orthographe exacte : `Transcription` (majuscule T)
- Renommez la colonne dans votre CSV si nécessaire

### Timeout API
- Réduisez le nombre de clients à analyser
- Vérifiez votre connexion internet

## 📞 Support

Pour toute question sur la taxonomie LVMH ou les insights générés, consultez `config/taxonomy.py`

## 📝 Exemple de Fichier CSV

```csv
ID,Date,Duration,Language,Length,Transcription
CLIENT_001,2024-01-15,30min,FR,medium,"Cliente VIP à Paris, budget 8000€, cherche sac pour mariage en mars. Urgence élevée."
CLIENT_002,2024-01-16,20min,EN,short,"New client exploring luxury options, no specific budget, just browsing."
```

---

**Développé avec ❤️ pour LVMH**  
Powered by Mistral AI
