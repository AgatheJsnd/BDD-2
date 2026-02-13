"""
Moteur d'Activation Client — Orchestrateur principal.
Exécute les 6 types d'activation sur tous les clients et génère un rapport actionnable.
"""
import sys
import os
from datetime import datetime
from typing import Optional

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from activations.extractors import extract_all_actionable
from activations.lifestyle_voyage import generate_lifestyle_voyage
from activations.gifting_dates import generate_gifting_dates
from activations.next_best_product import generate_next_best_product
from activations.rupture_stock import generate_rupture_stock
from activations.care_entretien import generate_care_entretien
from activations.cross_maison import generate_cross_maison


class ActivationEngine:
    """
    Moteur d'activation CRM — orchestre 6 types d'activation sur les résultats de scan.
    
    Usage:
        engine = ActivationEngine(results)
        activations = engine.run_all_activations()
        brief = engine.generate_weekly_brief()
    """
    
    GENERATORS = [
        ("lifestyle_voyage", generate_lifestyle_voyage),
        ("gifting_dates", generate_gifting_dates),
        ("next_best_product", generate_next_best_product),
        ("rupture_stock", generate_rupture_stock),
        ("care_entretien", generate_care_entretien),
        ("cross_maison", generate_cross_maison),
    ]
    
    def __init__(self, results: list, reference_date: datetime = None):
        """
        Args:
            results: Liste des résultats du scan (même format que session_state["results"])
            reference_date: Date de référence pour les calculs de timing
        """
        self.results = results or []
        self.reference_date = reference_date or datetime.now()
        self.activations = []
        self.stats = {}
    
    def run_all_activations(self) -> list:
        """
        Exécute les 6 types d'activation sur tous les clients.
        
        Returns:
            list[dict]: Toutes les activations générées
        """
        self.activations = []
        
        for r in self.results:
            self.generate_for_client(r)
        
        # Calculer les stats
        self._compute_stats()
        
        return self.activations

    def generate_for_client(self, client_data: dict) -> list:
        """Génère les activations pour un client spécifique et les ajoute à la liste."""
        client_id = client_data.get("client_id", "")
        tags = client_data.get("tags_extracted", {})
        text = client_data.get("transcription_originale", "") or client_data.get("cleaned_text", "")
        
        # Phase 1 : Extraction contextuelle
        extracted = extract_all_actionable(text, tags, self.reference_date)
        
        client_acts = []
        # Phase 2 : Générer les activations
        for act_type, generator in self.GENERATORS:
            try:
                acts = generator(client_id, tags, extracted, self.reference_date)
                client_acts.extend(acts)
            except Exception as e:
                print(f"Erreur activation {act_type} pour {client_id}: {e}")
        
        self.activations.extend(client_acts)
        return client_acts
    
    def get_activations_by_priority(self) -> dict:
        """Regroupe les activations par priorité."""
        result = {"HAUTE": [], "MOYENNE": [], "BASSE": []}
        for act in self.activations:
            p = act.get("priority", "MOYENNE")
            result.setdefault(p, []).append(act)
        return result
    
    def get_activations_by_pillar(self) -> dict:
        """Regroupe les activations par pilier."""
        result = {"Émotionnel": [], "Produit": [], "Service": []}
        for act in self.activations:
            pillar = act.get("pillar", "Service")
            result.setdefault(pillar, []).append(act)
        return result
    
    def get_activations_by_client(self) -> dict:
        """Regroupe les activations par client."""
        result = {}
        for act in self.activations:
            cid = act.get("client_id", "")
            result.setdefault(cid, []).append(act)
        return result
    
    def get_activations_by_type(self) -> dict:
        """Regroupe par type d'activation."""
        result = {}
        for act in self.activations:
            atype = act.get("activation_type", "")
            result.setdefault(atype, []).append(act)
        return result

    def get_top_clients(self, n: int = 5) -> list:
        """Retourne les N clients avec le plus d'activations haute priorité."""
        by_client = self.get_activations_by_client()
        scored = []
        for cid, acts in by_client.items():
            score = sum(1 for a in acts if a.get("priority") == "HAUTE") * 3
            score += sum(1 for a in acts if a.get("priority") == "MOYENNE")
            scored.append({"client_id": cid, "score": score, "nb_activations": len(acts)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:n]
    
    def generate_weekly_brief(self) -> str:
        """
        Génère un résumé hebdomadaire des actions à entreprendre.
        """
        if not self.activations:
            return "Aucune activation générée. Lancez d'abord le Scan Turbo."
        
        by_priority = self.get_activations_by_priority()
        by_pillar = self.get_activations_by_pillar()
        top_clients = self.get_top_clients(5)
        
        lines = [
            f"# Brief Hebdomadaire — {self.reference_date.strftime('%d/%m/%Y')}",
            f"",
            f"## 📊 Synthèse",
            f"- **{len(self.activations)}** activations générées",
            f"- **{len(by_priority.get('HAUTE', []))}** haute priorité",
            f"- **{len(by_priority.get('MOYENNE', []))}** moyenne priorité",
            f"- **{len(by_priority.get('BASSE', []))}** basse priorité",
            f"- **{self.stats.get('clients_actives', 0)}/{self.stats.get('total_clients', 0)}** clients avec activations",
            f"",
            f"## 🎯 Répartition par Pilier",
        ]
        
        for pillar, acts in by_pillar.items():
            if acts:
                lines.append(f"- **{pillar}** : {len(acts)} activations")
        
        lines.extend([
            f"",
            f"## 🏆 Top 5 Clients à Activer",
        ])
        for i, tc in enumerate(top_clients, 1):
            lines.append(f"{i}. **{tc['client_id']}** — {tc['nb_activations']} activations (score: {tc['score']})")
        
        # Actions urgentes
        urgent = by_priority.get("HAUTE", [])
        if urgent:
            lines.extend([
                f"",
                f"## 🔴 Actions Urgentes ({len(urgent)})",
            ])
            for u in urgent[:10]:
                atype = u.get("activation_type", "").replace("_", " ").title()
                lines.append(f"- **{u['client_id']}** — {atype}: {u.get('message_vendeur', '')[:80]}...")
        
        return "\n".join(lines)
    
    def _compute_stats(self):
        """Calcule les statistiques globales."""
        clients_with_activations = set(a["client_id"] for a in self.activations)
        all_clients = set(r.get("client_id", "") for r in self.results)
        
        self.stats = {
            "total_activations": len(self.activations),
            "total_clients": len(all_clients),
            "clients_actives": len(clients_with_activations),
            "taux_couverture": round(len(clients_with_activations) / max(len(all_clients), 1) * 100, 1),
            "by_priority": {p: len(acts) for p, acts in self.get_activations_by_priority().items()},
            "by_pillar": {p: len(acts) for p, acts in self.get_activations_by_pillar().items()},
            "by_type": {t: len(acts) for t, acts in self.get_activations_by_type().items()},
        }
