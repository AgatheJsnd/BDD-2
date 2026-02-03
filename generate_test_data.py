"""
Générateur de données de test pour LVMH Client Analytics
Crée un CSV de 500 clients avec des cas variés pour stress-test
"""
import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_CLIENTS = 500

# Données de base pour la génération
LANGUAGES = ["FR", "EN", "IT", "ES", "DE", "AR", "PT", "ZH", "JA"]  # Inclut langues non supportées
DURATIONS = ["5 min", "10 min", "15 min", "20 min", "25 min", "30 min", "35 min", "40 min", "45 min", "50 min", "55 min", "60 min", "90 min", "120 min"]
LENGTHS = ["short", "medium", "long"]

# Professions variées
PROFESSIONS_FR = ["avocat", "médecin", "chirurgien", "architecte", "entrepreneur", "banquier", "designer", "artiste", "professeur", "diplomate", "consultant", "ingénieur", "pilote", "chef étoilé", "producteur cinéma", "influenceur", "athlète professionnel", "musicien", "galeriste"]
PROFESSIONS_EN = ["lawyer", "doctor", "surgeon", "architect", "entrepreneur", "banker", "designer", "artist", "professor", "diplomat", "consultant", "engineer", "pilot", "chef", "film producer", "influencer", "professional athlete", "musician", "gallery owner"]

# Sports
SPORTS = ["golf", "tennis", "yoga", "running", "ski", "voile", "équitation", "natation", "triathlon", "marathon", "pilates", "danse", "escalade", "kitesurf", "polo"]

# Villes
CITIES_FR = ["Paris", "Lyon", "Bordeaux", "Nice", "Marseille", "Cannes", "Monaco", "Saint-Tropez"]
CITIES_INT = ["London", "New York", "Milan", "Madrid", "Berlin", "Tokyo", "Hong Kong", "Dubai", "Singapore", "Los Angeles", "Shanghai", "Mumbai", "Sydney", "São Paulo", "Moscow"]

# Couleurs préférées
COLORS = ["noir", "cognac", "bordeaux", "navy", "beige", "gris", "blanc", "rose gold", "marron", "kaki", "bleu marine", "rouge", "vert émeraude", "or"]

# Régimes alimentaires
DIETS = ["végétarien", "végane", "pescetarien", "omnivore", "vegan", "vegetarian", "halal", "casher", "sans gluten", "sans lactose"]

# Allergies
ALLERGIES = ["nickel", "latex", "fruits coque", "arachides", "mariscos", "shellfish", "noix", "peanut", "parfums forts", "produits chimiques", "gluten", "lactose"]

# Templates de transcriptions par langue avec différentes complexités
TEMPLATES_FR = [
    # Court
    "Client {nom}, {age} ans, {profession}. Achat rapide {produit}. Budget {budget}€. Cuir {couleur}. {diet}. Satisfait.",
    
    # Moyen
    "Rdv {titre} {nom}, {profession} {age} ans, client {statut}. Cherche {produit} {occasion}. Budget {budget}€ flexible. Préfère cuir {couleur}. Pratique {sport}. {diet} pour événements. {allergie}. Rappeler {mois}.",
    
    # Long  
    "{titre} {nom} et {relation}, {age}-{age2} ans, clients {statut} depuis {annee}. Cherchent {produit} et {produit2} pour {occasion}. Budget combiné {budget}€ très flexible. {profession} lui, {profession2} elle. Passionnés {sport} et {sport2}, voyagent {destination} régulièrement. Collectionnent {collection}. Style {style}, préfère cuir {couleur} {couleur2}. {diet} pour événements boutique. {allergie}. Mentionné {enfant} étudiant {etude}, opportunité cadeau. Anniversaire mariage {mois}. Réseau professionnel étendu, référé clients. Rappeler {mois2} preview collection. Intéressés personnalisation pièces. Excellent potentiel lifetime value.",
    
    # Très long (stress test)
    "{titre} {nom} et famille complète shopping événement exceptionnel. Grand-père {age_gp} ans, parents {age}-{age2} ans, enfants {age_e} et {age_e2} ans. Budget familial combiné exceptionnel {budget}€+. Grand-père collectionneur {collection}, style classique traditionnel. Père {profession} dirige entreprise familiale génération. Mère {profession2} créativité famille. Enfants étudient {etude} et {etude2}. Célèbrent anniversaire {anniversaire} ans entreprise. Grand-père préfère {couleur} traditionnel. Parents modernes sophistiqués, mère avant-garde {couleur2}, père classique {couleur3}. Enfants style jeune trendy. Grand-père {diet}, parents {diet2}, enfants {diet3}. Mère {allergie} important hardware. Famille tradition shopping luxe ensemble, potentiel multi-génératif straordinaire. Réseau industry vast, clients potentiels infiniti. Événement coïncide exhibition, possible collaboration. Intéressés collection capsule collaboration famille. Client priorité maximum lifetime value straordinario. Célèbrent également anniversaire parents, compleanno grand-mère, laurea enfants. Voyage planifié {destination} été, {destination2} hiver. Collectionnent également {collection2}. Pratiquent {sport} été, {sport2} hiver. Mentionné projet expansion international, nouvelles opportunités. Contact préféré {canal}. Rappeler {mois} coordonner. Fournir sélection personnalisée. Inviter événements VIP exclusifs. Top priorité relation.",
]

