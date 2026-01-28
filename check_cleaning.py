import pandas as pd
import re

df = pd.read_csv('transcriptions_clean.csv')

# Test samples
test_indices = [2, 4] # CA_103 (ES), CA_105 (DE)

print("--- ANALYSE DU NETTOYAGE ---")

for idx in test_indices:
    lang = df.iloc[idx]['Language']
    clean = df.iloc[idx]['transcription_cleaned']
    
    print(f"\nIndex {idx} ({lang}):")
    # Check for some specific words that should have accents
    if lang == 'ES':
        words = ['próximo', 'televisión', 'exóticas']
    elif lang == 'DE':
        words = ['große', 'universität', 'häuser']
    else:
        words = []
        
    for word in words:
        found = word.lower() in clean.lower()
        print(f"  Word '{word}': {'OK' if found else 'MISSING'}")
    
    # Check for some hesitation markers that should be REMOVED
    markers = ['vale', 'verdad', 'bueno', 'mira', 'na ja', 'tja']
    for marker in markers:
        # We check with word boundaries to be sure
        if re.search(r'\b' + re.escape(marker) + r'\b', clean.lower()):
            print(f"  Marker '{marker}': STILL PRESENT (FAIL)")

print("\n--- FIN ---")
