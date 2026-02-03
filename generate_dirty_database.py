"""
Générateur de Base de Données SALE pour Stress Test
Crée un CSV de 150 clients avec des données volontairement problématiques
pour tester la robustesse du script de nettoyage Python.
"""
import csv
import random
from datetime import datetime, timedelta

NUM_CLIENTS = 150

# ==== FORMATS D'ÂGE INTENTIONNELLEMENT VARIÉS ET PROBLÉMATIQUES ====
AGE_FORMATS = [
    "{age} ans",                    # Format correct
    "{age}ans",                     # Sans espace
    "{age} an",                     # Singulier incorrect
    "agé de {age}",                 # Texte français
    "âgé de {age} ans",             # Avec accent
    "{age} years old",              # Anglais
    "{age}-year-old",               # Anglais trait d'union
    "age: {age}",                   # Format label
    "né en {birth_year}",           # Année naissance (calcul requis)
    "born {birth_year}",            # Anglais année
    "la trentaine",                 # Vague
    "quarantaine",                  # Vague
    "cinquantaine",                 # Vague
    "soixantaine",                  # Vague
    "mid-thirties",                 # Anglais vague
    "early forties",                # Anglais vague
    "late twenties",                # Anglais vague
    "{age} Jahre alt",              # Allemand
    "{age} anni",                   # Italien
    "{age} años",                   # Espagnol
    "environ {age}",                # Approximatif
    "around {age}",                 # Anglais approximatif
    "~{age}",                       # Tilde
    "{age}+",                       # Plus
    "trente-cinq",                  # Lettres françaises
    "quarante-deux",                # Lettres françaises
    "fifty-two",                    # Anglais lettres
    "twenty eight",                 # Anglais sans trait
    "",                             # VIDE
    "CONFIDENTIEL",                 # Refus
    "ne souhaite pas dire",         # Refus
]

# ==== FORMATS DE BUDGET INTENTIONNELLEMENT VARIÉS ====
BUDGET_FORMATS = [
    "{budget}€",                    # Standard
    "{budget} €",                   # Avec espace
    "{budget} euros",               # Texte
    "{budget}EUR",                  # Code
    "${budget}",                    # Dollar
    "{budget}$",                    # Dollar après
    "{budget_k}k",                  # Abréviation k
    "{budget_k}K€",                 # K majuscule
    "{budget_k}k euros",            # K + texte
    "{budget_k}000",                # Zéros manquants
    "environ {budget}€",            # Approximatif
    "around ${budget}",             # Anglais approx
    "budget flexible",              # Vague
    "budget illimité",              # Vague
    "unlimited budget",             # Anglais vague
    "pas de limite",                # Vague
    "{budget}.000€",                # Séparateur point
    "{budget},000€",                # Séparateur virgule
    "{budget} – {budget2} €",       # Fourchette tiret
    "entre {budget} et {budget2}",  # Fourchette texte
    "from {budget} to {budget2}",   # Anglais fourchette
    "{budget}€-{budget2}€",         # Fourchette compact
    "presupuesto {budget}€",        # Espagnol
    "budget di {budget}€",          # Italien
    "Budget: {budget}€",            # Label
    "£{budget}",                    # Livres
    "¥{budget}000",                 # Yen
    "",                             # VIDE
    "à discuter",                   # Vague
    "selon modèle",                 # Conditionnel
    "5.000,00€",                    # Format européen
    "5,000.00$",                    # Format US
]

# ==== NOMS AVEC CARACTÈRES SPÉCIAUX ====
NOMS_SPECIAUX = [
    "M. Müller-Löwenstein",
    "Mme Ñoño García",
    "Sr. José María Pérez-López",
    "Signora D'Angelo",
    "Mr. O'Brien-McIntyre",
    "Mlle Çelik",
    "Frau Köhler",
    "Mme Thérèse André",
    "M. François-Xavier",
    "Mrs. Björk Jónsdóttir",
    "Sr. João Gonçalves",
    "Mme Zoë Bäcker",
    "M. 李明 (Li Ming)",
    "Mrs. Αλεξάνδρα Παπαδόπουλος",
    "السيد أحمد",
    "Dr. Émile François-Marie",
    "Prof. Øystein Ødegård",
    "Mme Śląska Bądź",
    "M. DUPONT Jean-Pierre",
    "mme durand marie",  # tout minuscule
    "MME LEGRAND",       # tout majuscule
    "m dubois",          # sans point
    "Durand",            # sans civilité
    "",                  # VIDE
]

