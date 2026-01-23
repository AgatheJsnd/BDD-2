"""
Taxonomie complète des tags pour profils clients LVMH
Structure hiérarchique de tous les tags possibles
"""

TAXONOMY = {
    "identite": {
        "genre": ["Femme", "Homme"],
        "age": ["18-25", "26-35", "36-45", "46-55", "56+"],
        "statut_relationnel": ["VIP", "Fidèle", "Régulier", "Occasionnel", "Nouveau"],
        "situation_familiale": ["Célibataire", "Couple", "Marié(e)", "Avec_enfants", "Famille_élargie"],
        "langue_parlee": ["Français", "Anglais", "Italien", "Espagnol", "Allemand", "Arabe", "Autres"],
        "profession": ["Entrepreneur", "Cadre", "Profession_libérale", "Artiste", "Étudiant", "Autres"]
    },
    
    "localisation": {
        "europe": ["Paris", "Berlin", "Milan", "Madrid", "London"],
        "amerique": ["New_York"],
        "moyen_orient_asie": ["Dubai", "Tokyo", "Hong_Kong", "Singapore"],
        "afrique": ["Maroc", "Tunisie", "Algérie", "Égypte", "Afrique_du_Sud", "Nigeria", "Kenya", "Autres"]
    },
    
    "mobilite_rythme_vie": {
        "residence": ["Principale", "Secondaire", "Multi_résidences"],
        "frequence_deplacement": ["Sédentaire", "Mobile", "Très_mobile"],
        "mode_transport": ["Avion_première", "Jet_privé", "Train_premium", "Voiture_chauffeur"],
        "saison_presence": ["Été_Europe", "Hiver_Dubai", "Toute_année"]
    },
    
    "lifestyle_centres_interet": {
        "sport": {
            "collectif": ["Football", "Basketball", "Rugby"],
            "individuel": ["Golf", "Tennis", "Yoga", "Running", "Fitness", "Ski"]
        },
        "musique": ["Classique", "Jazz", "Pop", "Rock", "Electro", "Opéra"],
        "animaux": {
            "domestiques": ["Chien", "Chat", "Cheval", "Autres"],
            "sauvages": ["Lion", "Éléphant", "Autres"],
            "aucun": []
        },
        "voyage": ["Luxe", "Aventure", "Culturel", "Détente"],
        "art_culture": ["Peinture", "Sculpture", "Musées", "Mode"],
        "gastronomie": ["Fine_dining", "Cuisine_locale", "Vins_spiritueux", "Vegan_healthy"]
    },
    
    "style_personnel": {
        "type_vetements": ["Casual", "Chic", "Business", "Sportswear", "Haute_couture"],
        "pieces_favorites": {
            "main": ["Sacs", "Chaussures", "Manteaux", "Robes_Costumes"],
            "accessoires": ["Chapeaux", "Ceintures", "Foulards", "Lunettes", "Bijoux", "Gants", "Montres"]
        },
        "couleurs_preferees": ["Noir", "Beige", "Bleu_marine", "Blanc", "Cognac", "Bordeaux", "Rose_gold", "Navy", "Gris", "Autres"],
        "matieres_preferees": ["Cuir", "Cachemire", "Soie", "Laine", "Coton", "Matières_vegan"],
        "sensibilite_mode": ["Tendance", "Intemporel", "Classique"]
    },
    
    "projet_achat": {
        "motif": ["Cadeau", "Mariage", "Anniversaire", "Diplôme", "Achat_personnel", "Voyage"],
        "budget": ["<5k", "5-10k", "10-15k", "15-25k", "25k+"],
        "timing": ["Urgent", "Date_fixée", "Long_terme"],
        "frequence_achat": ["Régulière", "Occasionnelle", "Rare"]
    },
    
    "appetence_evenementielle": {
        "type": ["Culturel", "Business", "Immersif", "Festif", "Intellectuel"],
        "format": ["One_to_one", "Petit_comité", "Groupe_sélect", "Grand_event"],
        "niveau_discretion": ["Très_discret", "Discret", "Visible"]
    },
    
    "relation_produit_innovation": {
        "attentes": ["Ultra_exclusif", "Personnalisable", "Fonctionnel", "Polyvalent", "Évolutif"],
        "usage": ["Quotidien", "Business", "Voyage", "Outdoor", "Cérémonie"],
        "frustrations": ["Manque_personnalisation", "Manque_fonctionnalité", "Manque_services", "Offre_trop_classique"]
    },
    
    "reseau_influence": {
        "influence": ["Leader_opinion", "Réseau_affluent", "Réseau_créatif", "Réseau_discret"],
        "role_marque": ["Ambassadeur", "Recommandant", "Acheteur_silencieux"]
    },
    
    "potentiel_innovation": ["Early_adopter", "Testeur_produit", "Co_création", "Feedback_structuré", "Faible_appétence"],
    
    "opportunites_marche": ["Travel_business_luxe", "Nomade_luxe", "Outdoor_chic", "Luxe_durable", "Luxe_tech", "Luxe_famille", "Luxe_bien_être"],
    
    "suivi": {
        "action": ["Rappeler", "Confirmer", "Preview_privée"],
        "echeance": ["M+1", "M+2", "M+3+"],
        "canal_contact": ["Email", "Téléphone", "WhatsApp", "Autres"]
    },
    
    # Métadonnées utiles pour le tagging
    "metadata": {
        "regime_alimentaire": ["Omnivore", "Végétarien", "Végane", "Pescetarien"],
        "allergies": []  # Liste dynamique
    }
}

# Mapping des langues du CSV vers la taxonomie
LANGUAGE_MAPPING = {
    "FR": "Français",
    "EN": "Anglais",
    "IT": "Italien",
    "ES": "Espagnol",
    "DE": "Allemand"
}
