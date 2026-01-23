# 🎨 Guide d'Utilisation - Dashboard LVMH

## 🚀 Lancement du Dashboard

### Méthode 1 : Script automatique
```bash
run_dashboard.bat
```

### Méthode 2 : Ligne de commande
```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse :
**http://localhost:8501**

---

## 📊 Interface Dashboard

### Onglet 1 : Vue d'Ensemble

**Métriques Clés**
- Total clients
- Clients VIP (avec pourcentage)
- Clients fidèles
- Nouveaux clients

**Graphiques**
- 📊 Répartition par statut (diagramme circulaire)
- 📊 Répartition par genre (barres)
- 🎨 Top 5 couleurs préférées
- 🏃 Top 5 sports

### Onglet 2 : Liste Clients

**Filtres Interactifs**
- **Statut** : VIP, Fidèle, Régulier, Nouveau, Occasionnel
- **Genre** : Femme, Homme
- **Âge** : 18-25, 26-35, 36-45, 46-55, 56+
- **Budget** : <5k, 5-10k, 10-15k, 15-25k, 25k+

**Affichage**
- Cartes clients avec badges colorés
- Détails complets dans expander
- Limite de 20 clients pour performance

**Exemple d'utilisation** :
1. Sélectionnez "VIP" dans Statut
2. Sélectionnez "25k+" dans Budget
3. → Voir uniquement les clients VIP à fort budget

### Onglet 3 : Recherche

**Recherche par Client**
- Sélecteur dropdown avec tous les IDs clients
- Vue détaillée complète du profil
- Organisation en sections :
  - 🆔 Identité
  - 📍 Localisation
  - 🎨 Style Personnel
  - 💰 Projet d'Achat
  - 🏃 Lifestyle

**JSON Complet**
- Expander avec le profil JSON brut
- Utile pour développeurs

### Onglet 4 : Statistiques Avancées

**Graphiques**
- Distribution par âge (barres)
- Distribution par budget (barres colorées)
- Régimes alimentaires (diagramme circulaire)

**Insights Clés**
- 🏆 Segment VIP
- 🌱 Conscience alimentaire
- 🏃 Sport populaire

---

## 🎯 Cas d'Usage

### 1. Préparer un Événement VIP

1. Aller dans l'onglet **Liste Clients**
2. Filtrer par **Statut = "VIP"**
3. Observer les **régimes alimentaires** (végane/végétarien)
4. Noter les **sports** et **centres d'intérêt** communs

### 2. Cibler une Campagne Marketing

1. Onglet **Statistiques Avancées**
2. Analyser les **couleurs populaires**
3. Observer les **budgets** moyens
4. Aller dans **Liste Clients** et filtrer selon campagne

### 3. Recherche Client Spécifique

1. Onglet **Recherche**
2. Sélectionner l'ID client (ex: CA_014)
3. Voir le profil complet
4. Noter les préférences pour personnalisation

### 4. Analyse de Segment

1. Onglet **Liste Clients**
2. Filtrer : **Age = "26-35"** + **Budget = "15-25k"**
3. Analyser les profils de ce segment
4. Adapter l'offre produit

---

## 💡 Astuces

### Performance
- Le dashboard charge automatiquement tous les profils
- Les données sont mises en cache pour rapidité
- Limite de 20 clients affichés simultanément

### Filtres Multiples
- Vous pouvez combiner plusieurs filtres
- Exemple : VIP + Femme + 36-45 ans + Budget 25k+

### Export
- Utilisez le profil JSON pour exporter
- Copiez-collez depuis l'expander JSON

### Rechargement
- Pour recharger les données : cliquez sur ⋮ > Rerun
- Ou appuyez sur **R** dans le dashboard

---

## 📈 Exemples de Requêtes

### Clients à fort potentiel
```
Statut: VIP
Budget: 25k+
```

### Segment wellness
```
Rechercher manuellement les clients avec:
- Sport: Yoga
- Régime: Végane
```

### Nouveaux clients à fidéliser
```
Statut: Nouveau
Budget: 15-25k ou 25k+
```

### Clients matures haut de gamme
```
Age: 56+
Statut: VIP ou Fidèle
```

---

## 🛠️ Maintenance

### Mise à jour des données
Après avoir traité de nouveaux CSV :
1. Exécutez `python main.py`
2. Relancez le dashboard
3. Les nouvelles données apparaîtront automatiquement

### Problèmes courants

**Le dashboard ne se lance pas**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

**Les données ne s'affichent pas**
- Vérifiez que `data/profiles.db` existe
- Ré-exécutez `python main.py`

**Erreur de port**
```bash
streamlit run dashboard.py --server.port 8502
```

---

## 🎨 Personnalisation

Le dashboard peut être personnalisé dans `dashboard.py` :

- **Couleurs** : Modifiez les `color_discrete_sequence`
- **Layout** : Changez `layout="wide"` en `layout="centered"`
- **Filtres** : Ajoutez de nouveaux critères de filtrage
- **Graphiques** : Utilisez d'autres types de graphiques Plotly

---

**Dashboard LVMH - Profils Clients v1.0**