# ==== VILLES AVEC ERREURS ====
VILLES_PROBLEMATIQUES = [
    "paris", "PARIS", "Paris", "Parsi", "Pars",  # Casse et typos
    "Londre", "london", "LONDON", "Londres",
    "Mailn", "Milan", "milano", "MILAN",
    "newyork", "New-York", "new york", "NYC", "NY",
    "鳥京", "Tokyo", "tokio", "TOKYO",
    "Dubai", "Dubaï", "dubai", "DUBAI",
    "Saint Tropez", "St-Tropez", "St Tropez", "Saint-Tropez",
    "Francfort", "Frankfurt", "francfort",
    "Zurich", "zürich", "ZURICH",
    "Côte d'Azur", "Cote d'Azur", "riviera",
    "Monaco", "monte carlo", "Monte-Carlo",
    "Hong Kong", "hong-kong", "HK", "Hongkong",
    "Singapoure", "Singapore", "singapour",
    "",
    "???",
    "N/A",
    "Inconnu",
]

# ==== PROFESSIONS PROBLÉMATIQUES ====
PROFESSIONS_MELANGEES = [
    "avocat/entrepreneur",
    "médecin-chirurgien",
    "banquier+investisseur",
    "artiste & designer",
    "CEO, CFO, COO",
    "retired banker formerly",
    "ancien directeur maintenant consultant",
    "ex-PDG startup",
    "étudiant travaille aussi",
    "multiple businesses",
    "influencer/entrepreneur/model",
    "profession libérale",
    "NC",
    "",
    "confidentiel",
    "préfère ne pas dire",
    "🎨 artiste",  # avec emoji
    "👔 businessman",
    "femme au foyer et bénévole",
    "retraité actif",
]

# ==== ALLERGIES PROBLÉMATIQUES ====
ALLERGIES_CHAOS = [
    "allergie arachides ET noix",
    "allergy nuts, latex, perfumes",
    "allergique nickel + latex",
    "ATTENTION: allergie sévère fruits coque!!!",
    "⚠️ allergies multiples",
    "pas d'allergie connue",
    "none",
    "aucune",
    "N/A",
    "???",
    "",
    "allergie soleil + produits chimiques",
    "severe shellfish allergy CRITICAL",
    "intolérances: gluten lactose",
    "allergies alimentaires diverses",
]

# ==== RÉGIMES ALIMENTAIRES CONFUS ====
REGIMES_CONFUS = [
    "végétarien mais mange du poisson",  # contradiction
    "vegan sauf occasionnellement",       # contradiction
    "végane strict",
    "vegetarian events",
    "pescetarien",
    "flexitarien",
    "omnivore",
    "suit régime Keto",
    "sans gluten sans lactose",
    "halal",
    "kosher",
    "pas de restrictions",
    "regime special",
    "",
    "???",
]

