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
            # Préparer les options de transcription
            options = {
                "model": "nova-2",  # Modèle le plus récent et précis
                "language": language,
                "punctuate": True,  # Ponctuation automatique
                "smart_format": True,  # Formatage intelligent (dates, nombres, etc.)
                "diarize": False,  # Pas de séparation des locuteurs
            }
            
            # Créer la source audio
            payload = {
                "buffer": audio_bytes,
            }
            
            # Appel API Deepgram
            response = self.deepgram_client.listen.rest.v("1").transcribe_file(
                payload, options
            )
            
            # Extraire le texte transcrit
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            confidence = response["results"]["channels"][0]["alternatives"][0]["confidence"]
            
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


def save_transcription_to_session(transcription_data: Dict, client_id: str = None):
    """
    Sauvegarde une transcription dans la session Streamlit
    
    Args:
        transcription_data: Résultat de process_voice_recording()
        client_id: ID du client (optionnel)
    """
    if "voice_transcriptions" not in st.session_state:
        st.session_state["voice_transcriptions"] = []
    
    # Ajouter métadonnées
    transcription_data["client_id"] = client_id or f"VOICE_{len(st.session_state['voice_transcriptions']) + 1}"
    transcription_data["saved_at"] = datetime.now().isoformat()
    
    st.session_state["voice_transcriptions"].append(transcription_data)


def get_transcriptions_history() -> list:
    """
    Récupère l'historique des transcriptions vocales
    
    Returns:
        list: Liste des transcriptions
    """
    return st.session_state.get("voice_transcriptions", [])
