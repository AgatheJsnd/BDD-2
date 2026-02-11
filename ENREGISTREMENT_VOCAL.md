# 🎤 ENREGISTREMENT VOCAL - GUIDE COMPLET

## ✅ Fonctionnalité Implémentée

L'espace vendeur dispose maintenant d'un système complet d'enregistrement vocal avec transcription IA automatique.

---

## 🚀 Comment ça marche ?

### Pipeline Complet

```
🎙️ Enregistrement Audio
    ↓
🤖 Transcription (Whisper AI)
    ↓
🧹 Nettoyage (Mistral AI)
    ↓
🏷️ Extraction Tags (Python)
    ↓
💾 Sauvegarde
```

---

## 📋 Prérequis

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les nouvelles dépendances ajoutées :
- `streamlit-audiorecorder` : Composant d'enregistrement audio
- `openai` : API Whisper pour la transcription
- `pydub` : Traitement audio

### 2. Configurer les clés API

Éditez le fichier `.env` et ajoutez votre clé OpenAI :

```bash
# Clé API OpenAI (pour Whisper)
OPENAI_API_KEY=sk-votre_clé_ici

# Clé API Mistral (déjà configurée)
MISTRAL_API_KEY=lm9Fxol4pzWCUZwYu0hCnThnCUUN2ZOm
```

**Où obtenir une clé OpenAI ?**
1. Allez sur : https://platform.openai.com/api-keys
2. Créez un compte (ou connectez-vous)
3. Cliquez sur "Create new secret key"
4. Copiez la clé et collez-la dans `.env`

---

## 🎯 Utilisation

### Connexion Vendeur

```
URL : http://localhost:8501
Utilisateur : vendeur
Mot de passe : vendeur123
```

### Interface Vendeur

L'espace vendeur contient **3 onglets** :

#### 1️⃣ Nouvel Enregistrement

**Étapes :**

1. **Informations Client** (optionnel)
   - ID Client : `CLIENT_001`
   - Nom : `Marie Dupont`

2. **Enregistrement Audio**
   - Cliquez sur le micro 🎙️
   - Parlez naturellement
   - Cliquez à nouveau pour arrêter

3. **Options**
   - ✅ Nettoyage automatique (recommandé)
   - 🌍 Langue : Français, Anglais, Espagnol, etc.

4. **Transcription**
   - Cliquez sur "🚀 Transcrire et Analyser"
   - L'IA transforme votre voix en texte
   - Le texte est automatiquement nettoyé

5. **Vérification**
   - Relisez la transcription
   - Modifiez si nécessaire
   - Les tags sont extraits automatiquement

6. **Sauvegarde**
   - Cliquez sur "💾 Sauvegarder"
   - L'enregistrement est ajouté à l'historique

#### 2️⃣ Historique

- 📋 Liste de tous vos enregistrements
- 👁️ Voir les détails de chaque transcription
- 📥 Exporter tout en CSV

#### 3️⃣ Configuration

- 🔑 Status des clés API
- 📖 Guide d'utilisation
- 💡 Conseils et astuces

---

## 🧠 Technologies Utilisées

### 1. Whisper (OpenAI)
- **Rôle** : Transcription vocale
- **Modèle** : `whisper-1`
- **Langues** : Français, Anglais, Espagnol, Italien, Allemand
- **Précision** : ~95% pour le français

### 2. Mistral AI
- **Rôle** : Nettoyage des transcriptions
- **Modèle** : `mistral-small-latest`
- **Actions** :
  - Supprime les "euh", "hum", "ben"
  - Élimine les répétitions
  - Corrige la grammaire
  - Garde le sens exact

### 3. Moteur Python (Tag Extractor)
- **Rôle** : Extraction automatique des tags
- **Tags détectés** :
  - 📍 Ville, Âge, Profession
  - 💰 Budget
  - 🎨 Style, Couleurs, Matières
  - 🎁 Motif d'achat
  - ⚡ Score d'urgence
  - 👨‍👩‍👧‍👦 Famille
  - 🎯 Centres d'intérêt

---

## 💡 Conseils pour de Meilleurs Résultats

### ✅ À FAIRE

- 🎯 Parlez clairement et à un rythme normal
- 📍 Mentionnez les informations clés (budget, style, ville)
- 🔇 Enregistrez dans un endroit calme
- ✅ Relisez toujours avant de sauvegarder
- 💬 Utilisez des phrases complètes

