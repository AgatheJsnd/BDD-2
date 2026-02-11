"""
Activation 5 — Care & Entretien (Pilier Service)
La Durabilité : propose des services d'entretien pour les pièces achetées.
"""
from datetime import datetime, timedelta


# Règles d'entretien par catégorie de produit
ENTRETIEN_RULES = {
    "sac": {
        "service": "Nettoyage professionnel et imperméabilisation cuir",
        "delai_mois": 12,
        "description": "Un nettoyage et un traitement imperméabilisant prolongeront la vie de votre sac.",
    },
    "portefeuille": {
        "service": "Rénovation cuir et teinture retouche",
        "delai_mois": 18,
        "description": "Un portefeuille en cuir mérite un soin régulier pour garder sa souplesse.",
    },
    "chaussures": {
        "service": "Ressemelage, cirage et patine artisanale",
        "delai_mois": 6,
        "description": "Pour que vos souliers gardent leur éclat, un soin complet en atelier.",
    },
    "montre": {
        "service": "Révision complète du mouvement et polissage",
        "delai_mois": 24,
        "description": "Une révision régulière garantit la précision et la longévité de votre montre.",
    },
    "ceinture": {
        "service": "Nettoyage cuir et remplacement boucle si besoin",
        "delai_mois": 18,
        "description": "Un entretien de votre ceinture pour maintenir son aspect neuf.",
    },
    "bijou": {
        "service": "Nettoyage aux ultrasons et vérification des sertis",
        "delai_mois": 12,
        "description": "Un nettoyage professionnel pour raviver l'éclat de vos bijoux.",
    },
    "lunettes": {
        "service": "Ajustement, nettoyage et vérification des verres",
        "delai_mois": 12,
        "description": "Un contrôle régulier pour un confort optimal.",
    },
    "foulard": {
        "service": "Pressing spécialisé soie/cachemire",
        "delai_mois": 6,  # Saisonnier
        "description": "Un pressing spécialisé pour préserver la qualité de la fibre.",
    },
    "costume": {
        "service": "Pressing haute couture et retouches si besoin",
        "delai_mois": 6,
        "description": "Un pressing spécialisé pour garder la coupe impeccable.",
    },
    "pull": {
        "service": "Anti-bouloches et pressing cachemire",
        "delai_mois": 6,
        "description": "Un traitement anti-bouloches pour prolonger la vie de votre pull.",
    },
    "manteau": {
        "service": "Nettoyage professionnel et imperméabilisation",
        "delai_mois": 12,
        "description": "Un entretien annuel pour préparer votre manteau à la saison.",
    },
    "maroquinerie": {
        "service": "Nettoyage, nourrissage et réparation cuir",
        "delai_mois": 12,
        "description": "Un traitement complet pour maintenir la qualité de votre maroquinerie.",
    },
}


def generate_care_entretien(client_id: str, tags: dict, extracted: dict,
                             reference_date: datetime = None) -> list:
    """
    Génère des activations d'entretien basées sur les produits possédés.
    Le trigger est calculé : date d'achat + délai entretien.
    
    Note: Sans date d'achat exacte, on utilise la date de la transcription
    comme approximation + le délai standard.
    """
    ref = reference_date or datetime.now()
    produits = extracted.get("produits", [])
    activations = []
    
    for p in produits:
        produit_type = p.get("produit", "")
        
        if produit_type not in ENTRETIEN_RULES:
            continue
        
        rules = ENTRETIEN_RULES[produit_type]
        
        # Calculer la date de trigger (date ref + délai)
        trigger_dt = ref + timedelta(days=rules["delai_mois"] * 30)
        trigger_date = trigger_dt.strftime("%Y-%m-%d")
        
        # Priorité basée sur la proximité
        days_since = (ref - ref).days  # 0 par défaut sans date d'achat
        priority = "BASSE"
        
        # Description produit
        desc = produit_type
        if p.get("marque"):
            desc = f"{p['marque']} {produit_type}"
        if p.get("couleur"):
            desc += f" {p['couleur']}"
        
        genre = tags.get("genre", "")
        civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
        
        activations.append({
            "client_id": client_id,
            "activation_type": "care_entretien",
            "pillar": "Service",
            "priority": priority,
            "trigger_date": trigger_date,
            "canal_prefere": _get_canal(tags),
            "message_vendeur": (
                f"Bonjour {civilite}, cela fait quelque temps que vous portez "
                f"votre {desc}. {rules['description']} "
                f"Notre service : {rules['service']}. "
                f"Souhaitez-vous prendre rendez-vous ?"
            ),
            "context": {
                "produit": produit_type,
                "marque": p.get("marque"),
                "service": rules["service"],
                "delai_mois": rules["delai_mois"],
            },
            "kpis": {
                "probabilite_conversion": 0.30,
                "valeur_estimee": "50-300€",
            }
        })
    
    return activations


def _get_canal(tags: dict) -> str:
    canaux = tags.get("canaux_contact", [])
    if isinstance(canaux, list) and canaux:
        return canaux[0]
    return "Email"