TEMPLATES_EN = [
    "Mr. {nom}, {age}, {profession}. Quick purchase {produit}. Budget ${budget}. Leather {couleur}. {diet}. Happy.",
    
    "Meeting with {titre} {nom}, {profession} {age}. Looking for {produit} {occasion}. Budget around ${budget}. Prefers {couleur} leather. Practices {sport}. {diet} for events. {allergie}. Follow up {mois}.",
    
    "{titre} {nom} and {relation}, {age}-{age2}, excellent clients since {annee}. Shopping for {produit} and {produit2} for {occasion}. Combined budget ${budget} very flexible. He's {profession}, she's {profession2}. Both passionate about {sport} and {sport2}, travel {destination} regularly. Collect {collection}. {style} style, prefers {couleur} {couleur2} leather. {diet} for boutique events. {allergie}. Mentioned {enfant} studying {etude}, gift opportunity. Anniversary {mois}. Extensive professional network, referred many clients. Follow up {mois2} for preview. Interested in customization. Excellent lifetime value potential.",
]

TEMPLATES_IT = [
    "Signor {nom}, {age} anni, {profession}. Acquisto rapido {produit}. Budget {budget}€. Cuoio {couleur}. {diet}. Soddisfatto.",
    
    "Appuntamento {titre} {nom}, {profession} {age} anni. Cerca {produit} {occasion}. Budget {budget}€ flessibile. Preferisce cuoio {couleur}. Pratica {sport}. {diet} per eventi. {allergie}. Richiamare {mois}.",
]

TEMPLATES_ES = [
    "Sr. {nom}, {age} años, {profession}. Compra rápida {produit}. Presupuesto {budget}€. Cuero {couleur}. {diet}. Satisfecho.",
    
    "Cita {titre} {nom}, {profession} {age} años. Busca {produit} {occasion}. Presupuesto {budget}€ flexible. Prefiere cuero {couleur}. Practica {sport}. {diet} para eventos. {allergie}. Llamar {mois}.",
]

TEMPLATES_DE = [
    "Herr {nom}, {age} Jahre, {profession}. Schneller Kauf {produit}. Budget {budget}€. Leder {couleur}. {diet}. Zufrieden.",
    
    "Termin {titre} {nom}, {profession} {age} Jahre. Sucht {produit} {occasion}. Budget {budget}€ flexibel. Bevorzugt {couleur} Leder. Praktiziert {sport}. {diet} für Events. {allergie}. Nachfassen {mois}.",
]

