"""
Script de Gestion de la Taxonomie LVMH
Permet d'ajouter, modifier ou supprimer des tags facilement
"""
import json
import os
from pathlib import Path

# Chemin vers le fichier taxonomy
TAXONOMY_FILE = "config/taxonomy.py"

# Taxonomie actuelle (sera chargée depuis le fichier)
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
    "lifestyle_centres_interet": {
        "sport": {
            "collectif": ["Football", "Basketball", "Rugby"],
            "individuel": ["Golf", "Tennis", "Yoga", "Running", "Fitness", "Ski"]
        },
        "musique": ["Classique", "Jazz", "Pop", "Rock", "Electro", "Opéra"],
        "voyage": ["Luxe", "Aventure", "Culturel", "Détente"],
        "art_culture": ["Peinture", "Sculpture", "Musées", "Mode"],
        "gastronomie": ["Fine_dining", "Cuisine_locale", "Vins_spiritueux", "Vegan_healthy"]
    },
    "style_personnel": {
        "type_vetements": ["Casual", "Chic", "Business", "Sportswear", "Haute_couture"],
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
    "opportunites_marche": ["Travel_business_luxe", "Nomade_luxe", "Outdoor_chic", "Luxe_durable", "Luxe_tech", "Luxe_famille", "Luxe_bien_être"]
}


def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("🏷️  GESTIONNAIRE DE TAXONOMIE LVMH")
    print("="*60)
    print("\n1. 📋 Afficher toute la taxonomie")
    print("2. ➕ Ajouter un tag")
    print("3. ❌ Supprimer un tag")
    print("4. 🔍 Rechercher un tag")
    print("5. 💾 Sauvegarder la taxonomie")
    print("6. 📊 Statistiques")
    print("0. 🚪 Quitter")
    print("\n" + "="*60)


def afficher_taxonomie(taxonomy=None, prefix=""):
    """Affiche la taxonomie de manière hiérarchique"""
    if taxonomy is None:
        taxonomy = TAXONOMY
    
    for key, value in taxonomy.items():
        if isinstance(value, dict):
            print(f"{prefix}📁 {key}:")
            afficher_taxonomie(value, prefix + "  ")
        elif isinstance(value, list):
            print(f"{prefix}🏷️  {key}: {len(value)} tags")
            for tag in value:
                print(f"{prefix}   • {tag}")
        else:
            print(f"{prefix}   {key}: {value}")


def lister_categories():
    """Liste toutes les catégories disponibles"""
    categories = []
    
    def parcourir(d, path=""):
        for key, value in d.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, list):
                categories.append(current_path)
            elif isinstance(value, dict):
                parcourir(value, current_path)
    
    parcourir(TAXONOMY)
    return categories


def obtenir_categorie(chemin):
    """Obtient une catégorie par son chemin (ex: 'identite.genre')"""
    parts = chemin.split('.')
    current = TAXONOMY
    
    for part in parts[:-1]:
        if part in current:
            current = current[part]
        else:
            return None
    
    return current.get(parts[-1])


def definir_categorie(chemin, valeur):
    """Définit une catégorie par son chemin"""
    parts = chemin.split('.')
    current = TAXONOMY
    
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    current[parts[-1]] = valeur


def ajouter_tag():
    """Ajoute un tag à une catégorie"""
    print("\n📋 Catégories disponibles:")
    categories = lister_categories()
    
    for i, cat in enumerate(categories, 1):
        tags = obtenir_categorie(cat)
        print(f"{i}. {cat} ({len(tags)} tags)")
    
    try:
        choix = int(input("\nChoisissez une catégorie (numéro): ")) - 1
        if 0 <= choix < len(categories):
            categorie_choisie = categories[choix]
            tags_actuels = obtenir_categorie(categorie_choisie)
            
            print(f"\n🏷️  Tags actuels dans '{categorie_choisie}':")
            for tag in tags_actuels:
                print(f"   • {tag}")
            
            nouveau_tag = input("\n➕ Entrez le nouveau tag: ").strip()
            
            if nouveau_tag:
                if nouveau_tag in tags_actuels:
                    print(f"⚠️  Le tag '{nouveau_tag}' existe déjà!")
                else:
                    tags_actuels.append(nouveau_tag)
                    definir_categorie(categorie_choisie, tags_actuels)
                    print(f"✅ Tag '{nouveau_tag}' ajouté à '{categorie_choisie}'")
            else:
                print("❌ Tag vide, annulation.")
        else:
            print("❌ Choix invalide.")
    except ValueError:
        print("❌ Entrée invalide.")


