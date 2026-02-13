"""
Activation 4 — Rupture de Stock (Pilier Produit)
Le Waitlist Killer : détecte les demandes en attente et prépare des alertes retour stock.
"""
from datetime import datetime


def generate_rupture_stock(client_id: str, tags: dict, extracted: dict,
                           reference_date: datetime = None) -> list:
    """
    Génère des activations pour les produits demandés en rupture de stock.
    Priorité HAUTE, canal WhatsApp pour l'immédiateté.
    """
    ref = reference_date or datetime.now()
    demandes = extracted.get("demandes_attente", [])
    activations = []
    
    for demande in demandes:
        produit = demande.get("produit", "non spécifié")
        marque = demande.get("marque", "")
        taille = demande.get("taille", "")
        couleur = demande.get("couleur", "")
        
        # Description produit
        desc_parts = []
        if marque:
            desc_parts.append(marque)
        desc_parts.append(produit)
        if couleur:
            desc_parts.append(couleur)
        if taille:
            desc_parts.append(f"taille {taille}")
        desc = " ".join(desc_parts)
        
        genre = tags.get("genre", "")
        civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
        
        activations.append({
            "client_id": client_id,
            "activation_type": "rupture_stock",
            "pillar": "Produit",
            "priority": "HAUTE",
            "trigger_date": ref.strftime("%Y-%m-%d"),  # Dès retour en stock
            "canal_prefere": "WhatsApp",  # Canal prioritaire pour l'urgence
            "message_vendeur": (
                f"Bonne nouvelle {civilite} ! Le/La {desc} que vous cherchiez "
                f"vient d'arriver ce matin. "
                f"Je me suis permis(e) de vous le/la mettre de côté. "
                f"Souhaitez-vous passer le récupérer ou préférez-vous une livraison ?"
            ),
            "context": {
                "produit": produit,
                "marque": marque,
                "taille": taille,
                "couleur": couleur,
                "statut": "en_attente_retour_stock",
                "description": desc,
            },
            "kpis": {
                "probabilite_conversion": 0.75,
                "valeur_estimee": "500-5000€",
            }
        })
    
    return activations
