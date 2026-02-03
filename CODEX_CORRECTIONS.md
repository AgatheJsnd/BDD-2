# Instructions de Correction - LVMH Client Analytics

## Rapport de Bugs

Le test avec 500 clients simulés a révélé les problèmes suivants.

---

## 🔴 Bug 1: Crash sur transcription vide (CRITIQUE)

**Fichier:** `src/text_analyzer.py`

**Problème:** Quand une transcription est vide (NaN du CSV), les méthodes appellent `.lower()` sur un float, causant:
```
AttributeError: 'float' object has no attribute 'strip'
```

**Clients affectés:** 5 sur 500

**Correction:** Ajouter une validation au début de `analyze_full_text()`:

```python
def analyze_full_text(self, text: str) -> Dict:
    """Analyse complète du texte"""
    # Validation de l'entrée
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
    if not text.strip():
        return {
            'age': None,
            'budget': None,
            'genre': [],
            'statut': [],
            'profession': [],
            'sport': [],
            'art_culture': [],
            'voyage': [],
            'couleurs': [],
            'matieres': [],
            'regime': [],
            'pieces': [],
            'motif': [],
            'cities': [],
            'allergies': []
        }
    # ... reste du code
```

---

## 🟡 Bug 2: Pattern budget limité

**Fichier:** `src/text_analyzer.py`

**Problème:** Le pattern `r'(\d+)[kK€]'` ne capture pas:
- Format USD: `$5000`
- Format complet: `5000€`, `5000 euros`
- Ranges: `3-4K`

**Correction:** Améliorer le pattern dans `extract_budget()`:

```python
def extract_budget(self, text: str) -> str:
    """Extrait le budget du texte"""
    if not isinstance(text, str) or not text.strip():
        return None
    
    text_lower = text.lower()
    
    # Pattern amélioré pour capturer plus de formats
    # Format: 5K, 5k, 5000€, $5000, 5000 euros
    patterns = [
        r'(\d+)\s*[kK]',           # 5K, 5k
        r'(\d+)\s*€',              # 5000€
        r'\$\s*(\d+)',             # $5000
        r'(\d+)\s*euros?',         # 5000 euros
        r'budget.*?(\d+)',         # budget 5000
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            try:
                budget = int(matches[0])
                # Normaliser en milliers si petit nombre (5 → 5000)
                if budget < 100:
                    budget = budget * 1000
                
                if budget < 5000:
                    return "<5k"
                elif budget < 10000:
                    return "5-10k"
                elif budget < 15000:
                    return "10-15k"
                elif budget < 25000:
                    return "15-25k"
                else:
                    return "25k+"
            except (ValueError, IndexError):
                continue
    
    return None
```

---

## 🟡 Bug 3: CSV - Champs manquants

**Fichier:** `src/csv_processor.py`

**Problème:** Les valeurs NaN ne sont pas gérées.

**Correction:** Dans `get_conversations()`:

```python
def get_conversations(self) -> List[Dict]:
    """Retourne la liste des conversations sous forme de dictionnaires"""
    if self.data is None:
        self.load_data()

    conversations = []
    for _, row in self.data.iterrows():
        conversations.append({
            "client_id": row["ID"],
            "date": row["Date"] if pd.notna(row["Date"]) else "",
            "duration": row["Duration"] if pd.notna(row["Duration"]) else "",
            "language": row["Language"] if pd.notna(row["Language"]) else "FR",
            "length": row["Length"] if pd.notna(row["Length"]) else "medium",
            "transcription": row["Transcription"] if pd.notna(row["Transcription"]) else "",
        })

    return conversations
```

---

## Commande de test après correction

```bash
python run_test.py
```

Le taux de succès devrait passer de 99% à 100%.