# ==== TEMPLATES DE TRANSCRIPTIONS SALES ====
DIRTY_TEMPLATES = [
    # 1. Mélange de langues
    """Client {nom}, {age_format}. Wants to buy un sac pour business trips. 
    Budget {budget_format}. Habite {ville} mais travels often to München et Milano.
    Sport: {sport}. {regime}. Cuir {couleur} preferred. {allergie}.""",
    
    # 2. Émojis et caractères spéciaux
    """🌟 CLIENTE VIP 🌟 {nom} 💼 {profession} ⭐⭐⭐⭐⭐
    Age: {age_format} | Budget: {budget_format} 💰💰💰
    🏠 {ville} | ✈️ travels a lot
    Loves: {sport} 🎾 | Art 🎨 | Music 🎵
    Diet: {regime} 🥗 | {allergie} ⚠️
    Color: {couleur} ❤️ | Wife birthday 🎂 coming up!
    Call back ASAP! 📞📞📞""",
    
    # 3. HTML et tentatives d'injection
    """Rendez-vous <script>alert('XSS')</script> avec {nom}.
    <b>Budget:</b> {budget_format} <i>flexible</i>
    <h1>IMPORTANT CLIENT</h1>
    Ville: {ville} <br> Age: {age_format}
    DROP TABLE clients; -- juste un test
    <img src="fake.jpg" onerror="alert('hack')">
    Couleur: {couleur}. {regime}. {allergie}.""",
    
    # 4. Texte quasi-vide
    """{nom}. {ville}. ok.""",
    
    # 5. Texte beaucoup trop long avec répétitions
    """CONVERSATION EXCEPTIONNELLE avec {nom}, {profession} extraordinaire, 
    vraiment un client exceptionnel et extraordinaire qui mérite une attention 
    exceptionnelle et extraordinaire. {age_format} donc dans la tranche d'âge 
    des clients exceptionnels et extraordinaires. Budget {budget_format} mais 
    pourrait être plus élevé car client exceptionnel et extraordinaire. 
    Réside à {ville} une ville exceptionnelle où vivent des gens exceptionnels.
    Pratique {sport} de manière exceptionnelle. {regime} de façon exceptionnelle.
    {allergie}. Couleur préférée {couleur} une couleur exceptionnelle.
    Client à rappeler car exceptionnel et extraordinaire pour proposition 
    exceptionnelle collection exceptionnelle prochaine saison exceptionnelle.
    Potentiel lifetime value exceptionnel et extraordinaire vraiment incroyable.
    """ + "Exceptionnel extraordinaire. " * 50,  # répétition spam
    
    # 6. Données manquantes ou nulles
    """Client . Age: . Budget: . Ville: .
    Sport: ???. Régime: N/A. Allergie: null.
    Couleur: undefined. Profession: NaN.
    TODO: compléter fiche plus tard""",
    
    # 7. Format tableau cassé
    """|Client|{nom}|
    |Age|{age_format}|
    |Budget|{budget_format}|
    |Ville|{ville}|
    |Corrupted|data|table|error|format|""",
    
    # 8. Contradictions multiples
    """M. {nom}, nouveau client mais client fidèle depuis 2015.
    {age_format} dynamique et retraité depuis 20 ans.
    Budget {budget_format} limité mais très généreux illimité.
    {regime} strict mais mange de tout occasionnellement.
    Habite {ville} mais n'a jamais visité cette ville.
    Aime {couleur} mais déteste absolument cette couleur.
    {allergie} mais aucun problème avec ces allergènes.""",
    
    # 9. Encodage problématique simulé
    """Client {nom} rencontré boutique.
    Ã¢ge: {age_format} -- Caractères encodés: Ã©Ã¨Ãªà 
    Budget: {budget_format} â‚¬
    Ville: {ville} aÃ©roport
    RÃ©gime: {regime}
    Couleur: {couleur}
    Sport: {sport}""",
    
    # 10. Dates et timing chaotiques
    """RDV {nom} le 31/02/2026 à 25:99
    Client depuis 2099, {age_format}.
    Anniversaire: hier/demain/bientôt
    Budget {budget_format} à confirmer 30/13/2025
    Rappeler: la semaine prochaine ou le mois dernier
    {ville}. {regime}. {allergie}. {couleur}.""",
    
    # 11. Format courriel/notes copié-collé
    """From: sales@boutique.com
    To: manager@boutique.com  
    Subject: RE: FW: RE: Client {nom}
    
    -----Original Message-----
    Hi,
    Pls see below client info:
    - {age_format}
    - {budget_format}  
    - {ville}
    - {couleur} leather pref
    
    Rgds,
    
    >>> Previous message truncated...
    
    Sent from my iPhone
    --
    This email is confidential blah blah disclaimer...""",
    
    # 12. Arabe/Caractères non-latins mélangés
    """عميل مهم {nom} من {ville}.
    العمر: {age_format}. الميزانية: {budget_format}.
    يبحث عن حقيبة فاخرة {couleur}.
    {regime}. {allergie}. 
    Sport: {sport}. رياضي جدا.
    Rappeler en français merci.""",
    
    # 13. Données dupliquées partielles  
    """Client {nom} {nom} (doublon??)
    Age {age_format} ou {age_format} ans
    Budget {budget_format} / {budget_format} euros
    Ville {ville} / {ville}
    ATTENTION: POSSIBLE DUPLICATE: POSSIBLE DUPLICATE:
    {regime}. {allergie}. {couleur}. {sport}.""",
    
    # 14. Transcription voice-to-text ratée
    """Euh alors le client c'est {nom} voilà euh 
    donc il a genre euh {age_format} enfin bon bref
    et donc son budget c'est euh environ euh genre {budget_format}
    il habite à ah mince comment ça s'appelle euh {ville}
    donc voilà quoi euh {regime} et puis euh {allergie}
    ah oui et il aime le {couleur} voilà c'est tout euh merci""",
    
    # 15. Format JSON cassé dans le texte
    """{{name: "{nom}", age: {age_format}, 
    budget: "{budget_format}", city: {ville}",
    diet: "{regime}, allergy: "{allergie}",
    color: {couleur}, sport": "{sport}"
    ERROR: JSON PARSE FAILED LINE 3}}""",
]

# ==== DONNÉES SUPPLÉMENTAIRES ====
SPORTS = ["golf", "Tennis", "YOGA", "running", "ski", "voile", "équitation", "natation", 
          "football", "polo", "kitesurf", "triathlon", "marathon", "pilates", "???", "", "N/A"]