# Edge cases spéciaux
EDGE_CASES = [
    # Caractères spéciaux et emoji
    "Client très satisfait! 😊 Budget: 5.000€ ✨ Cuir 100% authentique. Préfère les couleurs «classiques». Email: client@test.com. Tél: +33 6 12 34 56 78.",
    
    # Transcription quasi-vide
    "Appel court. OK.",
    
    # Aucune info extraire
    "Conversation téléphonique sans objet précis. Client passe juste dire bonjour.",
    
    # Budget mal formaté
    "Budget discuté: entre cinq mille et dix mille euros, peut-être plus selon les pièces.",
    
    # Âge non mentionné
    "Rdv client important, profession architecte. Cherche sac voyage luxe. Budget élevé.",
    
    # Multiples langues mélangées
    "Meeting avec cliente. Elle dit: 'Je cherche un sac très chic, you know, something special'. Muy elegante. Budget around 8K.",
    
    # Données contradictoires
    "Client homme cherche sac femme pour lui-même. Budget 50€ mais veut le plus cher. Nouveau client mais fidèle depuis 2010.",
    
    # Texte très répétitif
    "Client client client. Sac sac sac. Budget budget budget. Noir noir noir. Rappeler rappeler rappeler.",
    
    # Caractères Unicode extrêmes
    "クライアント田中さん、東京から。予算: ¥500,000。革製品を探しています。高級ブランド希望。",
    
    # Arabe
    "عميل مهم من دبي. يبحث عن حقيبة فاخرة. ميزانية مرنة.",
    
    # Très long monologue
    "Le client a parlé pendant toute la durée du rendez-vous sans vraiment préciser ce qu'il cherchait. Il a mentionné son enfance, ses voyages en Italie, sa passion pour les voitures anciennes, son chien qui s'appelle Max, le mariage de sa fille qui approche, les problèmes avec son entreprise, la météo qui n'est pas terrible en ce moment, le nouveau restaurant qui a ouvert près de chez lui, son opinion sur la politique actuelle, ses vacances prévues aux Maldives l'année prochaine, et finalement peut-être qu'il reviendra pour acheter quelque chose un jour. Budget non discuté. Aucun produit spécifique mentionné.",
    
    # SQL Injection test
    "Client nom: Robert'); DROP TABLE profiles;--. Budget: 5000€.",
    
    # HTML/Script injection
    "Client <script>alert('test')</script>. Budget: <b>5000€</b>.",
]

