import pandas as pd
import re
import os

# Configuration
INPUT_FILE = 'LVMH_Notes_CA101-400.csv'
OUTPUT_FILE = 'transcriptions_clean.csv'
COLUMN_NAME = 'Transcription'

# Liste étendue des marqueurs d'hésitation et tocs de langage (Multilingue)
HESITATION_MARKERS = [
    # Français
    "euh", "ehh", "ahh", "hum", "mmh", "bah", "bon", "ben", "enfin", "en gros", 
    "on va dire", "tu sais", "vous savez", "quoi", "bref", "en quelque sorte", 
    "pour ainsi dire", "voilà", "machin", "truc", "genre", "disons que", 
    "un petit peu", "un tantinet", "si vous voulez", "c'est-à-dire",
    
    # English
    "uh", "um", "er", "ah", "like", "you know", "i mean", "sort of", "kind of", 
    "basically", "actually", "well", "right", "pretty much", "as it were",
    
    # Español
    "em", "este", "bueno", "o sea", "pues", "digamos", "en plan", "ya sabes",
    "vamos a ver", "por así decirlo", "más o menos", "un poquito",
    
    # Italiano
    "tipo", "diciamo", "ehm", "beh", "allora", "insomma", "cioè", "praticamente",
    "in un certo senso", "per così dire", "pressappoco",
    
    # Deutsch
    "äh", "ähmm", "halt", "quasi", "sozusagen", "gewissermaßen", "weißt du",
    "genau", "eigentlich", "vielleicht", "etwa", "ungefähr"
]

def clean_text(text):
    """
    Nettoie une transcription de texte en supprimant les hésitations,
    la ponctuation excessive et en normalisant le format.
    """
    if not isinstance(text, str):
        return str(text) if text is not None else ""

    # 1. Normalisation : conversion en minuscules
    text = text.lower()

    # 2. Suppression des marqueurs d'hésitation
    # On utilise \b pour s'assurer qu'on supprime le mot entier et pas une partie d'un autre mot
    # On trie par longueur décroissante pour éviter que "ah" ne matche dans "ahh" avant suppression
    sorted_markers = sorted(HESITATION_MARKERS, key=len, reverse=True)
    pattern = r'\b(?:' + '|'.join(map(re.escape, sorted_markers)) + r')\b'
    text = re.sub(pattern, '', text)

    # 3. Nettoyage du bruit et ponctuation excessive
    # Remplacer la ponctuation répétée (ex: "!!" devient "!", "..." devient ".")
    text = re.sub(r'([!?,.])\1+', r'\1', text)
    
    # Supprimer les caractères spéciaux non alpha-numériques (sauf ponctuation basique et espaces)
    # Optionnel : dépend de si on veut garder la ponctuation ou non.
    # Ici, on garde les caractères de base et la ponctuation de phrase
    text = re.sub(r'[^a-z0-9àâçéèêëîïôùûüÿñæœ\s\.,?!]', ' ', text)

    # 4. Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def main():
    print("Démarrage du script de nettoyage...")

    # Vérification de l'existence du fichier
    if not os.path.exists(INPUT_FILE):
        print(f"ERREUR : Le fichier '{INPUT_FILE}' est introuvable.")
        print("Veuillez vérifier que le fichier est bien présent dans le dossier courant.")
        # Création d'un fichier exemple pour aider l'utilisateur
        try:
            sample_data = pd.DataFrame({
                COLUMN_NAME: [
                    "Bonjour ehh je voudrais... ahh savoir le prix.",
                    "Bah, je ne suis pas sûr hum...",
                    "C'est BON !!? Oui bon d'accord."
                ]
            })
            sample_data.to_csv('transcriptions_exemple.csv', index=False)
            print(f"Un fichier exemple 'transcriptions_exemple.csv' a été créé pour test.")
        except Exception as e:
            print(f"Impossible de créer le fichier exemple : {e}")
        return

    try:
        # Chargement des données
        print(f"Chargement du fichier {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE)

        # Vérification de la présence de la colonne cible
        if COLUMN_NAME not in df.columns:
            print(f"ERREUR : La colonne '{COLUMN_NAME}' n'existe pas dans le fichier.")
            print(f"Colonnes disponibles : {list(df.columns)}")
            return

        # Application du nettoyage
        print("Nettoyage des transcriptions en cours...")
        # On utilise .astype(str) pour éviter les erreurs si des nombres sont présents
        df['transcription_cleaned'] = df[COLUMN_NAME].astype(str).apply(clean_text)

        # Sauvegarde
        print(f"Sauvegarde dans {OUTPUT_FILE}...")
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("Traitement terminé avec succès !")
        
        # Affichage d'un aperçu
        print("\nAperçu des modifications (5 premières lignes) :")
        print(df[[COLUMN_NAME, 'transcription_cleaned']].head().to_string())

    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

if __name__ == "__main__":
    main()
