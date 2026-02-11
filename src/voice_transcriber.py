"""
Module de transcription vocale avec IA
Enregistrement audio → Transcription Deepgram → Nettoyage Mistral
"""
import os
import io
import tempfile
from datetime import datetime
from typing import Optional, Dict
from deepgram import DeepgramClient
from mistralai import Mistral
import streamlit as st


class VoiceTranscriber:
    """Gère l'enregistrement vocal et la transcription avec IA"""
    
    def __init__(self, deepgram_api_key: Optional[str] = None, mistral_api_key: Optional[str] = None):
        """
        Initialise le transcripteur vocal
        
        Args:
            deepgram_api_key: Clé API Deepgram (pour transcription)
            mistral_api_key: Clé API Mistral (pour nettoyage)
        """
        # Deepgram pour transcription
        self.deepgram_key = deepgram_api_key or os.getenv("DEEPGRAM_API_KEY")
        if self.deepgram_key:
            try:
                # Initialisation simple avec la clé API
                self.deepgram_client = DeepgramClient(api_key=self.deepgram_key)
            except Exception as e:
                self.deepgram_client = None
                print(f"Erreur initialisation Deepgram: {e}")
        else:
            self.deepgram_client = None
        
        # Mistral pour nettoyage
        self.mistral_key = mistral_api_key or os.getenv("MISTRAL_API_KEY")
        if self.mistral_key:
            self.mistral_client = Mistral(api_key=self.mistral_key)
        else:
            self.mistral_client = None
    
    def transcribe_audio(self, audio_bytes: bytes, language: str = "fr") -> Dict:
        """
        Transcrit un fichier audio en texte avec Deepgram
        
        Args:
            audio_bytes: Données audio en bytes
            language: Langue de l'audio (défaut: français)
            
        Returns:
            dict: {
                "success": bool,
                "text": str,
                "confidence": float,
                "error": str (si échec)
            }
        """
        if not self.deepgram_client:
            return {
                "success": False,
                "text": "",
                "confidence": 0.0,
                "error": "⚠️ DEEPGRAM_API_KEY non configurée. Ajoutez-la dans le fichier .env"
            }
        
        try:
            # Pour la version 5.3.2 du SDK, nous passons les options 
            # directement comme arguments nommés à la méthode transcribe_file
            # et les données (bytes) directement dans l'argument 'request'
            
            # Appel API Deepgram (v5 structure interne spécifique)
            response = self.deepgram_client.listen.v1.media.transcribe_file(
                request=audio_bytes,  # Passer les bytes directement, pas un dict
                model="nova-2",
                language=language,
                smart_format=True,
                punctuate=True
            )
            
            # Extraction du texte (Gestion robuste de la réponse)
            # D'après le code source, la réponse a un attribut 'results' ...
            if hasattr(response, 'results'):
                res_obj = response
            elif isinstance(response, dict) and "results" in response:
                res_obj = response
            else:
                # Tentative via to_dict si disponible
                res_dict = response.to_dict() if hasattr(response, 'to_dict') else response
                res_obj = res_dict

            # Accès aux données
            try:
                # Si c'est un objet (Pydantic/Dataclass), on accède par attribut ou index
                if isinstance(res_obj, dict):
                    alt = res_obj["results"]["channels"][0]["alternatives"][0]
                    transcript = alt["transcript"]
                    confidence = alt["confidence"]
                else:
                    alt = res_obj.results.channels[0].alternatives[0]
                    transcript = alt.transcript
                    confidence = alt.confidence
            except:
                # Fallback ultime via conversion dict
                res_dict = response.to_dict() if hasattr(response, 'to_dict') else dict(response)
                alt = res_dict["results"]["channels"][0]["alternatives"][0]
                transcript = alt["transcript"]
                confidence = alt["confidence"]
            
            return {
                "success": True,
                "text": transcript,
                "confidence": confidence,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "confidence": 0.0,
                "error": f"Erreur de transcription: {str(e)}"
            }
    
    def clean_transcription(self, raw_text: str) -> Dict:
        """
        Nettoie une transcription avec Mistral AI
        Supprime les "euh", répétitions, et met au propre
        
        Args:
            raw_text: Texte brut de la transcription
            
        Returns:
            dict: {
                "success": bool,
                "cleaned_text": str,
                "original_text": str,
                "error": str (si échec)
            }
        """
        if not self.mistral_client:
            return {
                "success": False,
                "cleaned_text": raw_text,
                "original_text": raw_text,
                "error": "⚠️ MISTRAL_API_KEY non configurée"
            }
        
        try:
            # Prompt de nettoyage optimisé
            prompt = f"""Tu es un assistant spécialisé dans le nettoyage de transcriptions vocales.

TRANSCRIPTION BRUTE :
{raw_text}

INSTRUCTIONS :
1. Supprime tous les mots de remplissage : "euh", "hum", "ben", "voilà", "donc", etc.
2. Élimine les répétitions inutiles
3. Corrige les fautes de grammaire évidentes
4. Garde le sens exact et le ton naturel
5. Ne rajoute RIEN, ne change pas le contenu
6. Retourne UNIQUEMENT le texte nettoyé, sans commentaire

TEXTE NETTOYÉ :"""

            # Appel Mistral
            response = self.mistral_client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            cleaned = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "cleaned_text": cleaned,
                "original_text": raw_text,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "cleaned_text": raw_text,
                "original_text": raw_text,
                "error": f"Erreur de nettoyage: {str(e)}"
            }
    
    def process_voice_recording(self, audio_bytes: bytes, language: str = "fr", clean: bool = True) -> Dict:
        """
        Pipeline complet : Audio → Transcription → Nettoyage
        
        Args:
            audio_bytes: Données audio
            language: Langue (défaut: français)
            clean: Appliquer le nettoyage IA (défaut: True)
            
        Returns:
            dict: {
                "success": bool,
                "transcription": str (texte brut),
                "cleaned_text": str (texte nettoyé),
                "timestamp": str,
                "error": str (si échec)
            }
        """
        # Étape 1: Transcription
        transcription_result = self.transcribe_audio(audio_bytes, language)
        
        if not transcription_result["success"]:
            return {
                "success": False,
                "transcription": "",
                "cleaned_text": "",
                "timestamp": datetime.now().isoformat(),
                "error": transcription_result["error"]
            }
        
        raw_text = transcription_result["text"]
        
        # Étape 2: Nettoyage (optionnel)
        if clean and self.mistral_client:
            cleaning_result = self.clean_transcription(raw_text)
            cleaned = cleaning_result["cleaned_text"]
        else:
            cleaned = raw_text
        
        return {
            "success": True,
            "transcription": raw_text,
            "cleaned_text": cleaned,
            "timestamp": datetime.now().isoformat(),
            "error": None
        }


