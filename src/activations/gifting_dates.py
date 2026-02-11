"""
Activation 2 — Gifting & Dates Clés (Pilier Émotionnel)
L'Assistant Personnel : rappelle les dates importantes et suggère des cadeaux pertinents.
"""
from datetime import datetime, timedelta


def generate_gifting_dates(client_id: str, tags: dict, extracted: dict,
                           reference_date: datetime = None) -> list:
    """
    Génère des activations basées sur les dates clés détectées.
    Trigger : J-15 avant chaque date anniversaire.
    """
    ref = reference_date or datetime.now()
    dates = extracted.get("dates_cles", [])
    produits = extracted.get("produits", [])
    activations = []
    
    for date_info in dates:
        date_type = date_info.get("type", "")
        date_estimee = date_info.get("date_estimee")
        
        # Calculer trigger J-15
        trigger_date = None
        priority = "MOYENNE"
        if date_estimee:
            try:
                dt = datetime.strptime(date_estimee, "%Y-%m-%d")
                trigger_date = (dt - timedelta(days=15)).strftime("%Y-%m-%d")
                days_until = (dt - ref).days
                if 0 < days_until <= 15:
                    priority = "HAUTE"
                    trigger_date = ref.strftime("%Y-%m-%d")
                elif days_until <= 0:
                    priority = "BASSE"  # Date passée
            except ValueError:
                pass
        
        # Suggestions basées sur le profil
        suggestions = _get_gift_suggestions(date_type, tags, produits)
        destinataire = _get_destinataire(date_type)
        
        genre = tags.get("genre", "")
        civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
        
        activations.append({
            "client_id": client_id,
            "activation_type": "gifting_dates",
            "pillar": "Émotionnel",
            "priority": priority,
            "trigger_date": trigger_date,
            "canal_prefere": _get_canal(tags),
            "message_vendeur": _build_message(civilite, date_info, destinataire, suggestions),
            "context": {
                "type_date": date_type,
                "destinataire": destinataire,
                "date_str": date_info.get("date_str"),
                "date_estimee": date_estimee,
                "suggestions": suggestions,
            },
            "kpis": {
                "probabilite_conversion": 0.55,
                "valeur_estimee": "300-1500€",
            }
        })
    
    return activations


def _get_destinataire(date_type: str) -> str:
    """Identifie le destinataire du cadeau."""
    mapping = {
        "anniversaire_epouse": "votre épouse",
        "anniversaire_mari": "votre époux",
        "anniversaire_enfant": "votre enfant",
        "anniversaire_mariage": "vous deux",
        "anniversaire_general": "la personne concernée",
        "naissance": "l'heureux événement",
        "mariage": "les mariés",
        "noel": "vos proches",
        "saint_valentin": "votre moitié",
        "fete_meres": "votre mère",
        "fete_peres": "votre père",
        "diplome": "le/la diplômé(e)",
    }
    return mapping.get(date_type, "la personne concernée")


def _get_gift_suggestions(date_type: str, tags: dict, produits: list) -> list:
    """Génère des suggestions de cadeaux basées sur le type et le profil."""
    suggestions = []
    
    # Suggestions par type de date
    type_suggestions = {
        "anniversaire_epouse": ["sac", "bijou", "foulard", "parfum"],
        "anniversaire_mari": ["ceinture", "portefeuille", "montre", "cravate"],
        "anniversaire_enfant": ["maroquinerie", "lunettes", "parfum"],
        "anniversaire_mariage": ["bijou", "montre", "voyage cadeau"],
        "naissance": ["médaille", "bracelet enfant", "coffret naissance"],
        "mariage": ["coffret cadeau", "foulard", "montre"],
        "noel": ["parfum", "foulard", "maroquinerie"],
        "saint_valentin": ["bijou", "parfum", "foulard en soie"],
        "diplome": ["montre", "stylo", "porte-documents"],
    }
    
    base_suggestions = type_suggestions.get(date_type, ["coffret cadeau", "parfum"])
    
    # Affiner avec les couleurs/matières préférées du client
    couleurs = tags.get("couleurs", [])
    matieres = tags.get("matieres", [])
    
    for s in base_suggestions[:3]:
        desc = s
        if couleurs:
            desc += f" en {couleurs[0]}" if isinstance(couleurs, list) else f" en {couleurs}"
        if matieres:
            mat = matieres[0] if isinstance(matieres, list) else matieres
            desc += f" ({mat})"
        suggestions.append(desc)
    
    return suggestions


def _get_canal(tags: dict) -> str:
    """Récupère le canal préféré."""
    canaux = tags.get("canaux_contact", [])
    if isinstance(canaux, list) and canaux:
        return canaux[0]
    return "Email"


def _build_message(civilite: str, date_info: dict, destinataire: str, suggestions: list) -> str:
    """Construit le message vendeur."""
    date_label = date_info.get("label", "une date importante")
    date_str = date_info.get("date_str", "")
    date_mention = f" ({date_str})" if date_str else ""
    
    suggestions_str = ", ".join(suggestions[:3]) if suggestions else "une pièce d'exception"
    
    return (
        f"Bonjour {civilite}, {date_label}{date_mention} approche pour {destinataire}. "
        f"Je me suis permis de préparer une sélection qui pourrait vous plaire : "
        f"{suggestions_str}. "
        f"Souhaitez-vous que je vous les présente lors d'un rendez-vous privé ?"
    )
