"""
Exemple de Code - Intégration Mistral AI
Démontre comment le système va fonctionner
"""
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Exemple de configuration
MISTRAL_API_KEY = "your_api_key_here"
client = MistralClient(api_key=MISTRAL_API_KEY)

# Exemple de taxonomie compacte
TAXONOMY_SIMPLIFIED = {
    "localisation": ["Paris", "London", "Dubai", "Tokyo"],
    "budget": ["<5k", "5-10k", "10-15k", "15-25k", "25k+"],
    "urgence": [1, 2, 3, 4, 5],
    "style": ["Casual", "Chic", "Business", "Haute_couture"],
    "couleurs": ["Noir", "Beige", "Cognac", "Bordeaux"]
}

# ========================================
# ÉTAPE 1: NETTOYAGE DU TEXTE
# ========================================

def clean_transcript_with_mistral(raw_text: str) -> str:
    """Nettoie une transcription avec Mistral AI"""
    
    prompt_cleaning = f"""Tu es un éditeur expert spécialisé dans l'analyse de conversations commerciales haut de gamme.

MISSION: Nettoie cette transcription en supprimant:
- Les hésitations (euh, alors, donc, voilà, etc.)
- Les répétitions inutiles
- Le bruit conversationnel
- Les émojis et HTML

IMPORTANT: Conserve INTÉGRALEMENT:
- Tous les termes liés au luxe, à la mode, aux produits
- Les émotions exprimées (frustrations, joies, besoins)
- Les détails concrets (villes, budgets, événements, professions)
- Les mots-clés liés à la personnalisation, exclusivité, fonctionnalité

Transcription à nettoyer:
{raw_text}

Réponds UNIQUEMENT avec le texte nettoyé, sans introduction ni commentaire."""

    response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="user", content=prompt_cleaning)],
        temperature=0.3,
        max_tokens=800
    )
    
    return response.choices[0].message.content


# ========================================
# ÉTAPE 2: ANALYSE SÉMANTIQUE
# ========================================

def analyze_transcript_with_mistral(cleaned_text: str) -> dict:
    """Analyse une transcription nettoyée avec Mistral AI"""
    
    # Convertir la taxonomie en JSON pour l'injecter dans le prompt
    taxonomy_json = json.dumps(TAXONOMY_SIMPLIFIED, indent=2, ensure_ascii=False)
    
    prompt_analysis = f"""Tu es l'analyste marketing du projet LVMH Client Profiling.

CONTEXTE: Voici notre taxonomie complète de classification client:
{taxonomy_json}

MISSION: Analyse cette transcription nettoyée et génère un profil client structuré.

RÈGLES STRICTES:
1. Les tags dans "client_tags" doivent UNIQUEMENT provenir de la taxonomie ci-dessus
2. Ne crée JAMAIS de nouvelles catégories
3. Si un aspect n'est pas mentionné, ne l'invente pas
4. Le score d'urgence (1-5) est basé sur:
   - 5: Achat urgent, événement imminent
   - 4: Projet défini avec date
   - 3: Intérêt fort, timing flexible
   - 2: Exploration, pas de deadline
   - 1: Curiosité simple

Transcription nettoyée:
{cleaned_text}

FORMAT DE SORTIE (JSON strict):
{{
  "marketing_summary": "Synthèse en 1 phrase du besoin client",
  "urgency_score": 1,
  "client_tags": ["tag1", "tag2"],
  "objections": ["objection1", "objection2"]
}}

Réponds UNIQUEMENT avec le JSON, sans markdown ni commentaire."""

    response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="user", content=prompt_analysis)],
        temperature=0.3,
        max_tokens=1000,
        response_format={"type": "json_object"}  # Force JSON output
    )
    
    # Parser la réponse JSON
    result = json.loads(response.choices[0].message.content)
    return result


# ========================================
# EXEMPLE D'UTILISATION
# ========================================

if __name__ == "__main__":
    # Transcription sale exemple
    raw_transcript = """
    🌟 CLIENTE VIP 🌟 Mme Dupont 💼 entrepreneur ⭐⭐⭐⭐⭐
    Euh donc voilà alors la cliente euh elle a 35 ans environ
    Budget: 8000€ 💰💰💰
    🏠 Paris | ✈️ travels a lot
    Elle cherche euh donc un sac pour son mariage dans 2 mois
    Couleur euh noir ou cognac preferred ❤️
    Elle dit que c'est urgent urgent urgent 📞📞📞
    """
    
    print("=" * 70)
    print("EXEMPLE - PIPELINE MISTRAL AI")
    print("=" * 70)
    print()
    
    # Étape 1: Nettoyage
    print("🧹 NETTOYAGE...")
    cleaned = clean_transcript_with_mistral(raw_transcript)
    print(f"Texte nettoyé: {cleaned}")
    print()
    
    # Étape 2: Analyse
    print("🔍 ANALYSE...")
    analysis = analyze_transcript_with_mistral(cleaned)
    print("Résultat JSON:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print()
    
    print("✅ Pipeline terminé!")
    
    # Exemple de sortie attendue:
    """
    {
      "marketing_summary": "Cliente VIP cherche un sac de luxe pour son mariage dans 2 mois, budget 8k€",
      "urgency_score": 4,
      "client_tags": ["Paris", "5-10k", "Noir", "Cognac", "Business"],
      "objections": []
    }
    """
