"""
Activation 1 — Lifestyle & Voyage (Pilier Émotionnel)
Le Concierge de Luxe : détecte voyages/événements planifiés et propose un service personnalisé.
"""
from datetime import datetime, timedelta


def generate_lifestyle_voyage(client_id: str, tags: dict, extracted: dict, 
                               reference_date: datetime = None) -> list:
    """
    Génère des activations basées sur les projets de voyage/événements détectés.
    
    Args:
        client_id: ID du client
        tags: Tags extraits (30 catégories)
        extracted: Résultat de extract_all_actionable()
        reference_date: Date de référence pour les timers
    
    Returns:
        list[dict]: Activations générées
    """
    ref = reference_date or datetime.now()
    projets = extracted.get("projets_vie", [])
    activations = []
    
    for projet in projets:
        destination = projet.get("destination", projet.get("evenement", ""))
        date_estimee = projet.get("date_estimee")
        
        # Calculer la date de trigger (J-21)
        trigger_date = None
        priority = "MOYENNE"
        if date_estimee:
            try:
                dt = datetime.strptime(date_estimee, "%Y-%m-%d")
                trigger_date = (dt - timedelta(days=21)).strftime("%Y-%m-%d")
                # Si c'est dans moins de 21 jours, priorité haute
                if (dt - ref).days < 21:
                    priority = "HAUTE"
                    trigger_date = ref.strftime("%Y-%m-%d")
            except ValueError:
                pass
        
        # Déterminer le service proposé selon le type
        if projet["type"] == "voyage":
            service = _get_voyage_service(destination, tags)
        else:
            service = _get_evenement_service(projet.get("evenement", ""), tags)
        
        # Genre pour personnalisation
        genre = tags.get("genre", "")
        civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
        
        activations.append({
            "client_id": client_id,
            "activation_type": "lifestyle_voyage",
            "pillar": "Émotionnel",
            "priority": priority,
            "trigger_date": trigger_date,
            "canal_prefere": _get_canal(tags),
            "message_vendeur": _build_message(civilite, destination, service, projet["type"]),
            "context": {
                "type_projet": projet["type"],
                "destination": destination,
                "timing": projet.get("timing"),
                "service_propose": service,
            },
            "kpis": {
                "probabilite_conversion": 0.35,
                "valeur_estimee": "500-2000€",
            }
        })
    
    return activations


def _get_voyage_service(destination: str, tags: dict) -> str:
    """Recommande un service selon la destination."""
    dest_lower = destination.lower() if destination else ""
    
    if any(d in dest_lower for d in ["tokyo", "japon", "japan", "hong kong", "singapour"]):
        return "Sélection voyage Asie: pièces légères, shopping guide Tokyo"
    elif any(d in dest_lower for d in ["dubai", "abu dhabi", "émirats"]):
        return "Sélection Moyen-Orient: tenues soirée, accessoires prestige"
    elif any(d in dest_lower for d in ["courchevel", "megève", "chamonix", "val d'isère"]):
        return "Collection ski & montagne: cachemire, après-ski raffiné"
    elif any(d in dest_lower for d in ["saint-tropez", "côte d'azur", "maldives", "riviera"]):
        return "Sélection balnéaire: lunettes, sandales, tenues resort"
    elif any(d in dest_lower for d in ["new york", "los angeles", "miami"]):
        return "Sélection USA: style décontracté chic, sneakers premium"
    elif any(d in dest_lower for d in ["milan", "rome", "italie"]):
        return "Sélection Italie: élégance classique, cuir artisanal"
    else:
        return "Sélection voyage personnalisée selon votre destination"


def _get_evenement_service(evenement: str, tags: dict) -> str:
    """Recommande un service selon l'événement."""
    evt = evenement.lower() if evenement else ""
    
    if "gala" in evt:
        return "Tenue de gala complète: smoking/robe, accessoires, pochette"
    elif "mariage" in evt:
        return "Conseil mariage: tenue cérémonie + cadeau pour les mariés"
    elif "cocktail" in evt or "réception" in evt:
        return "Look cocktail: tenue semi-formelle, bijoux de soirée"
    elif "vernissage" in evt or "exposition" in evt:
        return "Style vernissage: look arty & sophistiqué"
    elif "dîner" in evt or "affaires" in evt:
        return "Business dinner look: costume/tailleur, montre, maroquinerie"
    else:
        return "Conseil événement personnalisé"


def _get_canal(tags: dict) -> str:
    """Récupère le canal préféré du client."""
    canaux = tags.get("canaux_contact", [])
    if isinstance(canaux, list) and canaux:
        return canaux[0]
    return "Email"


def _build_message(civilite: str, destination: str, service: str, type_projet: str) -> str:
    """Construit le message vendeur personnalisé."""
    if type_projet == "voyage":
        return (
            f"Bonjour {civilite}, j'espère que vos préparatifs pour {destination} "
            f"avancent bien ! Je me suis permis de vous préparer une sélection "
            f"spéciale : {service}. "
            f"Souhaitez-vous que je vous les réserve pour un essayage ?"
        )
    else:
        return (
            f"Bonjour {civilite}, j'ai appris que vous aviez un événement à venir. "
            f"Je vous propose : {service}. "
            f"N'hésitez pas à me contacter pour organiser un rendez-vous privé."
        )
