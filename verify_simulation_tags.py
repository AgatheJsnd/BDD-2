import csv
import json
import re
from src.profile_generator import ProfileGenerator

def load_simulated_data(filename="simulation_new.csv"):
    data = {}
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['ID']] = row
    return data

def verify_tags():
    print("="*60)
    print("VÉRIFICATION DES TAGS SIMULÉS")
    print("="*60)

    sim_data = load_simulated_data()
    pg = ProfileGenerator()
    
    total = len(sim_data)
    processed = 0
    missing_tags = 0
    
    issues = []
    
    # Mots clés attendus (basé sur generate_simulation_data.py)
    # PRODUCTS = ["sac Capucines", "montre Tambour", "parfum Sauvage", "robe de soirée", "costume sur mesure", "sneakers Run Away"]
    # COLORS = ["rouge", "noir", "bleu", "or", "argent", "rose poudré", "beige"]
    # BUDGETS = ["1000", "5000", "10000", "unlimited", "flexible", "20000", "50000"]

    for client_id, expected in sim_data.items():
        profile = pg.get_profile(client_id)
        
        if not profile:
            print(f"❌ {client_id}: Profil non trouvé en base !")
            continue
            
        processed += 1
        transcription = expected['Transcription'].lower()
        
        # --- Vérification Projet Achat (Produit / Budget) ---
        projet = profile.get('projet_achat', {})
        budget_tag = projet.get('budget')
        product_tags = projet.get('type_produit', [])
        
        # Check Budget
        expected_budget = None
        if "budget" in transcription:
            # Extraction simple pour check grossier
            if "flexible" in transcription: expected_budget = "flexible"
            elif "unlimited" in transcription: expected_budget = "unlimited"
            # Les chiffres c'est plus dur à matcher parfaitement avec string exact mais on essaye
        
        # Check Couleur
        style = profile.get('style_personnel', {})
        colors_detected = style.get('couleurs_preferees', [])
        if isinstance(colors_detected, str): colors_detected = [colors_detected]
        
        missing_in_this_profile = []
        
        # Test Couleur spécifique (car facile à vérifier)
        known_colors = ["rouge", "noir", "bleu", "or", "argent", "rose poudré", "beige"]
        for c in known_colors:
            if c in transcription and c not in [str(x).lower() for x in colors_detected]:
                # Cas particulier: "rose poudré" peut être taggé "rose" ou autre, on est souple
                if c == "rose poudré" and "rose" in [str(x).lower() for x in colors_detected]: continue
                missing_in_this_profile.append(f"Couleur manquante: {c}")

        # Test Produit (keywords)
        known_products = {
            "sac": "Maroquinerie",
            "montre": "Joaillerie/Montres",
            "parfum": "Parfums",
            "robe": "Prêt-à-porter",
            "costume": "Prêt-à-porter",
            "sneakers": "Souliers"
        }
        # Note: ceci dépend de la taxonomie exacte, ici on check juste si on a *quelque chose*
        
        has_product_tag = False
        if product_tags: has_product_tag = True
        
        # On vérifie juste si la transcription n'est pas vide/courte
        if len(transcription) > 10 and not has_product_tag and not budget_tag and not colors_detected:
             missing_in_this_profile.append("Aucun tag principal détecté (Vide ?)")

        # Check Dirty XSS stripping
        # Si le profil contient <script> dans les champs texte, c'est grave
        profile_str = json.dumps(profile)
        if "<script>" in profile_str:
             missing_in_this_profile.append("CRITIQUE: Injection XSS non nettoyée en DB !")

        if missing_in_this_profile:
            missing_tags += 1
            issues.append({
                "id": client_id,
                "text": transcription[:60]+"...",
                "tags_found": f"Budget: {budget_tag}, Colors: {colors_detected}",
                "issues": missing_in_this_profile
            })

    print(f"\n📊 RÉSULTATS")
    print(f"Total attendus : {total}")
    print(f"Profils trouvés : {processed}")
    print(f"Succès total (sans manques évidents) : {processed - missing_tags} ({((processed - missing_tags)/total)*100:.1f}%)")
    print(f"Profils avec tags manquants ou soucis : {missing_tags}")
    
    if issues:
        print("\n⚠️ DÉTAILS DES PROBLÈMES (Top 10) :")
        for i in issues[:10]:
            print(f"\n[{i['id']}]")
            print(f"Txt: {i['text']}")
            print(f"Tags: {i['tags_found']}")
            for issue in i['issues']:
                print(f"  ❌ {issue}")

if __name__ == "__main__":
    verify_tags()
