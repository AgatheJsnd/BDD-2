"""
Module d'intégration Mistral AI pour l'analyse intelligente des profils clients
"""
import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

# Charger les variables d'environnement
load_dotenv()

class MistralAnalyzer:
    """Analyseur IA avec Mistral pour les profils clients LVMH"""
    
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY non trouvée dans le fichier .env")
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
    
    def analyze_transcription(self, transcription: str, client_id: str) -> dict:
        """Analyse une transcription avec Mistral AI"""
        
        prompt = f"""Tu es un expert en analyse de clientèle luxe pour LVMH. 
Analyse cette transcription de conversation client et extrait les informations clés.

TRANSCRIPTION (Client {client_id}):
{transcription}

Réponds en JSON avec exactement cette structure:
{{
    "resume": "Résumé de 2-3 phrases de la conversation",
    "profil_client": {{
        "genre": "Homme/Femme/Non précisé",
        "age_estime": "18-25/26-35/36-45/46-55/56+/Non précisé",
        "profession": "Profession détectée ou Non précisé",
        "statut_vip": "VIP/Fidèle/Régulier/Nouveau/Occasionnel"
    }},
    "preferences": {{
        "couleurs": ["liste des couleurs mentionnées"],
        "matieres": ["liste des matières mentionnées"],
        "styles": ["classique", "moderne", "casual", etc.]
    }},
    "projet_achat": {{
        "type": "Personnel/Cadeau/Professionnel",
        "budget_estime": "<5k/5-10k/10-15k/15-25k/25k+",
        "urgence": "Immédiat/Court terme/Moyen terme/Long terme",
        "produits_interesses": ["liste des produits"]
    }},
    "centres_interet": ["liste des hobbies/sports/passions détectés"],
    "tags_suggeres": ["5-10 tags pertinents pour ce client"],
    "recommandations_commerciales": ["3-5 actions recommandées pour ce client"],
    "score_potentiel": 1-100,
    "ice_breaker": "Phrase d'accroche conversationnelle (1 phrase) pour un Client Advisor",
    "notes_importantes": "Toute info importante à retenir"
}}

Réponds UNIQUEMENT avec le JSON, sans markdown ni explication."""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content
            
            # Parser le JSON
            # Nettoyer si nécessaire
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            return {
                "error": str(e),
                "resume": "Erreur lors de l'analyse IA",
                "tags_suggeres": [],
                "recommandations_commerciales": []
            }
    
    def suggest_tags_for_profile(self, profile: dict) -> list:
        """Suggère des tags supplémentaires pour un profil existant"""
        
        prompt = f"""En tant qu'expert CRM luxe, analyse ce profil client et suggère des tags pertinents.

PROFIL CLIENT:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Suggère 10 tags pertinents pour enrichir ce profil, en considérant:
- Segment client (VIP, potentiel, fidèle)
- Préférences produits
- Comportement d'achat
- Lifestyle et centres d'intérêt
- Opportunités commerciales

Réponds UNIQUEMENT avec un JSON array de tags:
["tag1", "tag2", "tag3", ...]"""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            return [f"Erreur: {str(e)}"]
    
    def generate_recommendations(self, profile: dict) -> list:
        """Génère des recommandations commerciales personnalisées"""
        
        prompt = f"""Tu es un conseiller commercial expert LVMH. Analyse ce profil client:

{json.dumps(profile, ensure_ascii=False, indent=2)}

Génère 5 recommandations commerciales personnalisées et actionnables.
Chaque recommandation doit inclure:
- Action concrète
- Produit/service à proposer
- Timing suggéré
- Justification basée sur le profil

Réponds en JSON:
[
    {{"action": "...", "produit": "...", "timing": "...", "justification": "..."}},
    ...
]"""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_client_segment(self, profiles: list) -> dict:
        """Analyse un segment de clients pour insights globaux"""
        
        # Résumer les profils pour l'analyse
        summary = {
            "total": len(profiles),
            "statuts": {},
            "budgets": {},
            "couleurs": {},
            "sports": []
        }
        
        for p in profiles[:20]:  # Limiter pour l'API
            statut = p.get('identite', {}).get('statut_relationnel', 'N/A')
            summary['statuts'][statut] = summary['statuts'].get(statut, 0) + 1
            
            budget = p.get('projet_achat', {}).get('budget', 'N/A')
            summary['budgets'][budget] = summary['budgets'].get(budget, 0) + 1
        
        prompt = f"""Analyse ce segment de {len(profiles)} clients LVMH:

{json.dumps(summary, ensure_ascii=False, indent=2)}

Fournis une analyse stratégique avec:
1. Profil type du segment
2. Opportunités commerciales
3. Risques identifiés
4. Actions prioritaires
5. KPIs à suivre

Réponds en JSON structuré."""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            return {"error": str(e)}


# Test rapide
if __name__ == "__main__":
    analyzer = MistralAnalyzer()
    
    test_profile = {
        "client_id": "CA_001",
        "identite": {"genre": "Femme", "age": "36-45", "statut_relationnel": "VIP"},
        "style_personnel": {"couleurs_preferees": ["Noir", "Cognac"]},
        "projet_achat": {"budget": "15-25k", "motif": "Cadeau"}
    }
    
    print("Test suggestion de tags:")
    tags = analyzer.suggest_tags_for_profile(test_profile)
    print(tags)