COULEURS = ["noir", "BLACK", "Noir", "cognac", "Cognac", "bordeaux", "BORDEAUX", "beige",
            "rose gold", "rose-gold", "rosé gold", "navy", "blanc", "multicolore", "???", ""]

DATES_PROBLEMATIQUES = [
    "2026-01-15", "15/01/2026", "01-15-2026", "January 15, 2026",
    "15 janvier 2026", "2026.01.15", "15.01.26", "1/15/26",
    "", "N/A", "???", "invalid", "31/02/2026", "00/00/0000"
]

DUREES_PROBLEMATIQUES = [
    "30 min", "30min", "30 minutes", "30m", "0.5h", "half hour",
    "une demi-heure", "environ 30", "~30min", "30-45 min",
    "", "N/A", "???", "long", "court", "très long"
]

LANGUES_PROBLEMATIQUES = [
    "FR", "fr", "Fr", "Français", "French", "francais",
    "EN", "en", "English", "Anglais", "anglais",
    "IT", "Italian", "Italien", "italiano",
    "ES", "Spanish", "Espagnol", "español",
    "DE", "German", "Allemand", "deutsch",
    "MIX", "multilingual", "FR/EN", "plusieurs",
    "", "???", "N/A", "autre"
]


def generate_dirty_age():
    """Génère un âge dans un format aléatoire problématique"""
    age = random.randint(22, 75)
    birth_year = 2026 - age
    format_template = random.choice(AGE_FORMATS)
    return format_template.format(age=age, birth_year=birth_year)


def generate_dirty_budget():
    """Génère un budget dans un format aléatoire problématique"""
    budget = random.choice([3000, 5000, 7000, 10000, 12000, 15000, 20000, 25000, 30000])
    budget_k = budget // 1000
    budget2 = budget + random.randint(2000, 5000)
    format_template = random.choice(BUDGET_FORMATS)
    return format_template.format(
        budget=budget, 
        budget_k=budget_k, 
        budget2=budget2
    )


def generate_dirty_transcription(index):
    """Génère une transcription volontairement problématique"""
    template = random.choice(DIRTY_TEMPLATES)
    
    nom = random.choice(NOMS_SPECIAUX)
    if not nom:
        nom = f"Client_{index}"
    
    return template.format(
        nom=nom,
        age_format=generate_dirty_age(),
        budget_format=generate_dirty_budget(),
        ville=random.choice(VILLES_PROBLEMATIQUES),
        profession=random.choice(PROFESSIONS_MELANGEES),
        allergie=random.choice(ALLERGIES_CHAOS),
        regime=random.choice(REGIMES_CONFUS),
        sport=random.choice(SPORTS),
        couleur=random.choice(COULEURS),
    )


def generate_dirty_csv():
    """Génère le fichier CSV sale"""
    filename = "LVMH_Dirty_Database.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Duration", "Language", "Length", "Transcription"])
        
        for i in range(1, NUM_CLIENTS + 1):
            client_id = f"DIRTY_{i:03d}"
            date = random.choice(DATES_PROBLEMATIQUES)
            duration = random.choice(DUREES_PROBLEMATIQUES)
            language = random.choice(LANGUES_PROBLEMATIQUES)
            
            # Length avec erreurs
            length = random.choice(["short", "medium", "long", "SHORT", "LONG", 
                                   "court", "moyen", "longe", "", "???", "N/A"])
            
            transcription = generate_dirty_transcription(i)
            
            # Parfois corrompre les données encore plus
            if random.random() < 0.1:
                # Ligne avec colonnes décalées
                writer.writerow([client_id, transcription, date, duration, language, length])
            elif random.random() < 0.1:
                # Ligne avec colonnes manquantes
                writer.writerow([client_id, date, transcription])
            else:
                writer.writerow([client_id, date, duration, language, length, transcription])
    
    print(f"✅ Fichier généré: {filename}")
    print(f"📊 Nombre de clients: {NUM_CLIENTS}")
    print("⚠️ Cette base contient intentionnellement:")
    print("   - Formats d'âge incohérents")
    print("   - Budgets mal formatés")
    print("   - Caractères spéciaux et émojis")
    print("   - HTML et tentatives d'injection")
    print("   - Langues mélangées")
    print("   - Données manquantes ou nulles")
    print("   - Contradictions")
    print("   - Encodage problématique")
    print("   - Doublons et erreurs de format")


if __name__ == "__main__":
    generate_dirty_csv()