import json
import csv

def _get_data_file_path():
    """Retourne le chemin vers le fichier de données JSON"""
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, "transcriptions.json")

def _load_transcriptions_from_file() -> list:
    """Charge les transcriptions depuis le fichier JSON"""
    file_path = _get_data_file_path()
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur chargement transcriptions: {e}")
            return []
    return []

def _save_transcription_to_file(transcription_data: Dict):
    """Sauvegarde une transcription dans le fichier JSON"""
    transcriptions = _load_transcriptions_from_file()
    transcriptions.append(transcription_data)
    
    file_path = _get_data_file_path()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(transcriptions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur sauvegarde transcription: {e}")

def _save_to_csv(transcription_data: Dict):
    """Sauvegarde la transcription dans un fichier CSV principal"""
    csv_path = os.path.join(os.getcwd(), "data", "interactions_vendeur.csv")
    file_exists = os.path.exists(csv_path)
    
    # Aplatir les données pour le CSV
    tags = transcription_data.get("tags", {})
    row = {
        "date": transcription_data.get("saved_at", datetime.now().isoformat()),
        "client_id": transcription_data.get("client_id", "Inconnu"),
        "transcription": transcription_data.get("text", ""),
        "texte_nettoye": transcription_data.get("cleaned_text", ""),
        "confiance": transcription_data.get("confidence", 0),
        "urgence": tags.get("urgence_score", 1),
        "ville": tags.get("ville", ""),
        "budget": tags.get("budget", ""),
        "styles": ", ".join(tags.get("style", [])),
        "motifs": ", ".join(tags.get("motif_achat", []))
    }
    
    try:
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys(), delimiter=';')
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Erreur sauvegarde CSV: {e}")

def save_transcription_to_session(transcription_data: Dict, client_id: str = None):
    """
    Sauvegarde une transcription dans la session Streamlit, le fichier JSON ET le CSV
    
    Args:
        transcription_data: Résultat de process_voice_recording()
        client_id: ID du client (optionnel)
    """
    if "voice_transcriptions" not in st.session_state:
        st.session_state["voice_transcriptions"] = _load_transcriptions_from_file()
    
    # Ajouter métadonnées
    transcription_data["client_id"] = client_id or f"VOICE_{len(st.session_state['voice_transcriptions']) + 1}"
    transcription_data["saved_at"] = datetime.now().isoformat()
    
    # Sauvegarder en mémoire
    st.session_state["voice_transcriptions"].append(transcription_data)
    
    # Sauvegarder sur disque (JSON pour l'historique app)
    _save_transcription_to_file(transcription_data)
    
    # Sauvegarder sur disque (CSV pour la base de données)
    _save_to_csv(transcription_data)

def delete_transcription_from_file(index: int):
    """Supprime une transcription du fichier par son index"""
    transcriptions = _load_transcriptions_from_file()
    if 0 <= index < len(transcriptions):
        transcriptions.pop(index)
        
        file_path = _get_data_file_path()
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(transcriptions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur suppression transcription: {e}")

def clear_all_transcriptions_file():
    """Efface tout l'historique du fichier"""
    file_path = _get_data_file_path()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
    except Exception as e:
        print(f"Erreur nettoyage transcriptions: {e}")

def get_transcriptions_history() -> list:
    """
    Récupère l'historique des transcriptions vocales
    Charge depuis le fichier si la session est vide
    
    Returns:
        list: Liste des transcriptions
    """
    # Toujours recharger du fichier pour être sûr d'avoir la dernière version
    # Sauf si on veut optimiser, mais ici la cohérence est prioritaire
    loaded_data = _load_transcriptions_from_file()
    st.session_state["voice_transcriptions"] = loaded_data
        
    return st.session_state.get("voice_transcriptions", [])
