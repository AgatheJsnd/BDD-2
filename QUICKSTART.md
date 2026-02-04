# 🚀 Guide de Démarrage Rapide - 3 Minutes Chrono

## Étape 1 : Installation (1 min)

Ouvrez PowerShell et tapez :

```powershell
cd c:\Users\oanse\OneDrive\Bureau\BDD2\BDD-2
pip install -r requirements.txt
```

## Étape 2 : Configuration API (30 secondes)

1. Obtenez votre clé API Mistral : https://console.mistral.ai/
2. Créez un fichier `.env` dans le dossier du projet
3. Ajoutez dedans :
   ```
   MISTRAL_API_KEY=votre_clé_ici
   ```

## Étape 3 : Lancer l'App (10 secondes)

```powershell
streamlit run app.py
```

Votre navigateur s'ouvre automatiquement sur `http://localhost:8501` !

## Étape 4 : Premier Test (1 min)

1. **Upload** : Glissez `LVMH_Dirty_Database.csv`
2. **Analysez** : Sélectionnez 5 clients → Cliquez "Lancer l'Analyse"
3. **Explorez** : Ouvrez un client → Lisez les insights marketing
4. **Exportez** : Téléchargez l'Excel

---

## 📊 Ce que vous verrez

### Dashboard Principal
- 📈 Métriques : Nombre clients, urgence moyenne, tags
- 🔍 Détails par client avec insights marketing
- 💡 Suggestions d'actions générées par l'IA

### Pour Chaque Client
```
📝 Résumé Complet : "Cliente VIP à Paris, 35 ans, entrepreneur..."

🏷️ Tags : Paris | 5-10k | Business | Noir | Urgent

💡 Insights Marketing :
  • Opportunités : "Sac business premium pour voyages"
  • Produits : "Sac cabine cuir noir", "Porte-documents"
  • Timing : "Contacter cette semaine - mariage dans 2 mois"
  • Actions : "Proposer preview privée", "Organiser essayage"

⚠️ Objections : "Budget serré pour événement"

📊 Looker Studio : CLIENT_001 | VIP Paris urgence mariage | 4/5
```

### Exports

**Excel** : Fichier complet avec toutes les colonnes
```
client_id | resume_complet | urgency_score | tags | opportunites | ...
```

**Looker Studio CSV** : Format optimisé pour dashboards
```
Client_ID | Resume | Urgence | Tags | Segment
```

---

## 🎯 Prochaines Étapes selon vos Besoins

### Scénario A : Analytics Quotidien
1. Upload CSV export CRM du jour
2. Analysez tous les nouveaux clients
3. Filtrez urgence ≥ 4
4. Exportez actions suggérées → Envoyez à l'équipe

### Scénario B : Dashboard Looker Studio
1. Analysez votre base complète (par batch de 100)
2. Téléchargez CSV Looker Studio
3. Importez dans Looker Studio
4. Créez vos visualisations

### Scénario C : Audit Marketing
1. Analysez échantillon représentatif
2. Identifiez patterns (tags fréquents, objections récurrentes)
3. Ajustez stratégie produit/communication

---

## ⚡ Astuces Pro

### 💰 Optimiser les Coûts
- Commencez par 10-20 clients pour tester
- Analysez par batch si grosse base (ex: 100 à la fois)
- Coût réel : ~0.002$/client avec Mistral Large

### 📊 Looker Studio
Le format CSV est **directement importable** dans Looker Studio :
1. Data Sources → Add Data → Upload CSV
2. Créez vos graphiques :
   - Distribution urgence (bar chart)
   - Top tags (pie chart)
   - Timeline opportunités (table)

### 🎯 Actions Prioritaires
L'IA génère 3 types d'insights à exploiter :
1. **Opportunités** : Ce qu'on peut vendre maintenant
2. **Timing** : Quand contacter
3. **Actions** : Que faire concrètement

---

## 🛠️ En Cas de Problème

### "MISTRAL_API_KEY non trouvée"
→ Vérifiez que `.env` existe et contient votre clé

### "Colonne Transcription introuvable"
→ Votre CSV doit avoir exactement cette colonne : `Transcription`

### Timeout / Erreur API
→ Réduisez le nombre de clients à analyser en une fois

---

## 📞 Besoin d'Aide ?

Consultez le `README_APP.md` complet pour plus de détails !
