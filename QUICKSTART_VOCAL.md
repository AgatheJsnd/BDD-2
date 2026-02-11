# 🚀 DÉMARRAGE RAPIDE - Enregistrement Vocal

## ⚡ Installation Express (5 minutes)

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurer OpenAI

Éditez le fichier `.env` et ajoutez votre clé :

```bash
OPENAI_API_KEY=sk-votre_clé_ici
```

**Obtenir une clé OpenAI :**
👉 https://platform.openai.com/api-keys

### 3️⃣ Lancer l'application

```bash
streamlit run app.py
```

### 4️⃣ Se connecter

```
URL : http://localhost:8501
Utilisateur : vendeur
Mot de passe : vendeur123
```

---

## 🎤 Utilisation Rapide

1. **Cliquez sur le micro** 🎙️
2. **Parlez** : "Client de 30 ans, Paris, budget 1500€, cherche un sac élégant"
3. **Cliquez sur "Transcrire"**
4. **Vérifiez** le texte
5. **Sauvegardez** ✅

---

## ✅ Checklist

- [ ] `pip install -r requirements.txt` exécuté
- [ ] `OPENAI_API_KEY` ajoutée dans `.env`
- [ ] Application lancée avec `streamlit run app.py`
- [ ] Connexion avec `vendeur / vendeur123`
- [ ] Premier enregistrement testé

---

## 🆘 Problèmes Courants

### "OpenAI API manquante"
➡️ Vérifiez que `OPENAI_API_KEY` est dans `.env`

### "Module not found"
➡️ Relancez `pip install -r requirements.txt`

### Le micro ne marche pas
➡️ Autorisez l'accès au micro dans votre navigateur

---

## 📖 Documentation Complète

Consultez `ENREGISTREMENT_VOCAL.md` pour :
- Guide détaillé
- Exemples d'utilisation
- Dépannage avancé
- Coûts et optimisation

---

**Prêt en 5 minutes ! 🚀**
