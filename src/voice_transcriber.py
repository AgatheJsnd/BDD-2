"""
Module de transcription vocale avec IA
Enregistrement audio → Transcription Deepgram → Nettoyage Mistral
"""
import os
import io
import tempfile
import re
from datetime import datetime
from typing import Optional, Dict
from deepgram import DeepgramClient
from mistralai import Mistral
from src.tag_extractor import extract_all_tags


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

    def _parse_french_number_words(self, raw: str) -> Optional[int]:
        """Convertit des nombres FR simples en entier (utile pour les âges)."""
        if not raw:
            return None

        text = raw.lower().strip()
        text = text.replace("'", " ")
        text = text.replace("quatre-vingts", "quatre-vingt")
        text = text.replace("quatre vingt", "quatre-vingt")
        text = text.replace("soixante dix", "soixante-dix")
        text = text.replace("quatre-vingt dix", "quatre-vingt-dix")
        text = text.replace("-", " ")

        units = {
            "zero": 0, "zéro": 0, "un": 1, "une": 1, "deux": 2, "trois": 3,
            "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9,
        }
        teens = {
            "dix": 10, "onze": 11, "douze": 12, "treize": 13, "quatorze": 14,
            "quinze": 15, "seize": 16, "dix sept": 17, "dix huit": 18, "dix neuf": 19,
        }
        tens = {
            "vingt": 20, "trente": 30, "quarante": 40, "cinquante": 50,
            "soixante": 60, "soixante dix": 70, "quatre vingt": 80, "quatre vingt dix": 90,
        }

        # Cas directs composés avant tokenisation simple
        compact = " ".join(text.split())
        if compact in teens:
            return teens[compact]
        if compact in tens:
            return tens[compact]

        tokens = [t for t in compact.split() if t not in {"et", "de", "d"}]
        if not tokens:
            return None

        total = 0
        current = 0
        idx = 0
        while idx < len(tokens):
            tok = tokens[idx]
            nxt = tokens[idx + 1] if idx + 1 < len(tokens) else ""
            pair = f"{tok} {nxt}".strip()

            if pair in teens:
                current += teens[pair]
                idx += 2
                continue
            if pair in tens:
                current += tens[pair]
                idx += 2
                continue
            if tok in units:
                current += units[tok]
                idx += 1
                continue
            if tok in {"cent", "cents"}:
                current = max(1, current) * 100
                idx += 1
                continue
            if tok == "mille":
                total += max(1, current) * 1000
                current = 0
                idx += 1
                continue
            return None

        return total + current

    def _normalize_age_to_digits(self, text: str) -> str:
        """Convertit les âges en lettres vers chiffres (ex: quarante cinq ans -> 45 ans)."""
        if not text:
            return text

        pattern = re.compile(
            r"\b([a-zA-Zàâçéèêëîïôûùüÿœæ' -]{2,40})\s+ans\b",
            flags=re.IGNORECASE,
        )

        def repl(match):
            raw_words = match.group(1).strip()
            value = self._parse_french_number_words(raw_words)
            if value is None:
                return match.group(0)
            return f"{value} ans"

        return pattern.sub(repl, text)

    def _anonymize_rgpd(self, text: str) -> str:
        """Applique un masquage RGPD strict côté code (défense en profondeur)."""
        if not text:
            return text

        sanitized = text

        # Masquage contextuel prioritaire (fonctionne même si les numéros sont en lettres)
        sanitized = re.sub(
            r"\b(num[eé]ro\s+de\s+t[ée]l[ée]phone)\b[^.!?;\n]*",
            r"\1 [NON DIVULGUÉ - RGPD]",
            sanitized,
            flags=re.IGNORECASE,
        )
        sanitized = re.sub(
            r"\b(codes?\s+de\s+carte(?:\s+bleue)?|num[eé]ro\s+de\s+carte(?:\s+bleue)?|cb)\b[^.!?;\n]*",
            "[PAIEMENT NON DIVULGUÉ - RGPD]",
            sanitized,
            flags=re.IGNORECASE,
        )
        sanitized = re.sub(
            r"\b(adresse)\b[^.!?;\n]*",
            r"\1 [NON DIVULGUÉE - RGPD]",
            sanitized,
            flags=re.IGNORECASE,
        )

        # Cartes bancaires: suites de 13-19 chiffres, avec/sans séparateurs
        card_pattern = re.compile(r"\b(?:\d[ -]?){13,19}\b")
        sanitized = card_pattern.sub("[PAIEMENT NON DIVULGUÉ - RGPD]", sanitized)

        # Téléphones (FR/internationaux simples)
        phone_pattern = re.compile(
            r"(?:(?:\+|00)\d{1,3}[ .-]?)?(?:\(?\d{1,4}\)?[ .-]?){2,6}\d{2,4}\b"
        )
        sanitized = phone_pattern.sub(
            lambda m: "[TÉLÉPHONE NON DIVULGUÉ - RGPD]"
            if len(re.sub(r"\D", "", m.group(0))) >= 9
            else m.group(0),
            sanitized,
        )

        # Cibler explicitement les codes de carte
        sanitized = re.sub(
            r"\b(code|codes)\s+(de\s+)?(carte|carte\s+bleue|cb)[^.,;:!?]*",
            "[PAIEMENT NON DIVULGUÉ - RGPD]",
            sanitized,
            flags=re.IGNORECASE,
        )

        # Adresse complète -> garder pays si trouvé
        countries = [
            "France", "Espagne", "Italie", "Portugal", "Allemagne", "Belgique",
            "Suisse", "Royaume-Uni", "États-Unis", "USA", "Canada", "Maroc",
            "Tunisie", "Algérie", "Chine", "Japon", "Corée", "Amérique",
        ]
        country_found = None
        for c in countries:
            if re.search(rf"\b{re.escape(c)}\b", sanitized, flags=re.IGNORECASE):
                country_found = c
                break

        address_pattern = re.compile(
            r"\b\d{1,4}\s+[a-zA-Zàâçéèêëîïôûùüÿœæ' -]{2,40}\s+"
            r"(rue|route|avenue|av|boulevard|bd|chemin|all[eé]e|impasse|place|quai)\b[^.,;:!?]*",
            flags=re.IGNORECASE,
        )
        replacement = (
            f"[ADRESSE NON DIVULGUÉE - RGPD] (pays: {country_found})"
            if country_found
            else "[ADRESSE NON DIVULGUÉE - RGPD]"
        )
        sanitized = address_pattern.sub(replacement, sanitized)

        # Nettoyage des répétitions immédiates de mots
        sanitized = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(
            r"\[\s*ADRESSE\s+MASQUÉE\s*\]",
            "[ADRESSE NON DIVULGUÉE - RGPD]",
            sanitized,
            flags=re.IGNORECASE,
        )
        sanitized = re.sub(r"\s{2,}", " ", sanitized).strip()
        return sanitized
    
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
            # Prompt de nettoyage ultra-strict, RGPD et conversion numérique
            prompt = f"""Tu es un expert en conformité RGPD et éditeur professionnel pour LVMH.
            
Ta mission est de transformer la TRANSCRIPTION BRUTE en un texte parfaitement propre, fluide et ANONYMISÉ.

RÈGLES DE SÉCURITÉ RGPD (ABSOLUES) :
1. NUMÉROS DE TÉLÉPHONE : Supprime tout numéro de téléphone (même écrit en lettres) et remplace par "[TÉLÉPHONE MASQUÉ]".
2. CARTES BANCAIRES / CODES : Supprime tout numéro de carte, code secret ou identifiant de paiement et remplace par "[PAIEMENT SÉCURISÉ]".
3. ADRESSES : Supprime l'adresse complète (rue, numéro, code postal, ville). Garde UNIQUEMENT le pays. Si aucun pays n'est mentionné, ne mets rien pour l'adresse.
   Exemple : "300 route de Corsenne à Malafrota" -> Supprimer totalement.

RÈGLES DE FORMATAGE (STRICTES) :
1. CHIFFRES & ÂGES : TOUS les nombres écrits en lettres DOIVENT être convertis en chiffres.
   Exemple : "quarante-cinq ans" -> "45 ans", "deux enfants" -> "2 enfants", "quinze mille" -> "15000".
2. SUPPRESSION DES DOUBLONS : Élimine systématiquement toute répétition de mots (ex: "je je" -> "je").
3. MOTS PARASITES : Supprime "Euh", "Voilà", "Du coup", "En fait", "Genre", "Tu vois".
4. FLUIDITÉ : Le texte doit être une note professionnelle parfaite.

TRANSCRIPTION BRUTE :
{raw_text}

TEXTE NETTOYÉ ET ANONYMISÉ :"""

            # Appel Mistral avec le modèle le plus puissant pour une compréhension parfaite des chiffres en lettres
            response = self.mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=2000
            )
            
            cleaned = response.choices[0].message.content.strip()
            cleaned = self._normalize_age_to_digits(cleaned)
            cleaned = self._anonymize_rgpd(cleaned)
            
            return {
                "success": True,
                "cleaned_text": cleaned,
                "original_text": raw_text,
                "error": None
            }
            
        except Exception as e:
            fallback = self._normalize_age_to_digits(raw_text)
            fallback = self._anonymize_rgpd(fallback)
            return {
                "success": False,
                "cleaned_text": fallback,
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
            cleaned = self._normalize_age_to_digits(raw_text)
            cleaned = self._anonymize_rgpd(cleaned)
        
        tags = extract_all_tags(cleaned)
        # Sécurité supplémentaire: si l'âge n'est pas trouvé après nettoyage,
        # retenter sur la transcription brute.
        if not tags.get("age"):
            raw_tags = extract_all_tags(raw_text)
            if raw_tags.get("age"):
                tags["age"] = raw_tags.get("age")

        return {
            "success": True,
            "transcription": raw_text,
            "cleaned_text": cleaned,
            "confidence": transcription_result.get("confidence", 0.0),
            "tags_extracted": tags,
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
    metadata = transcription_data.get("metadata_vendeur", {})
    
    row = {
        "date": transcription_data.get("saved_at", datetime.now().isoformat()),
        "client_id": transcription_data.get("client_id", "Inconnu"),
        "nom": metadata.get("nom", ""),
        "prenom": metadata.get("prenom", ""),
        "telephone": metadata.get("telephone", ""),
        "email": metadata.get("email", ""),
        "canaux_contact": ", ".join(metadata.get("canaux_contact", [])),
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
    Sauvegarde une transcription dans le fichier JSON ET le CSV
    
    Args:
        transcription_data: Résultat de process_voice_recording()
        client_id: ID du client (optionnel)
    """
    # Ajouter métadonnées
    transcription_data["client_id"] = client_id or f"VOICE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    transcription_data["saved_at"] = datetime.now().isoformat()
    
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
    Charge depuis le fichier
    
    Returns:
        list: Liste des transcriptions
    """
    return _load_transcriptions_from_file()
