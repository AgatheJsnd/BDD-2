"""
Script de nettoyage de transcriptions de vente avec Mistral AI
Auteur: Expert Senior Python & NLP
Version: 1.0

Ce script nettoie des transcriptions brutes en supprimant les hésitations,
répétitions et mots parasites tout en préservant le sens et le ton original.
"""

import pandas as pd
import os
import time
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from tqdm import tqdm
from mistralai import Mistral
from dotenv import load_dotenv

# ============================================================================
# CONFIGURATION
# ============================================================================

# Chargement des variables d'environnement
load_dotenv()

# Configuration des fichiers
INPUT_FILE = 'LVMH_Notes_CA101-400.csv'  # Fichier source
OUTPUT_FILE = 'LVMH_Notes_CA101-400_cleaned.csv'  # Fichier de sortie
COLUMN_NAME = 'Transcription'  # Nom de la colonne à nettoyer

# Configuration Mistral AI
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_MODEL = 'mistral-small-latest'  # ou 'mistral-large-latest' pour plus de qualité

# Paramètres de traitement
BATCH_SIZE = 50  # Nombre de transcriptions à traiter en parallèle
MAX_RETRIES = 3  # Nombre de tentatives en cas d'échec
RETRY_DELAY = 2  # Délai entre les tentatives (secondes)

# ============================================================================
# PROMPT SYSTÈME
# ============================================================================

SYSTEM_PROMPT = """Tu es un éditeur professionnel spécialisé dans le nettoyage de transcriptions de conversations commerciales.

Ta mission est de NETTOYER le texte en supprimant :
- Les hésitations : "euh", "hum", "hmm", "ben", "bah", "voilà", "en fait", "du coup"
- Les bégaiements et répétitions involontaires
- Les formules phatiques sans valeur informative ("tu vois", "tu sais", "genre")
- Les ponctuations excessives (???, !!!, ...)
- Les espaces multiples et retours à la ligne inutiles

RÈGLES STRICTES À RESPECTER :
1. NE PAS résumer le contenu
2. NE PAS modifier le sens ou les informations
3. NE PAS changer le ton de la conversation
4. CONSERVER tous les détails importants (prix, produits, dates, noms, etc.)
5. GARDER le style conversationnel naturel
6. Corriger uniquement les erreurs évidentes de transcription

Tu dois retourner UNIQUEMENT le texte nettoyé, sans commentaire, sans introduction, sans guillemets.

Exemple :
AVANT : "Euh... ben je cherche euh un sac, tu vois, pour euh... pour ma femme quoi. Budget euh... 5000 euros environ."
APRÈS : "Je cherche un sac pour ma femme. Budget 5000 euros environ."
"""

# ============================================================================
# CLASSE PRINCIPALE
# ============================================================================

