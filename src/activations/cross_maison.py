"""
Activation 6 — Cross-Maison (Pilier Service)
La Synergie Groupe LVMH : propose des expériences/produits de Maisons sœurs basées sur les affinités.
"""
from datetime import datetime


def generate_cross_maison(client_id: str, tags: dict, extracted: dict,
                          reference_date: datetime = None) -> list:
    """
    Génère des activations cross-maison basées sur les affinités détectées.
    Un client Berluti passionné de champagne → proposition Dom Pérignon.
    """
    ref = reference_date or datetime.now()
    affinites = extracted.get("affinites_cross", [])
    marques = tags.get("marques_preferees", [])
    activations = []
    
    for affinite in affinites:
        affinite_label = affinite.get("affinite", "")
        maisons_cibles = affinite.get("maisons_cibles", [])
        confidence = affinite.get("confidence", 0.5)
        keywords = affinite.get("keywords_detectes", [])
        
        if not maisons_cibles or confidence < 0.5:
            continue
        
        # Exclure les maisons déjà connues du client
        maisons_nouvelles = [m for m in maisons_cibles 
                            if not any(m.lower() in str(mk).lower() for mk in (marques if isinstance(marques, list) else []))]
        
        if not maisons_nouvelles:
            continue
        
        maison_principale = maisons_nouvelles[0]
        
        # Construire la proposition
        proposition = _get_proposition(affinite_label, maison_principale)
        
        genre = tags.get("genre", "")
        civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
        
        priority = "HAUTE" if confidence >= 0.7 else "MOYENNE"
        
        activations.append({
            "client_id": client_id,
            "activation_type": "cross_maison",
            "pillar": "Service",
            "priority": priority,
            "trigger_date": ref.strftime("%Y-%m-%d"),
            "canal_prefere": _get_canal(tags),
            "message_vendeur": (
                f"Bonjour {civilite}, sachant votre goût pour "
                f"{', '.join(keywords[:2])}, je me suis permis(e) de vous "
                f"recommander notre Maison sœur {maison_principale}. "
                f"{proposition} "
                f"Puis-je organiser cela pour vous ?"
            ),
            "context": {
                "affinite": affinite_label,
                "maison_cible": maison_principale,
                "toutes_maisons": maisons_nouvelles,
                "keywords": keywords,
                "confidence": confidence,
                "proposition": proposition,
            },
            "kpis": {
                "probabilite_conversion": round(confidence * 0.4, 2),
                "valeur_estimee": "200-5000€",
            }
        })
    
    return activations


def _get_proposition(affinite: str, maison: str) -> str:
    """Génère une proposition contextuelle basée sur l'affinité et la Maison."""
    propositions = {
        "Vins Spiritueux": f"{maison} organise des dégustations privées exclusives. Je peux vous réserver une place.",
        "Art Culture": f"{maison} propose des visites privées et des éditions limitées d'art. Un moment unique.",
        "Horlogerie": f"{maison} a de nouvelles collections fascinantes. Je peux organiser une présentation privée.",
        "Joaillerie": f"{maison} propose des pièces d'exception. Une découverte qui vaut le détour.",
        "Beaute Parfum": f"{maison} a créé de nouvelles fragrances exclusives. Un univers sensoriel à explorer.",
        "Gastronomie": f"{maison} offre des expériences gastronomiques uniques. Une table d'exception.",
        "Voyage Luxe": f"{maison} propose des séjours d'exception dans les plus beaux endroits du monde.",
    }
    return propositions.get(affinite, f"{maison} vous réserve des expériences exclusives.")


def _get_canal(tags: dict) -> str:
    canaux = tags.get("canaux_contact", [])
    if isinstance(canaux, list) and canaux:
        return canaux[0]
    return "Email"
