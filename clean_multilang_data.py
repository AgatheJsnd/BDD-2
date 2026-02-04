import pandas as pd
import re

def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # 1. Anonymisation RGPD (PII) - Ordre spécifique pour éviter les collisions
    
    # IBAN (très spécifique)
    text = re.sub(r'\b[A-Z]{2}\d{2}[A-Z0-9\s]{11,31}\b', '[IBAN]', text)
    
    # Cartes bancaires (13 à 16 chiffres)
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[CARTE_BANCAIRE]', text)
    
    # Emails
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]', text)
    
    # Téléphones (plus restrictif pour éviter de capturer les codes postaux ou dates)
    # Cherche des séquences de 8 chiffres ou plus avec des séparateurs
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}?\)?([-.\s]?\d{2,4}){2,4}', '[TELEPHONE]', text)
    
    # Identifiants nationaux
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text) # SSN US
    text = re.sub(r'\b\d{8}[A-Z]\b', '[DNI]', text) # DNI ES
    text = re.sub(r'\b[A-Z]{2}\s?\d{7}\b', '[PASSEPORT]', text) # Passeport
    text = re.sub(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', '[CODICE_FISCALE]', text) # CF IT

    # Adresses et codes
    text = re.sub(r'code\s+porte\s+\d+', 'code porte [CODE]', text, flags=re.IGNORECASE)
    text = re.sub(r'gate\s+code\s+\d+', 'gate code [CODE]', text, flags=re.IGNORECASE)
    
    # 2. Nettoyage linguistique (Tics de langage)
    # Français
    text = re.sub(r'\b(euh|enfin|tu vois|genre|du coup|enfin bref|voilà quoi|en fait|un peu|vous savez)\b', '', text, flags=re.IGNORECASE)
    # Anglais
    text = re.sub(r'\b(like|you know|sort of|ehm)\b', '', text, flags=re.IGNORECASE)
    # Espagnol
    text = re.sub(r'\b(o sea|en plan|sin querer)\b', '', text, flags=re.IGNORECASE)
    # Italien
    text = re.sub(r'\b(cioè|ehm)\b', '', text, flags=re.IGNORECASE)

    # Nettoyage final
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'["“”]', '', text)
    
    return text

def main():
    input_file = "LVMH_sample_multilang_FULL.csv"
    output_file = "LVMH_sample_multilang_FULL_cleaned.csv"
    
    print(f"Nettoyage de {input_file} (V2)...")
    df = pd.read_csv(input_file)
    
    if 'Transcription' in df.columns:
        df['Transcription_Cleaned'] = df['Transcription'].apply(clean_text)
        print("Colonne 'Transcription_Cleaned' mise à jour.")
    else:
        print("Erreur : Colonne 'Transcription' non trouvée.")
        return

    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Fichier nettoyé sauvegardé sous : {output_file}")

if __name__ == "__main__":
    main()