class TranscriptionCleaner:
    """Classe pour nettoyer les transcriptions avec Mistral AI"""
    
    def __init__(self, api_key: str, model: str = MISTRAL_MODEL):
        """
        Initialise le nettoyeur de transcriptions
        
        Args:
            api_key: Clé API Mistral
            model: Nom du modèle Mistral à utiliser
        """
        if not api_key:
            raise ValueError("La clé API Mistral est manquante. Vérifiez votre fichier .env")
        
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.stats = {
            'total': 0,
            'success': 0,
            'errors': 0,
            'skipped': 0
        }
    
    
    async def clean_text_async(self, text: str, max_retries: int = MAX_RETRIES) -> Optional[str]:
        """
        Nettoie un texte en utilisant l'API Mistral (version asynchrone)
        
        Args:
            text: Texte brut à nettoyer
            max_retries: Nombre maximum de tentatives
            
        Returns:
            Texte nettoyé ou None en cas d'échec
        """
        # Validation de l'entrée
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            self.stats['skipped'] += 1
            return text
        
        # Tentatives avec retry
        for attempt in range(max_retries):
            try:
                # Appel à l'API Mistral (synchrone dans un executor pour ne pas bloquer)
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.client.chat.complete(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": f"Nettoie cette transcription :\n\n{text}"
                            }
                        ],
                        temperature=0.3,
                        max_tokens=4000
                    )
                )
                
                # Extraction du texte nettoyé
                cleaned_text = response.choices[0].message.content.strip()
                
                # Validation basique du résultat
                if len(cleaned_text) < len(text) * 0.3:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(RETRY_DELAY)
                        continue
                
                self.stats['success'] += 1
                return cleaned_text
                
            except Exception as e:
                error_msg = str(e)
                
                # Gestion des erreurs spécifiques
                if "rate_limit" in error_msg.lower():
                    wait_time = RETRY_DELAY * (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                    
                elif "timeout" in error_msg.lower():
                    await asyncio.sleep(RETRY_DELAY)
                    
                else:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(RETRY_DELAY)
                    else:
                        self.stats['errors'] += 1
                        return None
        
        # Si toutes les tentatives échouent
        self.stats['errors'] += 1
        return None
    
    def clean_text(self, text: str, max_retries: int = MAX_RETRIES) -> Optional[str]:
        """
        Nettoie un texte (wrapper synchrone)
        """
        return asyncio.run(self.clean_text_async(text, max_retries))

    
    
    async def process_batch_async(self, texts: List[str]) -> List[Optional[str]]:
        """
        Traite un batch de textes en parallèle
        
        Args:
            texts: Liste de textes à nettoyer
            
        Returns:
            Liste de textes nettoyés
        """
        tasks = [self.clean_text_async(text) for text in texts]
        return await asyncio.gather(*tasks)
    
    def process_dataframe(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Traite un DataFrame complet avec traitement parallèle par batch
        
        Args:
            df: DataFrame contenant les transcriptions
            column: Nom de la colonne à nettoyer
            
        Returns:
            DataFrame avec colonne nettoyée (écrase l'originale)
        """
        if column not in df.columns:
            raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame")
        
        # Création d'une copie pour ne pas modifier l'original (au début)
        df_clean = df.copy()
        
        # Traitement avec barre de progression
        print(f"\n🧹 Nettoyage de {len(df)} transcriptions...")
        print(f"⚡ Traitement par batch de {BATCH_SIZE} requêtes en parallèle")
        self.stats['total'] = len(df)
        
        # Récupérer tous les textes
        all_texts = df[column].tolist()
        all_cleaned = []
        
        # Traiter par batch
        for i in tqdm(range(0, len(all_texts), BATCH_SIZE), desc="Progression"):
            batch = all_texts[i:i + BATCH_SIZE]
            
            # Traiter le batch en parallèle
            cleaned_batch = asyncio.run(self.process_batch_async(batch))
            all_cleaned.extend(cleaned_batch)
        
        # Remplir la colonne ORIGINALE avec les résultats (écrasement)
        for idx, cleaned_text in enumerate(all_cleaned):
            if cleaned_text:
                df_clean.at[idx, column] = cleaned_text
        
        return df_clean

    
    def print_stats(self):
        """Affiche les statistiques de traitement"""
        print("\n" + "="*60)
        print("📊 STATISTIQUES DE NETTOYAGE")
        print("="*60)
        print(f"Total de transcriptions : {self.stats['total']}")
        print(f"✅ Nettoyées avec succès : {self.stats['success']}")
        print(f"⏭️  Ignorées (vides)      : {self.stats['skipped']}")
        print(f"❌ Erreurs              : {self.stats['errors']}")
        
        if self.stats['total'] > 0:
            success_rate = (self.stats['success'] / self.stats['total']) * 100
            print(f"\n🎯 Taux de réussite : {success_rate:.1f}%")
        print("="*60 + "\n")

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def load_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données depuis un fichier CSV ou Excel
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        DataFrame pandas
    """
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Format de fichier non supporté : {file_ext}")
        
        print(f"✅ Fichier chargé : {len(df)} lignes")
        return df
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        raise

def save_data(df: pd.DataFrame, file_path: str):
    """
    Sauvegarde le DataFrame dans un fichier
    
    Args:
        df: DataFrame à sauvegarder
        file_path: Chemin de destination
    """
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.csv':
            df.to_csv(file_path, index=False, encoding='utf-8')
        elif file_ext in ['.xlsx', '.xls']:
            df.to_excel(file_path, index=False)
        else:
            raise ValueError(f"Format de fichier non supporté : {file_ext}")
        
        print(f"✅ Fichier sauvegardé : {file_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        raise

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Point d'entrée principal du script"""
    
    print("="*60)
    print("🚀 NETTOYEUR DE TRANSCRIPTIONS AVEC MISTRAL AI")
    print("="*60)
    
    try:
        # 1. Vérification de la clé API
        if not MISTRAL_API_KEY:
            print("\n❌ ERREUR : Clé API Mistral manquante !")
            print("📝 Créez un fichier .env avec : MISTRAL_API_KEY=votre_clé")
            return
        
        # 2. Chargement des données
        print(f"\n📂 Chargement de {INPUT_FILE}...")
        df = load_data(INPUT_FILE)
        
        # 3. Vérification de la colonne
        if COLUMN_NAME not in df.columns:
            print(f"\n❌ ERREUR : La colonne '{COLUMN_NAME}' n'existe pas !")
            print(f"📋 Colonnes disponibles : {', '.join(df.columns)}")
            return
        
        # 4. Initialisation du nettoyeur
        print(f"\n🤖 Initialisation de Mistral AI ({MISTRAL_MODEL})...")
        cleaner = TranscriptionCleaner(MISTRAL_API_KEY, MISTRAL_MODEL)
        
        # 5. Traitement
        df_cleaned = cleaner.process_dataframe(df, COLUMN_NAME)
        
        # 6. Sauvegarde
        print(f"\n💾 Sauvegarde dans {OUTPUT_FILE}...")
        save_data(df_cleaned, OUTPUT_FILE)
        
        # 7. Statistiques
        cleaner.print_stats()
        
        print("✨ Traitement terminé avec succès !\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Traitement interrompu par l'utilisateur")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        raise

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    main()
