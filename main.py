import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('LVMH_Realistic_Merged_CA001-100.csv')

# Afficher les premières lignes
print("=== Aperçu des données ===")
print(df.head())

print("\n=== Informations sur le dataset ===")
print(df.info())
