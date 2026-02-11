import csv
import random
import datetime

# Configuration
OUTPUT_FILE = "simulation_new.csv"
NUM_ROWS = 50 # Générer 50 clients pour le test

# Données de base pour la simulation
CITIES = ["Paris", "London", "New York", "Tokyo", "Milan", "Dubai", "Shanghai"]
NAMES = ["Dubois", "Smith", "Rossi", "Wang", "Müller", "Martin", "Garcia", "Silva", "Tanaka", "Ivanov"]
FIRST_NAMES = ["Jean", "Marie", "John", "Sarah", "Alessandro", "Giulia", "Wei", "Li", "Hans", "Anna"]
PRODUCTS = ["sac Capucines", "montre Tambour", "parfum Sauvage", "robe de soirée", "costume sur mesure", "sneakers Run Away"]
COLORS = ["rouge", "noir", "bleu", "or", "argent", "rose poudré", "beige"]
BUDGETS = ["1000", "5000", "10000", "unlimited", "flexible", "20000", "50000"]
HTML_TAGS = ["<script>alert('XSS')</script>", "<b>Bold</b>", "<i>Italic</i>", "<div>Div</div>"]
ENCODING_ERRORS = ["Ã©", "Ã¨", "Ãª", "â‚¬", "Ã"]

def generate_dirty_transcription(client_id):
    """Génère une transcription réaliste mais potentiellement 'sale'"""
    
    # Choix aléatoire du type de 'saleté' (20% de chance d'avoir un problème)
    is_dirty = random.random() < 0.2
    
    first_name = random.choice(FIRST_NAMES)
    name = random.choice(NAMES)
    city = random.choice(CITIES)
    product = random.choice(PRODUCTS)
    budget = random.choice(BUDGETS)
    color = random.choice(COLORS)
    
    # Base template
    templates = [
        f"Client {first_name} {name} rencontré à {city}. Cherche {product}. Budget environ {budget}.",
        f"Conversation avec {name}, client VIP. Intéressé par {product} en {color}.",
        f"Note: {first_name} cherche un cadeau. Budget {budget}. Aime le {color}.",
        f"Rdv boutique {city} avec {first_name}. Projet achat: {product}.",
    ]
    
    transcription = random.choice(templates)
    
    if is_dirty:
        dirty_type = random.choice(["html", "encoding", "empty", "short"])
        
        if dirty_type == "html":
            tag = random.choice(HTML_TAGS)
            transcription = f"{transcription} {tag}"
        elif dirty_type == "encoding":
            transcription = transcription.replace("é", random.choice(ENCODING_ERRORS)).replace("è", random.choice(ENCODING_ERRORS))
        elif dirty_type == "empty":
            transcription = ""
        elif dirty_type == "short":
            transcription = "Oui."

    return transcription

def generate_csv(filename, num_rows):
    print(f"Génération de {num_rows} lignes dans {filename}...")
    
    header = ["ID", "Date", "Duration", "Language", "Length", "Transcription"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for i in range(1, num_rows + 1):
            client_id = f"SIM_{i:03d}"
            date = datetime.date.today().isoformat()
            duration = f"{random.randint(5, 60)}min"
            language = random.choice(["FR", "EN", "IT", "FR", "EN"]) # Poids plus fort sur FR/EN
            length = random.choice(["short", "medium", "long"])
            transcription = generate_dirty_transcription(client_id)
            
            writer.writerow([client_id, date, duration, language, length, transcription])
            
    print("Terminé !")

if __name__ == "__main__":
    generate_csv(OUTPUT_FILE, NUM_ROWS)
