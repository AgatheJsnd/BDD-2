import pandas as pd
import re

def clean_text_rgpd_strict(text):
    if not isinstance(text, str):
        return text
    
    # 1. Moyens de Paiement (Remplacer les détails par le type uniquement)
    # IBAN (doit être fait avant les chiffres simples)
    text = re.sub(r'\b[A-Z]{2}\d{2}[A-Z0-9\s]{11,31}\b', '[PAIEMENT_VIREMENT]', text)
    # Cartes bancaires (13 à 16 chiffres)
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[PAIEMENT_CARTE]', text)
    
    # Supprimer les détails techniques de paiement (exp, CVC, CVV)
    text = re.sub(r'\b(exp|cad)\s+\d{2}/\d{2}\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(CVC|CVV)\s+\d{3}\b', '', text, flags=re.IGNORECASE)
    
    # 2. Adresses (Généralisation stricte au pays/région)
    # France
    text = re.sub(r'\d+\s+rue\s+[\w\s]+,\s+\d{5}\s+Paris', 'situé en France (Paris)', text, flags=re.IGNORECASE)
    # UK
    text = re.sub(r'\d+[A-Z]?\s+Baker\s+Street,\s+London\s+[\w\d\s]+', 'situé au Royaume-Uni (Londres)', text, flags=re.IGNORECASE)
    # Espagne
    text = re.sub(r'Calle\s+[\w\s]+\d+,\s+\d{5}\s+Madrid', 'situé en Espagne (Madrid)', text, flags=re.IGNORECASE)
    # Italie
    text = re.sub(r'Via\s+[\w\s]+\d+,\s+\d{5}\s+Roma', 'situé en Italie (Rome)', text, flags=re.IGNORECASE)
    
    # 3. Suppression des autres PII (Emails, Téléphones, Codes)
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL_MASQUÉ]', text)
    # Téléphones (regex plus précise pour éviter de manger les dates ou budgets)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}?\)?([-.\s]?\d{2,4}){3,4}', '[TÉLÉPHONE_MASQUÉ]', text)
    
    # Codes d'accès et détails d'étage/porte
    text = re.sub(r'(code porte|gate code|código|codice)\s+\d+', '[ACCÈS_SÉCURISÉ]', text, flags=re.IGNORECASE)
    text = re.sub(r'(piso|interno|appartement)\s+[\w\d]+', '[DÉTAILS_LOGEMENT_MASQUÉS]', text, flags=re.IGNORECASE)
    
    # Identifiants nationaux
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[ID_NATIONAL_MASQUÉ]', text)
    text = re.sub(r'\b\d{8}[A-Z]\b', '[ID_NATIONAL_MASQUÉ]', text)
    text = re.sub(r'\b[A-Z]{2}\s?\d{7,9}\b', '[PASSEPORT_MASQUÉ]', text)
    text = re.sub(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', '[ID_FISCAL_MASQUÉ]', text)

    # 4. Nettoyage linguistique (Tics de langage)
    text = re.sub(r'\b(euh|enfin|tu vois|genre|du coup|enfin bref|voilà quoi|en fait|un peu|vous savez|like|you know|sort of|ehm|o sea|en plan|sin querer|cioè)\b', '', text, flags=re.IGNORECASE)

    # Nettoyage final des espaces et guillemets
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'["“”]', '', text)
    # Nettoyer les virgules ou points orphelins dus aux suppressions
    text = re.sub(r'\s+,\s+', ', ', text)
    text = re.sub(r'\s+\.\s+', '. ', text)
    
    return text

def main():
    input_file = "LVMH_sample_multilang_FULL.csv"
    output_file = "LVMH_sample_multilang_FULL_cleaned.csv"
    
    print(f"Nettoyage RGPD STRICT V2 de {input_file}...")
    df = pd.read_csv(input_file)
    
    if 'Transcription' in df.columns:
        df['Transcription_Cleaned'] = df['Transcription'].apply(clean_text_rgpd_strict)
        print("Anonymisation et généralisation terminées.")
    else:
        print("Erreur : Colonne 'Transcription' non trouvée.")
        return

    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Fichier nettoyé sauvegardé sous : {output_file}")

if __name__ == "__main__":
    main()
