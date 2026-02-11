# 🎤 Espace Vendeur - Enregistrement Vocal

## 🎯 Vue d'Ensemble

L'espace vendeur vous permet d'enregistrer vos conversations clients et de les transformer automatiquement en données structurées grâce à l'intelligence artificielle.

---

## 🚀 Démarrage Rapide

### 1. Lancer l'application

```bash
streamlit run app.py
```

### 2. Se connecter

```
Utilisateur : vendeur
Mot de passe : vendeur123
```

### 3. Enregistrer une conversation

1. Cliquez sur le micro 🎙️
2. Parlez naturellement
3. Cliquez sur "Transcrire et Analyser"
4. Vérifiez et sauvegardez

---

## 🎤 Comment Ça Marche ?

### Pipeline Automatique

```
Votre Voix
    ↓
🎙️ Enregistrement (Navigateur)
    ↓
🤖 Transcription (Whisper AI)
    ↓
🧹 Nettoyage (Mistral AI)
    ↓
🏷️ Extraction Tags (Python)
    ↓
💾 Sauvegarde
```

### Exemple Concret

**Vous dites :**
> "Euh, j'ai rencontré une cliente de 35 ans qui habite à Paris. Elle cherche un sac pour un mariage. Son budget est de 2000 euros."

**L'IA comprend :**
- 📍 Ville : Paris
- 👤 Âge : 35 ans
- 💰 Budget : 2000€
- 🎁 Motif : mariage
- ⚡ Urgence : 4/5

---

## 📱 Interface

### Onglet 1 : 🎤 Nouvel Enregistrement

**Fonctionnalités :**
- Formulaire client (ID, Nom)
- Bouton d'enregistrement audio
- Lecture de l'enregistrement
- Options de transcription
- Affichage des tags détectés
- Sauvegarde en un clic

### Onglet 2 : 📋 Historique

**Fonctionnalités :**
- Liste de tous vos enregistrements
- Affichage en cartes
- Détails expandables
- Export CSV

### Onglet 3 : ⚙️ Configuration

**Fonctionnalités :**
- Statut des API
- Guide d'utilisation
- Conseils et astuces

---

## 💡 Conseils d'Utilisation

### ✅ À FAIRE

- 🎯 Parlez clairement
- 📍 Mentionnez les informations clés (budget, ville, style)
- 🔇 Enregistrez dans un endroit calme
- ✅ Relisez avant de sauvegarder

### ❌ À ÉVITER

- 🚫 Parler trop vite
- 🚫 Enregistrer dans le bruit
- 🚫 Oublier les détails importants

---

## 🏷️ Tags Détectés Automatiquement

### Informations Client

- 📍 **Ville** : Paris, Lyon, Marseille...
- 👤 **Âge** : 25 ans, 30-35 ans...
- 💼 **Profession** : Avocat, Médecin...
- 👨‍👩‍👧‍👦 **Famille** : Marié, Célibataire, Enfants...

### Achat

- 💰 **Budget** : 500€, 1000-2000€...
- 🎁 **Motif** : Mariage, Anniversaire, Cadeau...
- ⚡ **Urgence** : Score de 1 à 5

### Préférences

- ✨ **Style** : Élégant, Moderne, Classique...
- 🎨 **Couleurs** : Noir, Beige, Rouge...
- 🧵 **Matières** : Cuir, Soie, Coton...
- 🎯 **Centres d'intérêt** : Sport, Voyage, Mode...

---

## 📊 Statistiques

### Dans la Sidebar

- 📈 **Nombre d'enregistrements** : Total de vos enregistrements
- (Plus de stats à venir)

---

## 📥 Export des Données

### Format CSV

Vous pouvez exporter tous vos enregistrements en CSV avec :

- ID Client
- Date et heure
- Transcription brute
- Texte nettoyé
- Tous les tags extraits

**Comment ?**
1. Allez dans l'onglet "📋 Historique"
2. Cliquez sur "📥 Exporter tout en CSV"
3. Le fichier se télécharge automatiquement

---

## 💰 Coûts

### Par Enregistrement (2 minutes)

- Transcription : ~$0.012
- Nettoyage : ~$0.002
- **Total : ~$0.014** (1.4 centimes)

### Pour 100 Enregistrements

- **Total : ~$1.40**

---

## 🔧 Dépannage

### Le micro ne fonctionne pas

**Solutions :**
1. Autorisez l'accès au micro dans votre navigateur
2. Vérifiez que votre micro est branché
3. Essayez Chrome (recommandé)

### "OpenAI API manquante"

**Solutions :**
1. Contactez votre administrateur
2. Vérifiez que la clé est configurée dans `.env`

### La transcription est incorrecte

**Solutions :**
1. Parlez plus clairement
2. Enregistrez dans un endroit plus calme
3. Modifiez manuellement le texte avant de sauvegarder

---

## 📖 Documentation Complète

Pour plus de détails, consultez :

- **`QUICKSTART_VOCAL.md`** : Démarrage rapide
- **`ENREGISTREMENT_VOCAL.md`** : Guide complet
- **`IMPLEMENTATION_VOCAL.md`** : Détails techniques

---

## 🆘 Support

En cas de problème :

1. Consultez l'onglet "⚙️ Configuration"
2. Lisez la documentation
3. Contactez votre administrateur système

---

## 🎓 Formation

### Vidéo Tutoriel (À venir)

Une vidéo de démonstration sera bientôt disponible.

### Session de Formation

Demandez à votre manager d'organiser une session de formation.

---

## 🎉 Avantages

### Pour Vous

- ⏱️ **Gain de temps** : 5 minutes → 30 secondes
- 📝 **Moins de saisie** : Parlez au lieu de taper
- 🎯 **Plus de précision** : L'IA détecte tout
- 📊 **Meilleur suivi** : Historique complet

### Pour l'Entreprise

- 📈 **Données structurées** : Analyse facilitée
- 🎯 **Meilleur ciblage** : Tags précis
- 💰 **ROI amélioré** : Conversions optimisées
- 📊 **Insights** : Tendances identifiées

---

## 🚀 Prochaines Fonctionnalités

### En Développement

- 📧 **Email automatique** : Envoi des résumés
- 📱 **Notifications** : Alertes clients urgents
- 📊 **Dashboard vendeur** : Vos performances
- 🎯 **Recommandations** : Produits suggérés

---

## ✨ Conseils Pro

### Pour de Meilleurs Résultats

1. **Structurez votre discours**
   - Commencez par l'âge et la ville
   - Mentionnez le budget tôt
   - Décrivez les préférences clairement

2. **Soyez précis**
   - "Budget de 2000€" plutôt que "budget moyen"
   - "Style élégant" plutôt que "joli"
   - "Mariage dans 2 semaines" plutôt que "bientôt"

3. **Relisez toujours**
   - Vérifiez la transcription
   - Corrigez les erreurs
   - Ajoutez des détails si besoin

---

**Date de mise à jour** : 11 Février 2026  
**Version** : 1.0  

🎤 **Bon enregistrement !**