def supprimer_tag():
    """Supprime un tag d'une catégorie"""
    print("\n📋 Catégories disponibles:")
    categories = lister_categories()
    
    for i, cat in enumerate(categories, 1):
        tags = obtenir_categorie(cat)
        print(f"{i}. {cat} ({len(tags)} tags)")
    
    try:
        choix = int(input("\nChoisissez une catégorie (numéro): ")) - 1
        if 0 <= choix < len(categories):
            categorie_choisie = categories[choix]
            tags_actuels = obtenir_categorie(categorie_choisie)
            
            print(f"\n🏷️  Tags dans '{categorie_choisie}':")
            for i, tag in enumerate(tags_actuels, 1):
                print(f"{i}. {tag}")
            
            choix_tag = int(input("\nQuel tag supprimer (numéro): ")) - 1
            
            if 0 <= choix_tag < len(tags_actuels):
                tag_supprime = tags_actuels.pop(choix_tag)
                definir_categorie(categorie_choisie, tags_actuels)
                print(f"✅ Tag '{tag_supprime}' supprimé de '{categorie_choisie}'")
            else:
                print("❌ Choix invalide.")
        else:
            print("❌ Choix invalide.")
    except ValueError:
        print("❌ Entrée invalide.")


def rechercher_tag():
    """Recherche un tag dans toute la taxonomie"""
    terme = input("\n🔍 Entrez le terme à rechercher: ").strip().lower()
    
    if not terme:
        print("❌ Terme vide.")
        return
    
    print(f"\n📊 Résultats pour '{terme}':")
    
    categories = lister_categories()
    resultats = 0
    
    for cat in categories:
        tags = obtenir_categorie(cat)
        tags_trouves = [tag for tag in tags if terme in tag.lower()]
        
        if tags_trouves:
            print(f"\n📁 {cat}:")
            for tag in tags_trouves:
                print(f"   • {tag}")
                resultats += 1
    
    if resultats == 0:
        print(f"❌ Aucun tag trouvé contenant '{terme}'")
    else:
        print(f"\n✅ {resultats} tag(s) trouvé(s)")


def statistiques():
    """Affiche des statistiques sur la taxonomie"""
    print("\n📊 STATISTIQUES DE LA TAXONOMIE")
    print("="*60)
    
    categories = lister_categories()
    total_tags = 0
    
    print(f"\n📁 Nombre de catégories: {len(categories)}")
    print(f"\n📋 Détails par catégorie:")
    
    for cat in categories:
        tags = obtenir_categorie(cat)
        nb_tags = len(tags)
        total_tags += nb_tags
        print(f"   • {cat}: {nb_tags} tags")
    
    print(f"\n🏷️  TOTAL: {total_tags} tags dans la taxonomie")
    print("="*60)


def sauvegarder_taxonomie():
    """Sauvegarde la taxonomie dans le fichier Python"""
    print("\n💾 Sauvegarde de la taxonomie...")
    
    # Créer le contenu du fichier
    content = '''"""
Taxonomie complète des tags pour profils clients LVMH
Structure hiérarchique de tous les tags possibles
"""

TAXONOMY = '''
    
    # Ajouter la taxonomie en JSON formaté
    content += json.dumps(TAXONOMY, indent=4, ensure_ascii=False)
    
    # Ajouter le mapping des langues
    content += '''

# Mapping des langues du CSV vers la taxonomie
LANGUAGE_MAPPING = {
    "FR": "Français",
    "EN": "Anglais",
    "IT": "Italien",
    "ES": "Espagnol",
    "DE": "Allemand"
}
'''
    
    # Créer le dossier config s'il n'existe pas
    os.makedirs("config", exist_ok=True)
    
    # Sauvegarder
    with open(TAXONOMY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Taxonomie sauvegardée dans '{TAXONOMY_FILE}'")
    print("⚠️  N'oubliez pas de redémarrer l'application Streamlit pour voir les changements!")


def main():
    """Fonction principale"""
    print("\n🎯 Bienvenue dans le Gestionnaire de Taxonomie LVMH")
    
    while True:
        afficher_menu()
        choix = input("\nVotre choix: ").strip()
        
        if choix == "1":
            print("\n📋 TAXONOMIE COMPLÈTE:")
            print("="*60)
            afficher_taxonomie()
        
        elif choix == "2":
            ajouter_tag()
        
        elif choix == "3":
            supprimer_tag()
        
        elif choix == "4":
            rechercher_tag()
        
        elif choix == "5":
            sauvegarder_taxonomie()
        
        elif choix == "6":
            statistiques()
        
        elif choix == "0":
            print("\n👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide. Essayez à nouveau.")


if __name__ == "__main__":
    main()
