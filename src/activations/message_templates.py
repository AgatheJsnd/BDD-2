"""
Templates de Messages — Modèles par type d'activation et par canal.
Permet de générer des messages personnalisés prêts à l'emploi.
"""


TEMPLATES = {
    "lifestyle_voyage": {
        "Email": {
            "objet": "Votre voyage à {destination} — Sélection personnalisée",
            "corps": (
                "Bonjour {civilite},\n\n"
                "J'espère que vos préparatifs pour {destination} avancent bien !\n\n"
                "Je me suis permis(e) de vous préparer une sélection spéciale :\n"
                "{service}\n\n"
                "Souhaitez-vous que je vous les réserve pour un essayage ?\n\n"
                "Bien cordialement,\n"
                "Votre conseiller(ère)"
            )
        },
        "WhatsApp": (
            "Bonjour {civilite} 👋 Vos préparatifs pour {destination} avancent ? "
            "J'ai sélectionné quelques pièces parfaites pour votre voyage. "
            "Je vous envoie les photos ? 📸"
        ),
        "SMS": (
            "Bonjour {civilite}, voyage à {destination} bientôt ? "
            "Une sélection spéciale vous attend en boutique. Rdv ?"
        ),
    },
    
    "gifting_dates": {
        "Email": {
            "objet": "{date_label} approche — Idées cadeaux personnalisées",
            "corps": (
                "Bonjour {civilite},\n\n"
                "{date_label} de {destinataire} approche{date_mention}.\n\n"
                "Je me suis permis(e) de préparer une sélection qui pourrait vous plaire :\n"
                "{suggestions}\n\n"
                "Souhaitez-vous que je vous les présente ?\n\n"
                "Bien cordialement"
            )
        },
        "WhatsApp": (
            "Bonjour {civilite} ! {date_label} de {destinataire} approche 🎁 "
            "J'ai quelques idées parfaites : {suggestions}. "
            "On se voit pour un rendez-vous ? 💫"
        ),
        "SMS": (
            "{date_label} de {destinataire} bientôt ! "
            "Idées cadeaux exclusives en boutique. RDV ?"
        ),
    },
    
    "next_best_product": {
        "Email": {
            "objet": "Le complément parfait de votre {produit_existant}",
            "corps": (
                "Bonjour {civilite},\n\n"
                "Je viens de recevoir un(e) {produit_suggere} "
                "qui s'accorderait parfaitement avec votre {produit_existant}.\n\n"
                "Même univers de couleur et de matière — {raison}.\n\n"
                "Souhaitez-vous le voir ?\n\n"
                "Bien cordialement"
            )
        },
        "WhatsApp": (
            "Bonjour {civilite} ! 🛍️ Nouvelle arrivée : un(e) {produit_suggere} "
            "parfait avec votre {produit_existant}. Photos ? 📷"
        ),
        "SMS": (
            "Nouveau {produit_suggere} parfait avec votre {produit_existant}. "
            "Réservé pour vous. Intéressé(e) ?"
        ),
    },
    
    "rupture_stock": {
        "Email": {
            "objet": "🎉 Votre {description} est de retour !",
            "corps": (
                "Bonjour {civilite},\n\n"
                "Bonne nouvelle ! Le/La {description} que vous cherchiez "
                "vient d'arriver !\n\n"
                "Je me suis permis(e) de vous le/la mettre de côté.\n\n"
                "Souhaitez-vous passer le récupérer ou préférez-vous une livraison ?\n\n"
                "Bien cordialement"
            )
        },
        "WhatsApp": (
            "🎉 {civilite}, le/la {description} est de retour ! "
            "Je vous l'ai réservé(e). Vous passez ou livraison ?"
        ),
        "SMS": (
            "Le/La {description} est arrivé(e) ! "
            "Réservé(e) pour vous. Boutique ou livraison ?"
        ),
    },
    
    "care_entretien": {
        "Email": {
            "objet": "Prenez soin de votre {produit} — Service d'entretien",
            "corps": (
                "Bonjour {civilite},\n\n"
                "Cela fait quelque temps que vous portez votre {produit}.\n\n"
                "{description}\n\n"
                "Notre service : {service}\n\n"
                "Souhaitez-vous prendre rendez-vous ?\n\n"
                "Bien cordialement"
            )
        },
        "WhatsApp": (
            "Bonjour {civilite} ! 🧹 Votre {produit} mérite un petit soin. "
            "On propose : {service}. RDV ?"
        ),
        "SMS": (
            "Entretien de votre {produit} ? "
            "{service}. Prenez RDV en boutique."
        ),
    },
    
    "cross_maison": {
        "Email": {
            "objet": "Découvrez {maison_cible} — Recommandation personnalisée",
            "corps": (
                "Bonjour {civilite},\n\n"
                "Sachant votre goût pour {keywords}, je me suis permis(e) "
                "de vous recommander notre Maison sœur {maison_cible}.\n\n"
                "{proposition}\n\n"
                "Puis-je organiser cela pour vous ?\n\n"
                "Bien cordialement"
            )
        },
        "WhatsApp": (
            "Bonjour {civilite} ! ✨ Vu votre passion pour {keywords}, "
            "notre Maison sœur {maison_cible} devrait vous plaire. "
            "{proposition}"
        ),
        "SMS": (
            "Découvrez {maison_cible} ! "
            "Sélection spéciale basée sur vos goûts. Intéressé(e) ?"
        ),
    },
}


def get_template(activation_type: str, canal: str = "Email") -> dict:
    """
    Retourne le template de message pour un type d'activation et un canal.
    
    Returns:
        Template (dict pour Email avec objet+corps, str pour WhatsApp/SMS)
    """
    type_templates = TEMPLATES.get(activation_type, {})
    return type_templates.get(canal, type_templates.get("Email", ""))


def format_message(activation: dict, canal: str = None) -> str:
    """
    Formate un message personnalisé à partir d'une activation et de son contexte.
    
    Args:
        activation: Dict d'activation (issu de l'engine)
        canal: Canal de communication (Email, WhatsApp, SMS). None = canal_prefere
    
    Returns:
        str: Message formaté prêt à envoyer
    """
    canal = canal or activation.get("canal_prefere", "Email")
    atype = activation.get("activation_type", "")
    context = activation.get("context", {})
    
    template = get_template(atype, canal)
    
    if not template:
        return activation.get("message_vendeur", "")
    
    # Préparer les variables de remplacement
    variables = {
        "civilite": "",
        **context,
    }
    
    # Formater les listes en strings
    for k, v in variables.items():
        if isinstance(v, list):
            variables[k] = ", ".join(str(x) for x in v[:3])
    
    try:
        if isinstance(template, dict):
            # Email : objet + corps
            objet = template.get("objet", "").format(**variables)
            corps = template.get("corps", "").format(**variables)
            return f"Objet: {objet}\n\n{corps}"
        else:
            return template.format(**variables)
    except (KeyError, IndexError):
        # Fallback: message déjà rédigé par le module
        return activation.get("message_vendeur", "")
