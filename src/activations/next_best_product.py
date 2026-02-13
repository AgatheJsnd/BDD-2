"""
Activation 3 — Next Best Product (Pilier Produit)
Le Complément Parfait : analyse le profil style et suggère des compléments cohérents.
"""
from datetime import datetime


# Matrice de complémentarité produit
COMPLEMENTARITE = {
    "sac": ["portefeuille", "ceinture", "foulard", "porte-clés"],
    "portefeuille": ["sac", "porte-cartes", "ceinture"],
    "ceinture": ["sac", "chaussures", "portefeuille"],
    "chaussures": ["ceinture", "sac", "chaussettes de luxe"],
    "costume": ["cravate", "chaussures", "boutons de manchette", "pochette de costume"],
    "montre": ["bracelet", "boutons de manchette", "porte-montre"],
    "lunettes": ["étui", "foulard", "chapeau"],
    "foulard": ["sac", "broche", "lunettes"],
    "cravate": ["costume", "pochette de costume", "boutons de manchette"],
    "bijou": ["montre", "foulard en soie", "coffret bijoux"],
    "parfum": ["bougie parfumée", "lait pour le corps", "coffret parfum"],
    "chemise": ["cravate", "costume", "boutons de manchette"],
    "pull": ["foulard", "manteau", "chapeau"],
    "manteau": ["foulard", "gants", "chapeau"],
    "robe": ["pochette", "bijou", "chaussures"],
    "maroquinerie": ["portefeuille", "porte-clés", "étui"],
}


def generate_next_best_product(client_id: str, tags: dict, extracted: dict,
                                reference_date: datetime = None) -> list:
    """
    Analyse les pièces/couleurs/matières préférées du client et suggère des compléments.
    """
    ref = reference_date or datetime.now()
    produits = extracted.get("produits", [])
    activations = []
    
    # Récupérer les préférences du profil tags
    couleurs_pref = tags.get("couleurs", [])
    matieres_pref = tags.get("matieres", [])
    marques_pref = tags.get("marques_preferees", [])
    pieces_pref = tags.get("pieces_favorites", [])
    
    # Combiner avec les produits extraits
    all_products = set()
    for p in produits:
        all_products.add(p["produit"])
    if isinstance(pieces_pref, list):
        for p in pieces_pref:
            all_products.add(p.lower())
    
    if not all_products:
        return []
    
    # Générer les compléments
    suggestions_seen = set()
    for produit in all_products:
        complements = COMPLEMENTARITE.get(produit, [])
        
        for complement in complements:
            if complement in suggestions_seen or complement in all_products:
                continue
            suggestions_seen.add(complement)
            
            # Construire la description avec les préférences couleur/matière
            desc = complement
            couleur_match = couleurs_pref[0] if couleurs_pref else None
            matiere_match = matieres_pref[0] if matieres_pref else None
            marque_match = marques_pref[0] if marques_pref else None
            
            if couleur_match:
                desc = f"{complement} {couleur_match}"
            if matiere_match:
                desc += f" en {matiere_match}"
            if marque_match:
                desc = f"{desc} {marque_match}"
            
            genre = tags.get("genre", "")
            civilite = "Madame" if genre == "F" else "Monsieur" if genre == "M" else ""
            
            activations.append({
                "client_id": client_id,
                "activation_type": "next_best_product",
                "pillar": "Produit",
                "priority": "HAUTE" if len(complements) <= 2 else "MOYENNE",
                "trigger_date": ref.strftime("%Y-%m-%d"),
                "canal_prefere": _get_canal(tags),
                "message_vendeur": (
                    f"Bonjour {civilite}, je viens de recevoir un(e) {desc} "
                    f"qui s'accorderait parfaitement avec votre {produit}. "
                    f"Même univers de couleur et de matière — c'est le complément idéal. "
                    f"Souhaitez-vous le voir ?"
                ),
                "context": {
                    "produit_existant": produit,
                    "produit_suggere": complement,
                    "couleur_match": couleur_match,
                    "matiere_match": matiere_match,
                    "marque_match": marque_match,
                    "raison": f"Complémentarité avec {produit}",
                },
                "kpis": {
                    "probabilite_conversion": 0.45,
                    "valeur_estimee": "400-2000€",
                }
            })
    
    # Limiter à 3 suggestions max par client
    return sorted(activations, key=lambda x: x["priority"], reverse=True)[:3]


def _get_canal(tags: dict) -> str:
    canaux = tags.get("canaux_contact", [])
    if isinstance(canaux, list) and canaux:
        return canaux[0]
    return "Email"
