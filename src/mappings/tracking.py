"""
Module Tracking - Actions, Échéances, Canaux de contact
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# ACTIONS CRM
# ============================================================================

ACTIONS_MAPPING = {
    "Rappeler": [
        "rappeler", "call back", "recontacter", "contact again",
        "relancer", "follow up"
    ],
    "Confirmer": [
        "confirmer", "confirm", "confirmation", "valider", "validate"
    ],
    "Relancer": [
        "relancer", "follow up", "reminder", "rappel", "relance"
    ],
    "Invitation": [
        "invitation", "invite", "inviter", "événement", "event"
    ],
    "Preview_privee": [
        "preview privée", "private preview", "avant-première",
        "exclusive preview", "présentation privée"
    ]
}

# ============================================================================
# ÉCHÉANCES
# ============================================================================

ECHEANCES_MAPPING = {
    "M_1": [
        "dans un mois", "in one month", "m+1", "mois prochain",
        "next month"
    ],
    "M_2": [
        "dans deux mois", "in two months", "m+2", "dans 2 mois"
    ],
    "M_3": [
        "dans trois mois", "in three months", "m+3", "dans 3 mois",
        "trimestre prochain"
    ],
    "M_3_plus": [
        "plus de 3 mois", "more than 3 months", "m+3+",
        "long terme", "long term"
    ]
}

# ============================================================================
# CANAUX DE CONTACT PRÉFÉRÉS
# ============================================================================

CANAUX_MAPPING = {
    "Email": [
        "email", "e-mail", "mail", "courriel", "par mail",
        "adresse email", "email address"
    ],
    "Telephone": [
        "téléphone", "phone", "appel", "call", "par téléphone",
        "numéro de téléphone", "phone number"
    ],
    "SMS": [
        "sms", "texto", "text message", "message", "par sms"
    ],
    "WhatsApp": [
        "whatsapp", "whats app", "wa", "par whatsapp"
    ],
    "Reseaux_sociaux": [
        "réseaux sociaux", "social media", "instagram", "facebook",
        "linkedin", "dm", "message privé"
    ],
    "Site_web": [
        "site web", "website", "en ligne", "online", "internet"
    ]
}