def generate_name():
    """Génère un nom aléatoire"""
    prenoms = ["Laurent", "Dubois", "Martin", "Bernard", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Michel", "Lefebvre", "Garcia", "Martinez", "Lopez", "Rossi", "Ferrari", "Bianchi", "Schmidt", "Weber", "Müller", "Kim", "Chen", "Wang", "Tanaka", "Al-Hassan", "Khan", "Patel"]
    return random.choice(prenoms)

def generate_budget():
    """Génère un budget aléatoire"""
    budgets = [
        "500", "1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000",
        "6000", "7000", "8000", "9000", "10000", "12000", "15000", "18000", "20000",
        "25000", "30000", "35000", "40000", "50000", "75000", "100000",
        "0", "-500",  # Edge cases
        "cinq mille", "dix mille",  # Format texte
    ]
    return random.choice(budgets)

def generate_age():
    """Génère un âge aléatoire"""
    return random.choice([str(random.randint(18, 85)), "", "vingt-cinq", "quarante"])

def generate_transcription(lang):
    """Génère une transcription selon la langue"""
    templates = {
        "FR": TEMPLATES_FR,
        "EN": TEMPLATES_EN,
        "IT": TEMPLATES_IT,
        "ES": TEMPLATES_ES,
        "DE": TEMPLATES_DE,
    }
    
    template_list = templates.get(lang, TEMPLATES_FR)
    template = random.choice(template_list)
    
    data = {
        "nom": generate_name(),
        "titre": random.choice(["M.", "Mme", "Mr.", "Mrs.", "Dr.", "Sir", "Signor", "Signora", "Sr.", "Sra.", "Herr", "Frau"]),
        "age": random.randint(25, 75),
        "age2": random.randint(25, 75),
        "age_gp": random.randint(70, 90),
        "age_e": random.randint(18, 30),
        "age_e2": random.randint(15, 28),
        "profession": random.choice(PROFESSIONS_FR if lang == "FR" else PROFESSIONS_EN),
        "profession2": random.choice(PROFESSIONS_FR if lang == "FR" else PROFESSIONS_EN),
        "produit": random.choice(["sac", "portefeuille", "ceinture", "mallette", "bagage", "accessoires", "maroquinerie", "bag", "wallet", "belt", "briefcase", "luggage"]),
        "produit2": random.choice(["sac", "portefeuille", "ceinture", "accessoires", "montre", "bijoux"]),
        "occasion": random.choice(["anniversaire", "mariage", "cadeau", "voyage", "travail", "birthday", "wedding", "gift", "travel", "work", "graduation", "retirement"]),
        "budget": generate_budget(),
        "statut": random.choice(["VIP", "fidèle", "régulier", "occasionnel", "nouveau", "excellent", "loyal"]),
        "couleur": random.choice(COLORS),
        "couleur2": random.choice(COLORS),
        "couleur3": random.choice(COLORS),
        "sport": random.choice(SPORTS),
        "sport2": random.choice(SPORTS),
        "diet": random.choice(DIETS),
        "diet2": random.choice(DIETS),
        "diet3": random.choice(DIETS),
        "allergie": f"Allergie {random.choice(ALLERGIES)}" if random.random() > 0.5 else "",
        "destination": random.choice(CITIES_INT),
        "destination2": random.choice(CITIES_INT),
        "collection": random.choice(["art contemporain", "montres vintage", "vins", "livres rares", "photographie", "sculptures", "NFT", "voitures anciennes"]),
        "collection2": random.choice(["art", "design", "antiquités"]),
        "style": random.choice(["classique", "moderne", "élégant", "avant-garde", "minimaliste", "sophistiqué"]),
        "mois": random.choice(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]),
        "mois2": random.choice(["janvier", "février", "mars", "avril", "mai", "juin"]),
        "annee": random.randint(2010, 2024),
        "relation": random.choice(["épouse", "mari", "fille", "fils", "mère", "wife", "husband", "daughter", "son"]),
        "enfant": random.choice(["fils", "fille", "petite-fille", "son", "daughter"]),
        "etude": random.choice(["médecine", "droit", "architecture", "design", "économie", "medicine", "law", "engineering"]),
        "etude2": random.choice(["art", "music", "business"]),
        "anniversaire": random.choice([10, 20, 25, 30, 40, 50]),
        "canal": random.choice(["email", "téléphone", "WhatsApp"]),
    }
    
    try:
        return template.format(**data)
    except KeyError:
        return template  # Retourne le template brut si erreur

def generate_date():
    """Génère une date aléatoire"""
    base = datetime(2026, 1, 1)
    offset = random.randint(0, 180)
    d = base + timedelta(days=offset)
    
    # Edge cases: dates mal formatées
    if random.random() < 0.02:
        return random.choice(["", "invalid", "01-13-2026", "2026/01/15", "15 janvier 2026"])
    
    return d.strftime("%Y-%m-%d")

def generate_csv():
    """Génère le fichier CSV de test"""
    filename = "LVMH_Test_500.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Duration", "Language", "Length", "Transcription"])
        
        for i in range(1, NUM_CLIENTS + 1):
            client_id = f"TEST_{i:04d}"
            date = generate_date()
            duration = random.choice(DURATIONS)
            lang = random.choice(LANGUAGES)
            length = random.choice(LENGTHS)
            
            # 5% de chance d'avoir un edge case
            if random.random() < 0.05:
                transcription = random.choice(EDGE_CASES)
            else:
                transcription = generate_transcription(lang)
            
            # Edge cases supplémentaires
            if random.random() < 0.01:
                transcription = ""  # Transcription vide
            if random.random() < 0.01:
                duration = ""  # Durée vide
            
            writer.writerow([client_id, date, duration, lang, length, transcription])
    
    print(f"✅ Fichier généré: {filename}")
    print(f"   - {NUM_CLIENTS} clients simulés")
    print(f"   - Langues: {', '.join(LANGUAGES)}")
    print(f"   - Inclut edge cases et stress tests")

if __name__ == "__main__":
    generate_csv()
