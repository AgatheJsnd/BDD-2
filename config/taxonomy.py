"""
Taxonomie complète des tags pour profils clients LVMH
Structure hiérarchique mise à jour selon les nouveaux besoins
"""

TAXONOMY = {
    "identite": {
        "genre": ["Femme", "Homme", "Autre"],
        "age": ["18-25", "26-35", "36-45", "46-55", "56+"],
        "statut_relationnel": ["VIP", "Fidèle", "Nouveau", "Régulier", "Occasionnel"],
        "situation_familiale": ["Célibataire", "Couple", "Marié(e)", "Avec enfants", "Famille élargie"],
        "langue_parlee": ["Français", "Anglais", "Italien", "Espagnol", "Allemand", "Portugais", "Arabe", "Russe", "Mandarin", "Japonais", "Coréen", "Hindi", "Autres"],
        "profession_secteur": {
            "Entrepreneur_Dirigeant": [],
            "Cadre_Manager": [],
            "Profession_liberale": ["Avocat", "Médecin", "Architecte", "Consultant"],
            "Finance_Investissement": ["Banquier", "Trader", "Gestionnaire de patrimoine"],
            "Art_Creation": ["Artiste", "Designer", "Photographe", "Musicien"],
            "Mode_Luxe": ["Styliste", "Acheteur mode", "Retail luxe"],
            "Tech_Digital": ["Ingénieur", "Développeur", "Data / IA", "Product manager"],
            "Medias_Communication": ["Journaliste", "Marketing", "Relations publiques"],
            "Sport": ["Athlète", "Coach", "Dirigeant sportif"],
            "Etudiant": [],
            "Retraite": [],
            "Autres": []
        }
    },
    
    "localisation": {
        "europe": ["Paris", "Berlin", "Milan", "Madrid", "London"],
        "amerique": ["Los Angeles", "New York"],
        "moyen_orient_asie": ["Dubai", "Tokyo", "Hong Kong", "Singapore"],
        "afrique": ["Maroc", "Égypte", "Afrique du Sud", "Autre"]
    },
    
    "lifestyle_centres_interet": {
        "sport": {
            "collectif": ["Football", "Handball", "Basketball", "Volleyball", "Hockey", "Rugby"],
            "individuel": {
                "raquette": ["Tennis", "Padel", "Squash", "Badminton"],
                "outdoor": ["Golf", "Ski", "Surf", "Escalade", "Randonnée"],
                "bien_etre": ["Yoga", "Pilates", "Méditation"],
                "endurance": ["Running", "Cyclisme", "Natation"],
                "fitness_musculation": [],
                "mecanique": ["Formule 1", "Moto GP", "Rallye"]
            }
        },
        "musique": {
            "classique_elegant": ["Classique", "Opéra", "Musique instrumentale"],
            "moderne_populaire": ["Pop", "Rock", "Hip-hop / Rap", "R&B"],
            "electronique": ["Electro", "House", "Techno"],
            "jazz_soul": ["Jazz", "Soul / Blues"],
            "ambiance": ["Chill", "Lounge", "Lo-fi"],
            "musique_du_monde": ["Latine", "Africaine", "Asiatique"]
        },
        "animaux": {
            "domestiques": ["Chien", "Chat", "Cheval", "Oiseaux", "Autres"],
            "exotiques": ["Reptiles", "Poissons", "Autres"],
            "aucun": []
        },
        "voyage": {
            "experience": ["Luxe", "Aventure", "Culturel", "Détente", "Road trip", "City trip"],
            "style_sejour": ["Hôtel 5★ / Palace", "Resort", "Villa privée", "Croisière", "Airbnb"],
            "destination_pref": ["Plage", "Montagne", "Désert", "Nature sauvage", "Grandes villes"],
            "frequence": ["Très fréquent", "Occasionnel", "Rare"]
        },
        "art_culture": {
            "arts_visuels": ["Peinture", "Sculpture", "Photographie", "Art contemporain"],
            "lieux_culturels": ["Musées", "Galeries d'art", "Monuments historiques"],
            "spectacles": ["Théâtre", "Danse", "Concerts"],
            "cinema_litterature": ["Cinéma", "Lecture"],
            "mode": ["Défilés", "Créateurs", "Tendances"]
        },
        "gastronomie": {
            "type_cuisine": ["Fine dining", "Cuisine locale", "Cuisine du monde", "Street food premium"],
            "boissons": ["Vins", "Champagnes", "Spiritueux", "Cocktails"],
            "experiences": ["Restaurants étoilés", "Dîners privés", "Cours de cuisine"],
            "preferences": ["Gastronomie traditionnelle", "Cuisine légère / équilibrée", "Aucune restriction"]
        }
    },
    
    "style_personnel": {
        "type_vetements": ["Casual", "Chic / Élégant", "Business / Formel", "Sportwear", "Haute couture / Luxe"],
        "pieces_favorites": {
            "sacs": ["Sac à main", "Sac à dos", "Sac de voyage", "Pochette"],
            "chaussures": ["Baskets / Sneakers", "Escarpins", "Bottes", "Bottines", "Mocassins", "Derbies / Richelieus", "Sandales", "Talons", "Chaussures de sport"],
            "manteaux": ["Trench", "Manteau laine", "Doudoune", "Cape", "Manteau long", "Veste légère"],
            "robes": ["Robe courte", "Robe longue", "Robe de soirée", "Robe de cocktail"],
            "costumes": ["Costume classique", "Costume business", "Smoking / soirée"],
            "accessoires": ["Chapeaux", "Ceintures", "Foulards", "Lunettes", "Bijoux", "Gants", "Montres"]
        },
        "couleurs_preferees": {
            "neutres_intemporelles": ["Noir", "Blanc", "Beige", "Gris", "Bleu marine"],
            "tons_chauds": ["Cognac", "Marron", "Bordeaux", "Rouge", "Orange"],
            "tons_froids": ["Bleu", "Vert", "Kaki", "Violet"],
            "pastels": ["Rose poudré", "Bleu ciel", "Lavande", "Menthe"],
            "metalliques": ["Or", "Argent", "Bronze"]
        },
        "matieres_preferees": {
            "naturelles": ["Cuir", "Cachemire", "Soie", "Laine", "Coton", "Lin", "Denim"],
            "premium": ["Cuir exotique", "Fourrure", "Velours", "Tweed"],
            "techniques": ["Nylon", "Polyester", "Gore-Tex", "Matières sport"],
            "alternatives": ["Matières vegan", "Matières recyclées", "Éco-responsables"]
        },
        "sensibilite_mode": ["Tendance", "Intemporel", "Classique"],
        "mensurations": {
            "taille_vetements": ["XXS", "XS", "S", "M", "L", "XL", "Sur-mesure"],
            "pointure": ["35-37", "38-40", "41-43", "44-46", "Autres"],
            "coupe": ["Ajustée", "Oversize", "Standard"],
            "morphologie": ["Silhouette fine", "Silhouette moyenne", "Silhouette athlétique", "Silhouette généreuse"]
        }
    },
    
    "projet_achat": {
        "motif_role": {
            "offrir": ["Cadeau", "Anniversaire", "Mariage", "Diplôme", "Naissance", "Fêtes"],
            "pour_soi": ["Plaisir personnel", "Renouvellement garde-robe", "Événement spécial", "Voyage", "Investissement pièce iconique"]
        },
        "budget": ["<5k", "5–10k", "10–15k", "15–25k", "25k+", "Flexible"],
        "timing": ["Urgent", "Date fixée", "Projet long terme"],
        "marques_preferees": {
            "Louis Vuitton": ["Maroquinerie", "Prêt-à-porter luxe", "Accessoires", "Montres & joaillerie"],
            "Dior": ["Parfum", "Make-up", "Prêt-à-porter"],
            "Gucci": ["Prêt-à-porter", "Maroquinerie", "Chaussures", "Accessoires"],
            "Loro Piana": ["Cachemire", "Prêt-à-porter haut de gamme", "Textiles rares"],
            "Bulgari": ["Haute joaillerie", "Montres"],
            "Givenchy Beauty": ["Parfum", "Make-up", "Soins"],
            "Tiffany & Co.": ["Joaillerie", "Montres", "Accessoires"],
            "Celine": ["Prêt-à-porter", "Maroquinerie", "Accessoires"],
            "Fendi": ["Prêt-à-porter", "Maroquinerie", "Fourrure & cuir"],
            "Sephora": ["Make-up", "Soins", "Parfums"]
        },
        "frequence_achat": ["Régulière", "Occasionnelle", "Rare"]
    },
    
    "preferences_contraintes": {
        "regime": ["Vegan", "Végétarien", "Pescétarien", "Autre", "Aucun"],
        "allergies": {
            "alimentaires": ["Gluten", "Lactose", "Fruits à coque", "Autres"],
            "cutanees": ["Nickel", "Latex", "Autres"],
            "aucune": []
        },
        "valeurs": ["Éthique / durable", "Qualité & savoir-faire", "Exclusivité", "Standard"]
    },
    
    "suivi": {
        "action": ["Rappeler", "Confirmer", "Relancer", "Inviter", "Preview privée"],
        "echeance": ["M+1", "M+2", "M+3", "M+3+"],
        "canal_contact": ["Email", "Téléphone", "SMS", "WhatsApp", "Réseaux sociaux", "Site web"]
    }
}

# Mapping des langues du CSV vers la taxonomie
LANGUAGE_MAPPING = {
    "FR": "Français",
    "EN": "Anglais",
    "IT": "Italien",
    "ES": "Espagnol",
    "DE": "Allemand",
    "RU": "Russe",
    "PT": "Portugais",
    "AR": "Arabe",
    "ZH": "Mandarin",
    "JA": "Japonais",
    "KO": "Coréen"
}
