"""
Module d'analyse IA optimisée avec Mistral AI
L'IA reçoit les tags déjà extraits et se concentre sur l'analyse qualitative
"""
import json
from typing import Dict, List
from mistralai import Mistral

def analyze_batch(client: Mistral, batch_data: List[Dict]) -> List[Dict]:
    """
    Analyse IA par lots (Batch) pour une vitesse x5.
    Traite plusieurs clients en un seul appel API.
    
    Args:
        client: Client Mistral
        batch_data: Liste de dicts {"client_id": str, "text": str, "tags": dict}
        
    Returns:
        List[Dict]: Liste des résultats enrichis
    """
    
    # Construire le prompt "Multi-Client"
    clients_str = ""
    for item in batch_data:
        c_id = item['client_id']
        tags = item['tags']
        text = item['text']
        # Utilisation de json.dumps pour éviter les problèmes de quotes dans les tags
        tags_json = json.dumps(tags, ensure_ascii=False)
        
        clients_str += f"--- CLIENT ID: {c_id} ---\nMATCHING TAGS: {tags_json}\nTRANSCRIPTION: {text}\n\n"

    # Construction du prompt sécurisée (évite les triple quotes f-string qui peuvent casser)
    prompt = (
        f"Tu es l'analyste expert LVMH. Analyse ces {len(batch_data)} clients.\n\n"
        "DATA:\n"
        f"{clients_str}\n"
        "TACHE:\n"
        "1. Analyse CHAQUE client individuellement (Stratégie, Segments, Opportunités).\n"
        "2. Va droit au but.\n\n"
        "FORMAT DE RÉPONSE ATTENDU (Liste JSON stricte):\n"
        "{\n"
        '  "analyses": [\n'
        "    {\n"
        '      "client_id": "ID_DU_CLIENT",\n'
        '      "resume_complet": "Synthèse narrative (contexte + besoin)",\n'
        '      "insights_marketing": {\n'
        '        "opportunites_vente": ["Opp 1", "Opp 2"],\n'
        '        "produits_recommandes": ["Prod A", "Prod B"],\n'
        '        "actions_suggerees": ["Action 1"]\n'
        "      },\n"
        '      "analyse_intelligente": {\n'
        '         "nouveaux_tags_suggeres": ["Tag1"],\n'
        '         "strategie_avancee": ["Stratégie 1"]\n'
        "      },\n"
        '      "segment_client": "Un segment parmi: VIP_Travel_Business, VIP_Lifestyle_Luxe, Luxury_Outdoor, Young_Professional, Established_Elite, Occasionnel",\n'
        '      "objections_freins": ["Frein éventuel"],\n'
        '      "ice_breaker": "Phrase d\'accroche conversationnelle courte (1 phrase) pour briser la glace"\n'
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Consigne de stabilité: Réponds UNIQUEMENT avec le JSON valide, sans texte avant ni après."
    )

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            # Adapter max_tokens à la taille du lot (environ 500 tokens par client ou une grosse limite globale)
            max_tokens=8000, 
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result_json = json.loads(content)
        return result_json.get("analyses", [])
        
    except Exception as e:
        print(f"Erreur batch IA: {e}")
        # En cas d'erreur de l'IA (timeout, format...), on renvoie une structure vide
        fallback = []
        for item in batch_data:
            fallback.append({
                "client_id": item['client_id'],
                "resume_complet": "Erreur d'analyse IA (Timeout/Format)",
                "insights_marketing": {},
                "analyse_intelligente": {},
                "segment_client": "Inconnu",
                "objections_freins": []
            })
        return fallback
