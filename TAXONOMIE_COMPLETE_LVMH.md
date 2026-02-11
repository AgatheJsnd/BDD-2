# Taxonomie Complète LVMH - Profil Client

## 📋 Vue d'ensemble

Cette taxonomie définit la structure complète des données client pour le système LVMH Client Analytics.

## 🔍 Comparaison : Actuel vs Cible

### ✅ Catégories Actuellement Implémentées (Système actuel)

1. **Âge** ✅ (18-25, 26-35, 36-45, 46-55, 56+)
2. **Localisation** ✅ (Europe, Amérique, Moyen-Orient/Asie, Afrique + villes)
3. **Profession** ✅ (Entrepreneur, Cadre, Profession libérale, Artiste, Étudiant)
4. **Situation familiale** ✅ (Célibataire, Couple, Marié(e), Avec enfants)
5. **Budget** ✅ (<5k, 5-10k, 10-15k, 15-25k, 25k+)
6. **Motif d'achat** ✅ (Cadeau, Mariage, Anniversaire, Diplôme, Voyage, Achat personnel)
7. **Style personnel** ✅ (Casual, Chic, Business, Sportswear, Haute couture)
8. **Couleurs** ✅ (Noir, Beige, Cognac, Bordeaux, Bleu marine, Blanc, Gris, Rose gold, Rouge)
9. **Matières** ✅ (Cuir, Cachemire, Soie, Laine, Coton, Matières vegan)
10. **Centres d'intérêt** ✅ (Golf, Tennis, Yoga, Running, Fitness, Ski, Football, Voyage, Art/Culture, Gastronomie)
11. **Urgence** ✅ (Score 1-5)

### ❌ Catégories Manquantes (À implémenter)

#### 1. **Identité**
- ❌ Genre (Femme, Homme, Autre)
- ❌ Statut relationnel (VIP, Fidèle, Nouveau, Régulier, Occasionnel)
- ❌ Langue parlée (12+ langues)
- ⚠️ Profession (à enrichir avec sous-catégories détaillées)

#### 2. **Lifestyle & Centres d'intérêt** (À enrichir)
- ⚠️ Sport (à structurer en Collectif/Individuel avec sous-catégories)
- ❌ Musique (6 catégories principales)
- ❌ Animaux (Domestiques, Exotiques)
- ⚠️ Voyage (à enrichir avec Type/Style/Préférence/Fréquence)
- ⚠️ Art & Culture (à structurer)
- ⚠️ Gastronomie (à enrichir)

#### 3. **Style personnel** (À enrichir massivement)
- ❌ Pièces favorites (Sacs, Chaussures, Manteaux, Robes, Costumes, Accessoires)
- ⚠️ Couleurs (à enrichir avec Tons chauds/froids, Pastels, Métalliques)
- ⚠️ Matières (à enrichir avec Naturelles/Premium/Techniques/Alternatives)
- ❌ Sensibilité mode (Tendance, Intemporel, Classique)
- ❌ Taille/Mensurations (Taille vêtements, Pointure, Coupe, Morphologie)

#### 4. **Projet d'achat** (À enrichir)
- ⚠️ Motif & Rôle (à structurer Offrir/Pour soi)
- ❌ Timing (Urgent, Date fixée, Long terme)
- ❌ Marques préférées (LV, Dior, Gucci, Loro Piana, Bulgari, etc.)
- ❌ Fréquence d'achat (Régulière, Occasionnelle, Rare)

#### 5. **Préférences & Contraintes**
- ❌ Régime (Vegan, Végétarien, Pescétarien, etc.)
- ❌ Allergies (Alimentaires, Cutanées)
- ❌ Valeurs (Éthique/durable, Qualité, Exclusivité)

#### 6. **Suivi**
- ❌ Action (Rappeler, Confirmer, Relancer, Invitation, Preview)
- ❌ Échéance (M+1, M+2, M+3, M+3+)
- ❌ Canal de contact (Email, Téléphone, SMS, WhatsApp, Réseaux sociaux, Site web)

## 📊 Statistiques d'implémentation

| Catégorie | Sous-catégories | Implémenté | Taux |
|-----------|----------------|------------|------|
| **Identité** | 6 | 2/6 | 33% |
| **Localisation** | 1 | 1/1 | 100% |
| **Lifestyle** | 6 | 2/6 | 33% |
| **Style personnel** | 6 | 3/6 | 50% |
| **Projet d'achat** | 5 | 2/5 | 40% |
| **Préférences** | 3 | 0/3 | 0% |
| **Suivi** | 3 | 0/3 | 0% |
| **TOTAL** | **30** | **10/30** | **33%** |

## 🎯 Prochaines étapes recommandées

### Phase 1 : Enrichissement rapide (Impact élevé)
1. **Genre** - Détection simple (il/elle, monsieur/madame)
2. **Marques préférées** - Mots-clés LVMH
3. **Pièces favorites** - Sac, chaussures, accessoires
4. **Langue parlée** - Détection automatique
5. **Timing** - Expressions d'urgence

### Phase 2 : Structuration avancée
1. **Sport** - Réorganiser en Collectif/Individuel
2. **Musique** - 6 catégories principales
3. **Voyage** - Type/Style/Destination
4. **Couleurs** - Tons chauds/froids/pastels
5. **Matières** - Naturelles/Premium/Techniques

### Phase 3 : Fonctionnalités CRM
1. **Préférences & Contraintes** - Régime, allergies, valeurs
2. **Suivi** - Actions, échéances, canaux
3. **Taille/Mensurations** - Pour recommandations précises

## 💡 Recommandations techniques

### Pour l'extraction automatique
- ✅ **Facile** : Genre, Langue, Marques, Timing
- ⚠️ **Moyen** : Pièces favorites, Musique, Animaux
- ❌ **Difficile** : Mensurations, Allergies, Valeurs (nécessite IA)

### Pour le dashboard
- Ajouter filtres par Genre, Langue, Marques
- Créer visualisations par Pièces favorites
- Intégrer module Suivi/Actions

## 📁 Structure de fichiers recommandée

```
src/
├── tag_extractor.py (actuel - tags de base)
├── advanced_extractor.py (nouveau - taxonomie complète)
├── mappings/
│   ├── identity.py (Genre, Langue, Statut)
│   ├── lifestyle.py (Sport, Musique, Animaux, Voyage)
│   ├── style.py (Pièces, Couleurs, Matières, Tailles)
│   ├── purchase.py (Motif, Budget, Marques, Timing)
│   ├── preferences.py (Régime, Allergies, Valeurs)
│   └── tracking.py (Actions, Échéances, Canaux)
└── validators/
    └── taxonomy_validator.py
```

## 🚀 Estimation d'effort

| Phase | Catégories | Mots-clés | Temps estimé |
|-------|-----------|-----------|--------------|
| Phase 1 | 5 | ~200 | 2-3 jours |
| Phase 2 | 5 | ~300 | 3-4 jours |
| Phase 3 | 3 | ~150 | 2-3 jours |
| **TOTAL** | **13** | **~650** | **7-10 jours** |

---

**Note** : La taxonomie actuelle couvre environ 33% de la cible. L'implémentation complète nécessitera une refonte structurelle du système d'extraction.
