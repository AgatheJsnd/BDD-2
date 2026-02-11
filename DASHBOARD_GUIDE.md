# Guide d'Utilisation - LVMH Client Analytics

## Lancement

### Methode 1 : Script automatique
```bash
run_app.bat
```

### Methode 2 : Ligne de commande
```bash
streamlit run app.py
```

Le dashboard s'ouvre dans le navigateur a l'adresse:
`http://localhost:8501`

---

## Interface

### Onglet 1 : Donnees & Tags
- Import CSV avec une colonne obligatoire `Transcription`.
- Detection automatique d'une colonne de date si elle existe (ex: `date`, `created_at`).
- `SCAN TURBO` pour extraire les tags Python.
- `AJOUTER L'INTELLIGENCE` pour enrichir via IA (optionnel).

### Onglet 2 : Vue Globale
- Filtres avances: Segment IA (si dispo), Urgence >= 4, Urgence minimum.
- Bascule d'affichage:
- `Tableaux & Graphiques` pour KPIs et charts.
- `Clienteling (cartes)` pour les vendeurs en boutique (cartes lisibles).
- Analyse temporelle (nouveaux clients par semaine) si une colonne date est detectee.

### Onglet 3 : Analyse Intelligente
- Suggestions de nouveaux tags IA.
- Strategies marketing avancees.
- Focus client avec ice-breaker, resume et objections.

### Onglet 4 : Exports
- Export CSV (Looker/CRM).
- Export Excel complet.
- Champs IA inclus (segment, opportunites, strategies).

---

## Cas d'usage

### 1. Mode Clienteling (Boutique)
1. Onglet `Vue Globale`
2. Activer `Clienteling (cartes)`
3. Utiliser les ice-breakers et le budget pour orienter la conversation

### 2. Triage CRM (Urgence)
1. Onglet `Vue Globale`
2. Activer filtre `Urgence >= 4`
3. Export CSV pour traitement CRM

### 3. Analyse de tendance
1. Importer un CSV avec une colonne de date
2. Onglet `Vue Globale`
3. Lire la courbe "nouveaux clients par semaine"

---

## Astuces

### Performance
- Limiter le nombre de clients analyses pour l'IA.
- Le `SCAN TURBO` est instantane pour les tags.

### Export
- L'export Excel contient les champs IA et tags Python.
- Le CSV est pret pour Looker Studio.

### Rechargement
- Menu `Rerun` dans Streamlit.
- Ou appuyer sur `R` dans l'UI.

---

## Maintenance

### Problemes courants

**Le dashboard ne se lance pas**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Le CSV ne s'importe pas**
- Verifier la colonne `Transcription`.
- Verifier l'encodage (UTF-8 recommande).

**Erreur de port**
```bash
streamlit run app.py --server.port 8502
```

---

LVMH Client Analytics
