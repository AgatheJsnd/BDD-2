# Roadmap - Système d'Automatisation Profils Clients LVMH

Objectif : industrialiser la création de profils clients à partir de données et transcriptions, avec une UI orientée retail et des exports CRM.

## Principes
- Priorité à la qualité des tags et à la traçabilité des règles.
- Schéma de données versionné, extensible et documenté.
- UX dédiée aux vendeurs (rapidité, clarté, actions directes).
- IA en soutien (explicable, non bloquante).

---

## Phase 1 — Planification & Structure (P0)
But : poser les fondations techniques et sémantiques.

### Tâches
- Analyser la structure hiérarchique des tags (taxonomie).
- Créer le schéma de base de données (profils, tags, règles, sources).
- Définir les règles d'extraction (mots-clés, motifs, pondérations).

### Livrables
- Document de taxonomie (niveaux, catégories, exemples).
- Schéma DB (ERD + tables + contraintes).
- Spécification des règles d'extraction (v1).

### Critères d'acceptation
- Taxonomie validée avec exemples de 10 profils.
- DB crée un lien traçable entre source, règle et tag.
- Règles testables sur un échantillon de transcriptions.

---

## Phase 2 — Développement (P0)
But : implémenter la chaîne de traitement.

### Tâches
- Créer le module de définition des tags (taxonomie).
- Développer l'analyseur de transcriptions.
- Implémenter le système de règles de tagging.
- Créer le générateur de profils clients.

### Livrables
- Module `taxonomy` avec versioning.
- Parser de transcriptions + normalisation.
- Moteur de règles (score/poids + justifications).
- Générateur de profils (JSON + DB).

### Critères d'acceptation
- Tagging explique "pourquoi" un tag est attribué.
- 90% des champs clés du profil sont remplis sur un set test.
- Génération reproductible (mêmes entrées = mêmes sorties).

---

## Phase 3 — Intégration (P0)
But : connecter les sources et alimenter la DB.

### Tâches
- Lire et parser le CSV.
- Appliquer le tagging automatique.
- Générer la base de données des profils.
- Créer des rapports et visualisations.

### Livrables
- Pipeline CSV → Profil → DB.
- Job de génération batch (CLI).
- Rapports initiaux (KPI + segments).

### Critères d'acceptation
- Pipeline traite 100% du CSV sans erreurs bloquantes.
- DB cohérente (contraintes respectées).
- Rapports affichent des agrégats plausibles.

---

## Phase 4 — Vérification (P1)
But : fiabiliser la qualité des tags et profils.

### Tâches
- Tester sur quelques clients (échantillon guidé).
- Valider la qualité des tags.
- Ajuster les règles si nécessaire.

### Livrables
- Suite de tests manuels + checklist.
- Rapport qualité des tags (precision/coverage).
- Règles ajustées (v2).

### Critères d'acceptation
- < 10% de tags jugés "hors contexte" sur l'échantillon.
- Ajustements documentés et versionnés.

---

## Phase 5 — Refonte UI & UX (P1)
But : améliorer l’expérience retail et visuelle.

### Tâches
- Design épuré (palette Beige/Marron).
- Tableau de bord interactif.
- Intégration badges et tags visuels.
- Connexion IA Mistral temps réel.

### Livrables
- Nouvelle charte UI (couleurs, typographies, composants).
- Dashboard mis à jour (filtres, cartes, stats).
- Badges/tag UI uniformisés.
- Intégration IA (streaming, fallback).

### Critères d'acceptation
- Temps d'accès aux infos clés < 3 clics.
- Affichage fluide sur desktop + tablette.
- IA optionnelle, non bloquante si indisponible.

---

## Phase 6 — Déploiement (P1)
But : rendre le projet déployable et documenté.

### Tâches
- Vérification des dépendances (`requirements.txt`).
- Création du Dockerfile (build + run).
- Documentation (README.md).
- Push sur GitHub.

### Livrables
- Image Docker exécutable.
- README complet (setup, run, IA, troubleshooting).
- Repo propre (structure + .gitignore).

### Critères d'acceptation
- Déploiement possible en 10 minutes.
- README suffisant pour un nouveau dev.

---

## Phase 7 — Améliorations Post-Simulation (P2)
But : fonctionnalités avancées et ROI retail.

### Tâches prioritaires
- Mode "Clienteling/iPad" : Vue simplifiée pour vendeurs (Camille).
- Générateur d'Ice-Breaker IA : Accroches conversationnelles (Camille).
- Export Données CRM : Bouton CSV pour campagnes (Sophie).
- Analyse Temporelle : Graphiques d'évolution (Alexandre).

### Livrables
- Mode vendeur (vue compacte + actions rapides).
- Module IA d'accroches contextualisées.
- Export CSV segmenté.
- Graphiques d'évolution par période.

### Critères d'acceptation
- Vendeurs accèdent à un profil en < 5s.
- Export prêt pour campagnes CRM sans retraitement.

---

## Dépendances clés
- Phase 2 dépend de Phase 1.
- Phase 3 dépend de Phase 2.
- Phase 4 dépend de Phase 3.
- Phase 5 peut démarrer après Phase 3.
- Phase 6 après Phase 5 (ou en parallèle si UI stable).

## Risques
- Qualité des transcriptions (bruit, langue, style).
- Taxonomie trop rigide ou trop large.
- Surdépendance à l'IA pour des tâches déterministes.

## Next Actions recommandées
- Valider la taxonomie v1 avec 10 profils réels.
- Définir les tables DB et les clés de traçabilité.
- Écrire 5 règles d'extraction "golden" testables.