### ❌ À ÉVITER

- 🚫 Parler trop vite
- 🚫 Enregistrer dans un environnement bruyant
- 🚫 Oublier de mentionner les détails importants
- 🚫 Sauvegarder sans relire

---

## 📊 Exemple d'Utilisation

### Scénario : Conversation avec un client

**Vous dites dans le micro :**

> "Bonjour, j'ai rencontré aujourd'hui une cliente de 35 ans qui habite à Paris. Elle cherche un sac à main pour un mariage dans deux semaines. Son budget est d'environ 2000 euros. Elle aime le style élégant et moderne, avec une préférence pour les couleurs neutres comme le beige ou le noir. Elle a mentionné qu'elle adore les sacs en cuir de qualité."

**Résultat après transcription :**

```
Texte nettoyé :
"Bonjour, j'ai rencontré aujourd'hui une cliente de 35 ans qui habite à Paris. 
Elle cherche un sac à main pour un mariage dans deux semaines. Son budget est 
d'environ 2000 euros. Elle aime le style élégant et moderne, avec une préférence 
pour les couleurs neutres comme le beige ou le noir. Elle a mentionné qu'elle 
adore les sacs en cuir de qualité."

Tags extraits :
📍 Ville: Paris
👤 Âge: 35 ans
💰 Budget: 2000€
⚡ Urgence: 4/5
🎁 Motif: mariage
✨ Style: élégant, moderne
🎨 Couleurs: beige, noir
🧵 Matières: cuir
```

---

## 🔧 Dépannage

### Problème : "OpenAI API manquante"

**Solution :**
1. Vérifiez que vous avez ajouté `OPENAI_API_KEY` dans `.env`
2. Redémarrez l'application Streamlit
3. Vérifiez que la clé est valide

### Problème : "Erreur de transcription"

**Solutions possibles :**
- Vérifiez votre connexion internet
- Vérifiez que votre clé OpenAI a des crédits
- Essayez avec un enregistrement plus court
- Vérifiez la qualité de l'audio

### Problème : Le micro ne fonctionne pas

**Solutions :**
- Autorisez l'accès au microphone dans votre navigateur
- Vérifiez que votre micro est branché
- Essayez un autre navigateur (Chrome recommandé)

---

## 📁 Fichiers Créés/Modifiés

### Nouveaux Fichiers

1. **`src/voice_transcriber.py`**
   - Module de transcription vocale
   - Classe `VoiceTranscriber`
   - Fonctions de sauvegarde

### Fichiers Modifiés

1. **`app.py`**
   - Fonction `show_vendeur_interface()` complètement réécrite
   - 3 onglets : Enregistrement, Historique, Configuration

2. **`requirements.txt`**
   - Ajout de `streamlit-audiorecorder`
   - Ajout de `openai`
   - Ajout de `pydub`
   - Ajout de `plotly`

3. **`.env`**
   - Ajout de `OPENAI_API_KEY`

---

## 💰 Coûts

### Whisper (OpenAI)
- **Prix** : $0.006 / minute
- **Exemple** : 
  - 1 minute d'audio = $0.006
  - 100 enregistrements de 2 min = $1.20

### Mistral AI
- **Prix** : ~$0.002 / requête (nettoyage)
- **Exemple** :
  - 100 nettoyages = $0.20

**Total pour 100 enregistrements de 2 min : ~$1.40**

---

## 🎉 Résumé

### ✅ Ce qui fonctionne

- ✅ Enregistrement audio dans le navigateur
- ✅ Transcription automatique avec Whisper
- ✅ Nettoyage automatique avec Mistral AI
- ✅ Extraction automatique des tags
- ✅ Sauvegarde dans la session
- ✅ Historique des enregistrements
- ✅ Export CSV
- ✅ Interface intuitive et moderne

### 🚀 Prochaines Améliorations Possibles

- 📊 Synchronisation avec la base de données
- 📧 Envoi automatique par email
- 📱 Notifications push
- 🔄 Synchronisation cloud
- 📈 Statistiques avancées

---

## 📞 Support

Pour toute question ou problème :
1. Consultez l'onglet "⚙️ Configuration" dans l'espace vendeur
2. Vérifiez que toutes les dépendances sont installées
3. Vérifiez que les clés API sont correctement configurées

---

**Date de création** : 11 Février 2026  
**Version** : 1.0  
**Status** : ✅ Opérationnel
