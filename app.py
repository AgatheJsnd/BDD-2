"""
Application Streamlit - Architecture Hybride Python + IA
Extraction tags Python (gratuit) + Analyse IA (1 appel) + Dashboard Looker intégré
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import re
import os
from datetime import datetime
from mistralai import Mistral
from dotenv import load_dotenv

# Import modules custom
from src.tag_extractor import extract_all_tags
from src.ai_analyzer import analyze_batch
from src.auth import authenticate

# Charger variables d'environnement
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="LVMH Client Analytics - Hybrid AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def init_mistral_client():
    """Initialise le client Mistral AI"""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("⚠️ MISTRAL_API_KEY non trouvée dans .env")
        st.stop()
    return Mistral(api_key=api_key)


def process_transcription(client: Mistral, client_id: str, transcription: str) -> dict:
    """
    Pipeline complet : Extraction Python + Analyse IA
    
    Returns:
        dict: Résultats complets (tags + analyse IA)
    """
    # ÉTAPE 1: Extraction tags Python (gratuit, instant)
    tags = extract_all_tags(transcription)
    
    # ÉTAPE 2: Analyse IA avec tags pré-extraits (1 appel)
    analysis = analyze_with_tags(client, transcription, tags, client_id)
    
    # Combiner résultats
    analysis["transcription_originale"] = transcription[:200] + "..."
    
    return analysis


def sanitize_display_text(text: str) -> str:
    """Nettoyage léger pour éviter l'injection HTML dans l'UI."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'(?is)<script.*?>.*?</script>', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def detect_date_column(df: pd.DataFrame):
    """Détecte une colonne de date exploitable dans le CSV."""
    candidates = [
        c for c in df.columns
        if any(k in c.lower() for k in ["date", "created", "time", "timestamp"])
    ]
    for col in candidates:
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().any():
            return col
    return None


def parse_date_value(value):
    try:
        return pd.to_datetime(value, errors="coerce")
    except Exception:
        return pd.NaT


def _list_to_text(value):
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return value


def build_export_dataframe(results):
    rows = []
    for r in results:
        tags = r.get("tags_extracted", {})
        insights = r.get("insights_marketing", {})
        analysis = r.get("analyse_intelligente", {})
        rows.append({
            "client_id": r.get("client_id"),
            "source_date": r.get("source_date"),
            "segment_client": r.get("segment_client"),
            "ice_breaker": r.get("ice_breaker"),
            "resume_complet": r.get("resume_complet"),
            "urgency_score_final": r.get("urgency_score_final"),
            "budget": tags.get("budget"),
            "ville": tags.get("ville"),
            "age": tags.get("age"),
            "motif_achat": _list_to_text(tags.get("motif_achat", [])),
            "style": _list_to_text(tags.get("style", [])),
            "famille": _list_to_text(tags.get("famille", [])),
            "centres_interet": _list_to_text(tags.get("centres_interet", [])),
            "opportunites_vente": _list_to_text(insights.get("opportunites_vente", [])),
            "produits_recommandes": _list_to_text(insights.get("produits_recommandes", [])),
            "actions_suggerees": _list_to_text(insights.get("actions_suggerees", [])),
            "nouveaux_tags_suggeres": _list_to_text(analysis.get("nouveaux_tags_suggeres", [])),
            "strategie_avancee": _list_to_text(analysis.get("strategie_avancee", [])),
            "objections_freins": _list_to_text(r.get("objections_freins", [])),
            "transcription_originale": r.get("transcription_originale"),
            "cleaned_text": r.get("cleaned_text")
        })
    return pd.DataFrame(rows)

def get_available_fields(results):
    """Extract all available fields from results for chart building."""
    if not results:
        return {}
    
    fields = {
        "Démographiques": [],
        "Achat": [],
        "Préférences": [],
        "IA Insights": []
    }
    
    # Sample first result to get structure
    sample = results[0]
    tags = sample.get("tags_extracted", {})
    
    # Demographics
    if tags.get("age"): fields["Démographiques"].append("age")
    if tags.get("ville"): fields["Démographiques"].append("ville")
    if tags.get("profession"): fields["Démographiques"].append("profession")
    if tags.get("famille"): fields["Démographiques"].append("famille")
    
    # Purchase
    if tags.get("budget"): fields["Achat"].append("budget")
    if tags.get("urgence_score"): fields["Achat"].append("urgence_score")
    if tags.get("motif_achat"): fields["Achat"].append("motif_achat")
    
    # Preferences
    if tags.get("couleurs"): fields["Préférences"].append("couleurs")
    if tags.get("matieres"): fields["Préférences"].append("matieres")
    if tags.get("style"): fields["Préférences"].append("style")
    if tags.get("centres_interet"): fields["Préférences"].append("centres_interet")
    
    # AI Insights (if available)
    if sample.get("segment_client"): fields["IA Insights"].append("segment_client")
    if sample.get("urgency_score_final"): fields["IA Insights"].append("urgency_score_final")
    
    return fields


def prepare_chart_data(results, x_field, y_field=None, chart_type="bar", filters=None):
    """Prepare data for charting based on selected fields and filters."""
    filtered_results = results
    
    # Apply filters if provided
    if filters:
        if filters.get("urgency_min"):
            filtered_results = [r for r in filtered_results if r.get("urgency_score_final", 1) >= filters["urgency_min"]]
        if filters.get("segments"):
            filtered_results = [r for r in filtered_results if r.get("segment_client") in filters["segments"]]
    
    data = []
    for r in filtered_results:
        tags = r.get("tags_extracted", {})
        
        # Get x value
        if x_field in ["age", "ville", "budget", "profession", "famille"]:
            x_val = tags.get(x_field)
        elif x_field in ["urgence_score"]:
            x_val = tags.get(x_field)
        elif x_field in ["segment_client", "urgency_score_final"]:
            x_val = r.get(x_field)
        elif x_field in ["motif_achat", "couleurs", "matieres", "style", "centres_interet"]:
            x_val = tags.get(x_field, [])
            if isinstance(x_val, list) and x_val:
                x_val = x_val[0]  # Take first item for simplicity
        else:
            x_val = None
        
        # Get y value if needed
        y_val = None
        if y_field:
            if y_field in ["age", "ville", "budget"]:
                y_val = tags.get(y_field)
            elif y_field in ["urgency_score_final"]:
                y_val = r.get(y_field)
        
        if x_val:
            data.append({"x": x_val, "y": y_val if y_val else 1})
    
    return data


def create_custom_chart(data, chart_type, x_label, y_label="Count"):
    """Create a Plotly chart based on configuration."""
    if not data:
        return None
    
    df = pd.DataFrame(data)
    
    if chart_type == "bar":
        # Count occurrences
        counts = df["x"].value_counts().reset_index()
        counts.columns = [x_label, "Count"]
        fig = px.bar(counts, x=x_label, y="Count", color_discrete_sequence=["#4285F4"])
    
    elif chart_type == "pie":
        counts = df["x"].value_counts().reset_index()
        counts.columns = [x_label, "Count"]
        fig = px.pie(counts, names=x_label, values="Count", hole=0.4)
    
    elif chart_type == "line":
        counts = df["x"].value_counts().reset_index()
        counts.columns = [x_label, "Count"]
        counts = counts.sort_values(x_label)
        fig = px.line(counts, x=x_label, y="Count", markers=True)
    
    elif chart_type == "scatter":
        fig = px.scatter(df, x="x", y="y", labels={"x": x_label, "y": y_label})
    
    else:  # heatmap or default
        counts = df["x"].value_counts().reset_index()
        counts.columns = [x_label, "Count"]
        fig = px.bar(counts, x=x_label, y="Count")
    
    fig.update_layout(height=500)
    return fig


# ============================================================================
# INTERFACES PAR RÔLE
# ============================================================================

def show_vendeur_interface():
    """Interface pour les vendeurs avec enregistrement vocal"""
    from audio_recorder_streamlit import audio_recorder
    from src.voice_transcriber import VoiceTranscriber, save_transcription_to_session, get_transcriptions_history
    from src.tag_extractor import extract_all_tags
    
    # Bouton de déconnexion dans la sidebar
    with st.sidebar:
        st.markdown("---")
        user = st.session_state.get("user", {})
        st.markdown(f"**👤 {user.get('name', 'Utilisateur')}**")
        st.caption(f"Rôle : {user.get('role', 'N/A').upper()}")
        
        # Statistiques rapides
        st.markdown("---")
        st.subheader("📊 Mes Stats")
        transcriptions = get_transcriptions_history()
        st.metric("Enregistrements", len(transcriptions))
        
        if st.button("🚪 Déconnexion", use_container_width=True):
            # Clear session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Header
    st.title("👔 Espace Vendeur")
    st.markdown("**Enregistrez vos conversations clients en un clic**")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🎤 Nouvel Enregistrement", "📋 Historique", "⚙️ Configuration"])
    
    # ============================================================================
    # TAB 1: NOUVEL ENREGISTREMENT
    # ============================================================================
    with tab1:
        st.header("🎤 Enregistrement Vocal")
        
        # Vérifier les clés API
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        mistral_key = os.getenv("MISTRAL_API_KEY")
        
        col_status1, col_status2 = st.columns(2)
        with col_status1:
            if deepgram_key:
                st.success("✅ Deepgram configuré")
            else:
                st.error("❌ Deepgram API manquante")
        
        with col_status2:
            if mistral_key:
                st.success("✅ Mistral AI configuré")
            else:
                st.warning("⚠️ Mistral AI manquante (nettoyage désactivé)")
        
        if not deepgram_key:
            st.error("""
            **Configuration requise :**
            
            Pour utiliser la transcription vocale, ajoutez votre clé Deepgram dans le fichier `.env` :
            ```
            DEEPGRAM_API_KEY=votre_clé_ici
            ```
            
            Obtenez une clé GRATUITE ($200 de crédits) sur : https://console.deepgram.com/
            """)
            st.stop()
        
        st.markdown("---")
        
        # Formulaire client
        with st.form("client_info_form"):
            st.subheader("📝 Informations Client")
            col1, col2 = st.columns(2)
            
            with col1:
                client_id = st.text_input("ID Client (optionnel)", placeholder="Ex: CLIENT_001")
            
            with col2:
                client_name = st.text_input("Nom du client (optionnel)", placeholder="Ex: Marie Dupont")
            
            submitted = st.form_submit_button("💾 Enregistrer les infos", use_container_width=True)
            
            if submitted:
                if client_id or client_name:
                    st.session_state["current_client_id"] = client_id or client_name
                    st.success(f"✅ Client enregistré : {st.session_state['current_client_id']}")
        
        st.markdown("---")
        
        # Zone d'enregistrement
        st.subheader("🎙️ Enregistrer la conversation")
        st.info("👇 Cliquez sur le micro pour démarrer l'enregistrement, puis cliquez à nouveau pour arrêter.")
        
        # Audio recorder
        audio_bytes = audio_recorder(
            text="Cliquez pour enregistrer",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x",
        )
        
        if audio_bytes:
            st.success("✅ Enregistrement capturé !")
            
            # Lecture audio
            st.audio(audio_bytes, format="audio/wav")
            
            # Options de traitement
            col_opt1, col_opt2 = st.columns(2)
            
            with col_opt1:
                auto_clean = st.checkbox("🧹 Nettoyage automatique (IA)", value=True, help="Supprime les 'euh', répétitions, etc.")
            
            with col_opt2:
                language = st.selectbox("🌍 Langue", ["fr", "en", "es", "it", "de"], index=0)
            
            # Bouton de transcription
            if st.button("🚀 Transcrire et Analyser", type="primary", use_container_width=True):
                with st.spinner("🎯 Transcription en cours..."):
                    # Initialiser le transcripteur
                    transcriber = VoiceTranscriber()
                    
                    # Traitement complet
                    result = transcriber.process_voice_recording(
                        audio_bytes=audio_bytes,
                        language=language,
                        clean=auto_clean
                    )
                    
                    if result["success"]:
                        # Affichage des résultats
                        confidence = result.get("confidence", 0.0)
                        st.success(f"✅ Transcription terminée ! (Confiance: {confidence*100:.1f}%)")
                        
                        # Texte brut
                        with st.expander("📝 Transcription brute", expanded=False):
                            st.text_area("Texte original", result["transcription"], height=150, disabled=True)
                            if confidence > 0:
                                st.caption(f"🎯 Score de confiance : {confidence*100:.1f}%")
                        
                        # Texte nettoyé
                        st.subheader("✨ Texte nettoyé")
                        cleaned_text = st.text_area(
                            "Vous pouvez modifier le texte si nécessaire",
                            result["cleaned_text"],
                            height=200,
                            key="cleaned_text_edit"
                        )
                        
                        # Extraction des tags
                        st.markdown("---")
                        st.subheader("🏷️ Tags détectés automatiquement")
                        
                        with st.spinner("Analyse des tags..."):
                            tags = extract_all_tags(cleaned_text)
                        
                        # Affichage des tags
                        col_tag1, col_tag2, col_tag3 = st.columns(3)
                        
                        with col_tag1:
                            st.markdown("**📍 Informations**")
                            if tags.get("ville"):
                                st.write(f"🏙️ Ville: {tags['ville']}")
                            if tags.get("age"):
                                st.write(f"👤 Âge: {tags['age']}")
                            if tags.get("budget"):
                                st.write(f"💰 Budget: {tags['budget']}")
                        
                        with col_tag2:
                            st.markdown("**🎯 Préférences**")
                            if tags.get("style"):
                                st.write(f"✨ Style: {', '.join(tags['style'][:3])}")
                            if tags.get("couleurs"):
                                st.write(f"🎨 Couleurs: {', '.join(tags['couleurs'][:3])}")
                            if tags.get("matieres"):
                                st.write(f"🧵 Matières: {', '.join(tags['matieres'][:3])}")
                        
                        with col_tag3:
                            st.markdown("**📊 Analyse**")
                            st.write(f"⚡ Urgence: {tags.get('urgence_score', 1)}/5")
                            if tags.get("motif_achat"):
                                st.write(f"🎁 Motif: {', '.join(tags['motif_achat'][:2])}")
                        
                        # Sauvegarder
                        st.markdown("---")
                        if st.button("💾 Sauvegarder cette transcription", type="primary", use_container_width=True):
                            client_id = st.session_state.get("current_client_id", None)
                            
                            # Enrichir les données
                            result["tags"] = tags
                            result["client_name"] = client_name if 'client_name' in locals() else None
                            
                            save_transcription_to_session(result, client_id)
                            st.success("✅ Transcription sauvegardée !")
                            st.balloons()
                            
                        # Bouton pour abandonner
                        if st.button("🗑️ Supprimer / Abandonner", type="secondary", use_container_width=True):
                            st.rerun()
                    
                    else:
                        st.error(f"❌ {result['error']}")
    
    # ============================================================================
    # TAB 2: HISTORIQUE
    # ============================================================================
    with tab2:
        st.header("📋 Historique des Enregistrements")
        
        transcriptions = get_transcriptions_history()
        
        if not transcriptions:
            st.info("Aucun enregistrement pour le moment. Commencez par créer votre premier enregistrement dans l'onglet 'Nouvel Enregistrement'.")
        else:
            col_titre, col_del_all = st.columns([3, 1])
            with col_titre:
                st.success(f"**{len(transcriptions)} enregistrement(s) sauvegardé(s)**")
            with col_del_all:
                if st.button("🗑️ Tout effacer", type="primary", use_container_width=True):
                     if "voice_transcriptions" in st.session_state:
                         del st.session_state["voice_transcriptions"]
                     st.rerun()

            
            # Affichage en cartes
            # On utilise indices inversés pour la suppression correcte (le dernier est le premier affiché)
            # Mais attention, si on supprime par index, il faut utiliser l'index original.
            # Reversed retourne un itérateur.
            
            # On crée une liste inversée avec les index originaux : [(index, item)]
            items_with_index = list(enumerate(transcriptions))
            reversed_items = list(reversed(items_with_index))
            
            for original_idx, trans in reversed_items:
                with st.container(border=True):
                    col_h1, col_h2, col_h3, col_h4 = st.columns([2, 1, 0.5, 0.5])
                    
                    with col_h1:
                        client_id = trans.get("client_id", f"Enregistrement")
                        st.markdown(f"**🎤 {client_id}**")
                        timestamp = trans.get("timestamp", "")
                        if timestamp:
                            st.caption(f"📅 {timestamp[:19].replace('T', ' à ')}")
                    
                    with col_h2:
                        if trans.get("tags"):
                            urgence = trans["tags"].get("urgence_score", 1)
                            st.metric("Urgence", f"{urgence}/5")
                    
                    with col_h3:
                        if st.button("👁️", key=f"view_{original_idx}", help="Voir les détails"):
                            st.session_state[f"show_detail_{original_idx}"] = not st.session_state.get(f"show_detail_{original_idx}", False)
                    
                    with col_h4:
                        if st.button("🗑️", key=f"del_{original_idx}", help="Supprimer cet enregistrement"):
                            # Suppression sécurisée par index
                            transcriptions.pop(original_idx)
                            st.session_state["voice_transcriptions"] = transcriptions
                            st.rerun()
                    
                    # Détails (expandable)
                    if st.session_state.get(f"show_detail_{original_idx}", False):
                        st.markdown("---")
                        st.markdown("**💬 Transcription nettoyée :**")
                        st.write(trans.get("cleaned_text", "N/A"))
                        
                        if trans.get("tags"):
                            st.markdown("**🏷️ Tags détectés :**")
                            tags = trans["tags"]
                            st.json(tags)
            
            # Export CSV
            st.markdown("---")
            if st.button("📥 Exporter tout en CSV", use_container_width=True):
                # Créer un DataFrame
                export_data = []
                for trans in transcriptions:
                    tags = trans.get("tags", {})
                    export_data.append({
                        "client_id": trans.get("client_id"),
                        "timestamp": trans.get("timestamp"),
                        "transcription": trans.get("transcription"),
                        "cleaned_text": trans.get("cleaned_text"),
                        "ville": tags.get("ville"),
                        "age": tags.get("age"),
                        "budget": tags.get("budget"),
                        "urgence": tags.get("urgence_score"),
                        "style": ", ".join(tags.get("style", [])),
                        "motif_achat": ", ".join(tags.get("motif_achat", []))
                    })
                
                df_export = pd.DataFrame(export_data)
                csv = df_export.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=csv,
                    file_name=f"transcriptions_vendeur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    # ============================================================================
    # TAB 3: CONFIGURATION
    # ============================================================================
    with tab3:
        st.header("⚙️ Configuration")
        
        st.subheader("🔑 Clés API")
        
        # Status Deepgram
        if deepgram_key:
            st.success("✅ **Deepgram API** : Configurée")
            st.caption("Utilisée pour la transcription vocale (Nova-2)")
        else:
            st.error("❌ **Deepgram API** : Non configurée")
            st.code("DEEPGRAM_API_KEY=votre_clé_ici", language="bash")
            st.caption("Ajoutez cette ligne dans le fichier `.env`")
            st.info("🎁 **Offre gratuite** : $200 de crédits sur https://console.deepgram.com/")
        
        # Status Mistral
        if mistral_key:
            st.success("✅ **Mistral AI** : Configurée")
            st.caption("Utilisée pour le nettoyage des transcriptions")
        else:
            st.warning("⚠️ **Mistral AI** : Non configurée")
            st.caption("Le nettoyage automatique sera désactivé")
        
        st.markdown("---")
        
        st.subheader("📖 Guide d'utilisation")
        
        st.markdown("""
        ### Comment utiliser l'enregistrement vocal ?
        
        1. **Préparez-vous** : Ayez le client devant vous ou ses informations
        2. **Cliquez sur le micro** 🎙️ pour démarrer l'enregistrement
        3. **Parlez naturellement** : Décrivez la conversation avec le client
        4. **Arrêtez l'enregistrement** en cliquant à nouveau sur le micro
        5. **Cliquez sur "Transcrire"** : L'IA va transformer votre voix en texte
        6. **Vérifiez le texte** : Vous pouvez le modifier si nécessaire
        7. **Sauvegardez** : Les tags seront automatiquement extraits
        
        ### Conseils pour de meilleurs résultats
        
        - 🎯 Parlez clairement et à un rythme normal
        - 📍 Mentionnez les informations clés : budget, style, préférences
        - 🔇 Enregistrez dans un endroit calme si possible
        - ✅ Relisez toujours la transcription avant de sauvegarder
        
        ### Que fait l'IA ?
        
        1. **Deepgram (Nova-2)** : Transforme votre voix en texte (95%+ précision)
        2. **Mistral AI** : Nettoie le texte (supprime les "euh", répétitions)
        3. **Moteur Python** : Extrait automatiquement les tags (ville, budget, style, etc.)
        """)


# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

def main():
    # ============================================================================
    # AUTHENTIFICATION
    # ============================================================================
    
    # Initialiser l'état d'authentification
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Si non authentifié, afficher la page de connexion
    if not st.session_state["authenticated"]:
        # Style de la page de connexion
        st.markdown("""
            <style>
            .login-container {
                max-width: 500px;
                margin: 100px auto;
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            .login-title {
                color: white;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: bold;
            }
            .login-subtitle {
                color: rgba(255,255,255,0.9);
                text-align: center;
                margin-bottom: 30px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<h1 class="login-title">🎯 LVMH</h1>', unsafe_allow_html=True)
            st.markdown('<p class="login-subtitle">Client Analytics Platform</p>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Nom d'utilisateur", placeholder="analyste")
                password = st.text_input("🔒 Mot de passe", type="password", placeholder="••••••••")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit = st.form_submit_button("🚀 Connexion", use_container_width=True)
                with col_btn2:
                    help_btn = st.form_submit_button("❓ Aide", use_container_width=True)
                
                if submit:
                    if username and password:
                        user_info = authenticate(username, password)
                        if user_info:
                            st.session_state["authenticated"] = True
                            st.session_state["user"] = user_info
                            st.success(f"✅ Bienvenue {user_info['name']} !")
                            st.rerun()
                        else:
                            st.error("❌ Identifiants incorrects")
                    else:
                        st.warning("⚠️ Veuillez remplir tous les champs")
                
                if help_btn:
                    st.info("""
                    **Comptes Disponibles :**
                    
                    👔 **Vendeur**
                    - Utilisateur : `vendeur`
                    - Mot de passe : `vendeur123`
                    
                    📊 **Analyste**
                    - Utilisateur : `analyste`
                    - Mot de passe : `analyste123`
                    """)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Arrêter l'exécution ici si non authentifié
        st.stop()
    
    # ============================================================================
    # APPLICATION PRINCIPALE (après authentification)
    # ============================================================================
    
    # Routage par rôle
    user = st.session_state.get("user", {})
    user_role = user.get("role", "")
    
    if user_role == "vendeur":
        # Rediriger vers l'espace vendeur
        show_vendeur_interface()
        return  # Arrêter l'exécution ici pour ne pas afficher l'interface analyste
    
    # Si analyste ou autre, continuer avec l'interface complète
    
    # Bouton de déconnexion dans la sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**👤 {user.get('name', 'Utilisateur')}**")
        st.caption(f"Rôle : {user.get('role', 'N/A').upper()}")
        
        if st.button("🚪 Déconnexion", use_container_width=True):
            # Clear session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Header
    st.title("🎯 LVMH Client Analytics")
    st.markdown("**Architecture Hybride:** Python (tags) + IA (insights) + Dashboard Looker")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Vérifier API
        api_key = os.getenv("MISTRAL_API_KEY")
        if api_key:
            st.success("✅ Mistral API OK")
        else:
            st.error("❌ MISTRAL_API_KEY manquante")
            st.stop()
        
        st.markdown("---")
        st.markdown("**🚀 Pipeline Optimisé:**")
        st.info("""
        1️⃣ **Python** extrait tags  
        ⚡ Gratuit & Instant  
          
        2️⃣ **IA** génère insights  
        💰 1 appel/client  
          
        3️⃣ **Dashboard** Looker  
        📊 Visualisations live
        """)
        
        st.markdown("---")
        st.markdown("**💰 Économie:**")
        st.metric("Coût/client", "0.002$", "-50%")
        st.metric("Vitesse", "~1.5s", "x2")
    
    # Tabs principales style "Google Studio"
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📂 Données & Tags", "📊 Vue Globale (Google Studio)", "🧠 Analyse Intelligente", "📥 Exports", "🎨 Studio Builder"])
    
    # ============================================================================
    # TAB 1: DONNÉES & TAGS
    # ============================================================================
    with tab1:
        st.header("1. Ingestion & Tagging Automatique")
        
        uploaded_file = st.file_uploader(
            "Importer un fichier CSV (Transcriptions)",
            type=["csv"],
            help="Le fichier doit contenir une colonne 'Transcription'"
        )
        
        if uploaded_file:
            # Réinitialiser si nouveau fichier
            uploaded_file_name = uploaded_file.name
            if "current_file" not in st.session_state or st.session_state["current_file"] != uploaded_file_name:
                st.session_state["current_file"] = uploaded_file_name
                if "results" in st.session_state:
                    del st.session_state["results"]
                if "results_df" in st.session_state:
                    del st.session_state["results_df"]
                if "source_df" in st.session_state:
                    del st.session_state["source_df"]
                if "date_col" in st.session_state:
                    del st.session_state["date_col"]
                st.toast(f"Fichier chargé : {uploaded_file_name}", icon="✅")
            
            try:
                # Lecture intelligente du CSV (détection séparateur)
                try:
                    df = pd.read_csv(uploaded_file, sep=None, engine='python')
                except:
                    # Fallback classique
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)
                
                st.info(f"Base de données chargée : {len(df)} clients")
                
                if "Transcription" not in df.columns:
                    st.error("❌ Colonne 'Transcription' manquante")
                    st.stop()

                st.session_state["source_df"] = df.copy()
                date_col = detect_date_column(df)
                st.session_state["date_col"] = date_col
                if date_col:
                    st.caption(f"Colonne date détectée : {date_col}")
                
                # Configuration rapide
                col1, col2 = st.columns([1, 2])
                with col1:
                    max_clients = st.number_input("Nombre de clients à analyser", 1, len(df), min(10, len(df)))
                # Boutons d'action séparés
                col_act1, col_act2 = st.columns(2)
                
                with col_act1:
                    # BOUTON 1 : SCAN PYTHON RAPIDE (Batch Processing)
                    if st.button("⚡ SCAN TURBO (Nettoyage + Tags)", type="primary", use_container_width=True, help="Instantané - Moteur Python"):
                        
                        # Traitement par lot instantané
                        scan_results = []
                        progress_bar = st.progress(0)
                        
                        total_rows = len(df)
                        # On traite TOUT le dataset ou la limite choisie par l'user ? 
                        # Pour "Turbo", on peut tout faire, c'est rapide. Limitons à max_clients pour cohérence.
                        rows_to_process = df.head(max_clients)
                        
                        for idx, row in rows_to_process.iterrows():
                            client_id = row.get("ID", f"CLIENT_{idx}")
                            raw_text = row.get("Transcription", "")
                            date_col = st.session_state.get("date_col")
                            source_date = parse_date_value(row.get(date_col)) if date_col else pd.NaT
                            safe_text = sanitize_display_text(raw_text)
                            
                            # Extraction 100% Python
                            tags = extract_all_tags(raw_text)
                            
                            # Structure de résultat préliminaire (sans IA)
                            scan_results.append({
                                "client_id": client_id,
                                "transcription_originale": (safe_text[:200] + "...") if len(safe_text) > 200 else safe_text,
                                "tags_extracted": tags,
                                "cleaned_text": tags["cleaned_text"],
                                "source_date": source_date,
                                # Champs IA vides pour l'instant
                                "resume_complet": "Analyse IA en attente...",
                                "segment_client": "À définir (IA)",
                                "urgency_score_final": tags["urgence_score"], # On prend le score Python par défaut
                                "insights_marketing": {},
                                "analyse_intelligente": {},
                                "objections_freins": []
                            })
                            progress_bar.progress((idx + 1) / max_clients)
                        
                        progress_bar.empty()
                        st.success(f"✅ {max_clients} clients scannés en < 1 seconde !")
                        
                        # Sauvegarde Session
                        st.session_state["results"] = scan_results
                        st.session_state["scan_done"] = True
                        st.session_state["ai_done"] = False # Reset AI status
                        st.rerun()

                with col_act2:
                    # BOUTON 2 : IA (Optionnel) - MODE BATCH RAPIDE
                    if st.button("🧠 AJOUTER L'INTELLIGENCE (Stratégie)", disabled=not st.session_state.get("scan_done"), use_container_width=True, help="Analyse par lots (5x plus rapide)"):
                        
                        client = init_mistral_client()
                        current_results = st.session_state["results"]
                        enriched_results = []
                        
                        # Batch configuration (Mode "MEGA PROMPT")
                        # On tente de tout envoyer d'un coup (jusqu'à 50 clients par appel pour sécurité context window)
                        BATCH_SIZE = 50 
                        total_clients = len(current_results)
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        st.toast(f"🚀 Mode Mega-Prompt activé : Traitement par paquets de {BATCH_SIZE} clients", icon="🚀")
                        
                        # Préparer les données pour le batch
                        # On a besoin de : client_id, text (clean), tags (python)
                        batch_queue = []
                        
                        start_time = datetime.now()
                        
                        for idx, res in enumerate(current_results):
                            batch_queue.append({
                                "client_id": res["client_id"],
                                "text": res["cleaned_text"],
                                "tags": res["tags_extracted"]
                            })
                            
                            # Si batch plein ou dernier élément
                            if len(batch_queue) == BATCH_SIZE or idx == total_clients - 1:
                                current_batch_num = (idx // BATCH_SIZE) + 1
                                total_batches = (total_clients + BATCH_SIZE - 1) // BATCH_SIZE
                                
                                status_text.text(f"🧠 Analyse IA en cours... Lot {current_batch_num}/{total_batches} ({len(batch_queue)} clients)")
                                
                                # Appel Batch
                                batch_results = analyze_batch(client, batch_queue)
                                
                                # Réconcilier les résultats
                                # On crée un dictionnaire rapide pour retrouver les résultats par ID
                                batch_results_map = {item['client_id']: item for item in batch_results}
                                
                                for original_item in batch_queue:
                                    c_id = original_item['client_id']
                                    # Retrouver l'item original complet dans current_results (pour garder les champs Python)
                                    # Note: optimisation possible, ici on fait simple
                                    full_original = next(r for r in current_results if r["client_id"] == c_id)
                                    
                                    if c_id in batch_results_map:
                                        # Fusionner resultats IA
                                        full_original.update(batch_results_map[c_id])
                                    else:
                                        # Fallback si l'IA a perdu un client en route (rare mais possible)
                                        full_original["resume_complet"] = "Erreur mapping IA"
                                    
                                    enriched_results.append(full_original)

                                batch_queue = [] # Reset batch
                                progress_bar.progress((idx + 1) / total_clients)
                        
                        execution_time = (datetime.now() - start_time).total_seconds()
                        progress_bar.empty()
                        status_text.success(f"✅ Analyse Stratégique Terminée en {execution_time:.1f}s !")
                        
                        st.session_state["results"] = enriched_results
                        st.session_state["ai_done"] = True
                        st.rerun()
                        
            except Exception as e:
                st.error(f"Erreur: {e}")

        # Affichage des tags Python (Données brutes)
        if "results" in st.session_state:
            st.markdown("---")
            st.subheader("🏷️ Tags Extraits (Moteur Python Turbo)")
            
            results = st.session_state["results"]
            
            # Vue tabulaire enrichie
            tags_data = []
            for r in results:
                t = r.get("tags_extracted", {})
                tags_data.append({
                    "ID": r["client_id"],
                    "Ville": t.get("ville"),
                    "Âge": t.get("age"),
                    "Budget": t.get("budget"),
                    "Urgence": f"{t.get('urgence_score')}/5",
                    "Motif": ", ".join(t.get("motif_achat", [])),
                    "Style": ", ".join(t.get("style", [])),
                    "Famille": ", ".join(t.get("famille", [])),
                    "Centres d'intérêt": ", ".join(t.get("centres_interet", []))
                })
            
            st.dataframe(pd.DataFrame(tags_data), use_container_width=True)

    # ============================================================================
    # TAB 2: VUE GLOBALE (GOOGLE STUDIO)
    # ============================================================================
    with tab2:
        if "results" not in st.session_state:
            st.info("Veuillez d'abord lancer le SCAN TURBO dans l'onglet 'Données & Tags'")
        else:
            st.header("📊 Vue d'Ensemble")
            results = st.session_state["results"]
            ai_done = st.session_state.get("ai_done", False)
            
            if not ai_done:
                st.warning("⚠️ Ces données sont basées uniquement sur le Scan Python (Tags). Lancez l'IA pour l'analyse stratégique complète.")

            st.subheader("Filtres Avancés")
            f1, f2, f3 = st.columns(3)
            if ai_done:
                segments_all = sorted({r.get("segment_client", "Inconnu") for r in results})
                segments_filter = f1.multiselect("Segment IA", segments_all, default=segments_all)
            else:
                f1.caption("Segment IA disponible après IA.")
                segments_filter = None
            urgent_only = f2.checkbox("Urgence ≥ 4", value=False)
            urgency_min = f3.slider("Urgence minimum", 1, 5, 1)

            filtered_results = []
            for r in results:
                if ai_done and segments_filter is not None and r.get("segment_client", "Inconnu") not in segments_filter:
                    continue
                if urgent_only and r.get("urgency_score_final", 1) < 4:
                    continue
                if r.get("urgency_score_final", 1) < urgency_min:
                    continue
                filtered_results.append(r)

            if not filtered_results:
                st.warning("Aucun client ne correspond aux filtres actuels.")
            else:
                view_mode = st.radio(
                    "Affichage",
                    ["Tableaux & Graphiques", "Clienteling (cartes)"],
                    horizontal=True
                )

                if view_mode == "Clienteling (cartes)":
                    st.subheader("Clienteling Mode")
                    cols = st.columns(2)
                    for i, r in enumerate(filtered_results):
                        with cols[i % 2]:
                            with st.container(border=True):
                                client_name = r.get("client_id", "Client")
                                segment = r.get("segment_client", "Scan Python")
                                budget = r.get("tags_extracted", {}).get("budget") or "N/A"
                                ice = sanitize_display_text(r.get("ice_breaker") or "")
                                ice_display = ice if ice else "—"
                                st.markdown(f"**{client_name}**")
                                st.caption(f"Statut: {segment}")
                                st.success(f"Ice-Breaker: {ice_display}")
                                st.write(f"Budget: {budget}")
                                st.write(f"Urgence: {r.get('urgency_score_final', 1)}/5")

                                cta1, cta2, cta3 = st.columns(3)
                                if cta1.button("WhatsApp", key=f"wa_{client_name}_{i}"):
                                    st.toast("Action WhatsApp (placeholder)", icon="📲")
                                if cta2.button("Email", key=f"em_{client_name}_{i}"):
                                    st.toast("Action Email (placeholder)", icon="✉️")
                                if cta3.button("Noter", key=f"note_{client_name}_{i}"):
                                    st.toast("Action Noter (placeholder)", icon="📝")
                else:
                    # KPIs style Google Analytics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Clients Analysés", len(filtered_results))
                
                # Urgence (vient de Python donc toujours dispo)
                avg_urgency = sum(r.get("urgency_score_final", 1) for r in filtered_results)/len(filtered_results) if filtered_results else 0
                col2.metric("Score Urgence Moyen", f"{avg_urgency:.1f}/5")
                
                high_urgency = sum(1 for r in filtered_results if r.get("urgency_score_final", 1) >= 4)
                col3.metric("Clients Haute Urgence", high_urgency)
                
                # Opportunités (vient de l'IA)
                if ai_done:
                    opps_count = sum(len(r.get("insights_marketing", {}).get("opportunites_vente", [])) for r in filtered_results)
                    col4.metric("Opportunités Identifiées", opps_count)
                else:
                    col4.metric("Opportunités", "En attente IA", help="Lancez l'IA pour calculer")
                
                st.markdown("---")
                
                # Graphiques principaux
                c1, c2 = st.columns(2)
                
                with c1:
                    st.subheader("Distribution Urgence")
                    urgency_counts = {}
                    for r in filtered_results:
                        u = r.get("urgency_score_final", 1)
                        urgency_counts[u] = urgency_counts.get(u, 0) + 1
                    
                    fig = px.bar(x=list(urgency_counts.keys()), y=list(urgency_counts.values()), 
                                 labels={'x': 'Score', 'y': 'Clients'}, color_discrete_sequence=['#4285F4'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                with c2:
                    # Segments : Vient de l'IA. Si pas IA, on affiche une répartition par ville ou autre tag Python
                    if ai_done:
                        st.subheader("Segments Clients (IA)")
                        segments = {}
                        for r in filtered_results:
                            s = r.get("segment_client", "Occasionnel")
                            segments[s] = segments.get(s, 0) + 1
                        fig = px.pie(names=list(segments.keys()), values=list(segments.values()), hole=0.4)
                    else:
                        st.subheader("Répartition Villes (Python)")
                        cities = {}
                        for r in filtered_results:
                            c = r.get("tags_extracted", {}).get("ville") or "Non détectée"
                            cities[c] = cities.get(c, 0) + 1
                        fig = px.pie(names=list(cities.keys()), values=list(cities.values()), hole=0.4)
                        
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.subheader("Analyse Temporelle")
                date_series = pd.to_datetime(
                    [r.get("source_date") for r in filtered_results],
                    errors="coerce"
                ).dropna()
                if not date_series.empty:
                    df_time = pd.DataFrame({"date": date_series})
                    df_time["week"] = df_time["date"].dt.to_period("W").dt.start_time
                    weekly = df_time.groupby("week").size().reset_index(name="nouveaux_clients")
                    fig = px.line(weekly, x="week", y="nouveaux_clients", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune colonne de date exploitable pour la tendance.")

    # ============================================================================
    # TAB 3: ANALYSE INTELLIGENTE (IA)
    # ============================================================================
    with tab3:
        ai_done = st.session_state.get("ai_done", False)
        
        if "results" not in st.session_state:
             st.info("Veuillez d'abord lancer le SCAN TURBO.")
        elif not ai_done:
            st.info("👋 **L'intelligence est en veille.**")
            st.markdown("""
            Vous consultez actuellement les données brutes (Tags Python).
            
            Pour obtenir :
            - ✨ Les suggestions de nouveaux tags
            - 🚀 Les stratégies marketing avancées
            - 📝 Les résumés narratifs
            
            👉 **Cliquez sur '🧠 AJOUTER L'INTELLIGENCE' dans l'onglet 1.**
            """)
        else:
            st.header("🧠 Analyse Intelligente & Stratégie")
            st.markdown("*L'IA agit ici comme un consultant senior pour recommander des évolutions.*")
            
            results = st.session_state["results"]
            
            # 1. Suggestions de Nouveaux Tags
            st.subheader("✨ Suggestions de Nouveaux Tags")
            st.info("L'IA a détecté ces concepts récurrents qui manquent à votre taxonomie actuelle :")
            
            all_new_tags = []
            for r in results:
                all_new_tags.extend(r.get("analyse_intelligente", {}).get("nouveaux_tags_suggeres", []))
            
            if all_new_tags:
                from collections import Counter
                new_tags_count = Counter(all_new_tags).most_common(10)
                
                cols = st.columns(3)
                for i, (tag, count) in enumerate(new_tags_count):
                    with cols[i % 3]:
                        st.metric(label=f"Suggestion #{i+1}", value=tag, help=f"Mentionné {count} fois")
            else:
                st.markdown("Aucune suggestion majeure détectée sur cet échantillon.")

            st.markdown("---")
            
            # 2. Avancées Stratégiques
            st.subheader("🚀 Avancées Stratégiques Marketing")
            
            all_strategies = []
            for r in results:
                all_strategies.extend(r.get("analyse_intelligente", {}).get("strategie_avancee", []))
            
            if all_strategies:
                # Afficher quelques stratégies phares (aléatoire ou premières)
                seen = set()
                unique_strategies = [x for x in all_strategies if not (x in seen or seen.add(x))][:5]
                
                for i, strat in enumerate(unique_strategies, 1):
                    st.success(f"**Stratégie {i}:** {strat}")
            
            st.markdown("---")
            
            # 3. Focus Client Détaillé (avec Insights IA)
            st.subheader("🔍 Focus Client & Recommandations")
            selected_client = st.selectbox("Sélectionner un client pour voir l'analyse détaillée", 
                                         [r["client_id"] for r in results])
            
            client_data = next(r for r in results if r["client_id"] == selected_client)
            
            c1, c2 = st.columns(2)
            with c1:
                # ICE BREAKER ZONE (New P0)
                if client_data.get("ice_breaker"):
                    ice_text = sanitize_display_text(client_data.get("ice_breaker", ""))
                    st.success(f"🗣️ **Ice-Breaker IA:** \"{ice_text}\"")
                
                st.markdown("**📝 Résumé Narratif**")
                st.write(client_data.get("resume_complet"))
                
                st.markdown("**⚠️ Objections / Freins**")
                for obj in client_data.get("objections_freins", []):
                    st.write(f"- {obj}")
            
            with c2:
                st.markdown("**💡 Recommandations IA**")
                insights = client_data.get("insights_marketing", {})
                if insights.get("produits_recommandes"):
                    st.write("**Produits:** " + ", ".join(insights["produits_recommandes"]))
                if insights.get("actions_suggerees"):
                    st.write("**Actions:** " + ", ".join(insights["actions_suggerees"]))
                if client_data.get("analyse_intelligente", {}).get("strategie_avancee"):
                     st.write("**Stratégie Spécifique:** " + ", ".join(client_data["analyse_intelligente"]["strategie_avancee"]))

    # ============================================================================
    # TAB 4: EXPORTS
    # ============================================================================
    with tab4:
        if "results" in st.session_state:
            st.header("📥 Exports Données")
            export_df = build_export_dataframe(st.session_state["results"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Excel Complet")
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    export_df.to_excel(writer, index=False, sheet_name="clients")
                output.seek(0)
                st.download_button(
                    "Télécharger Excel",
                    data=output,
                    file_name=f"clients_enrichis_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                st.subheader("CSV Looker Studio")
                csv_data = export_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Télécharger CSV",
                    data=csv_data,
                    file_name=f"clients_enrichis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Veuillez d'abord lancer le SCAN TURBO dans l'onglet 'Données & Tags'")

    # ============================================================================
    # TAB 5: STUDIO BUILDER
    # ============================================================================
    with tab5:
        if "results" not in st.session_state:
            st.info("Veuillez d'abord lancer le SCAN TURBO dans l'onglet 'Données & Tags'")
        else:
            st.header("🎨 Studio Builder - Créez vos Graphiques")
            st.markdown("*Construisez vos propres visualisations en sélectionnant les dimensions et métriques*")
            
            results = st.session_state["results"]
            available_fields = get_available_fields(results)
            
            # Flatten fields for selection
            all_fields = []
            field_categories = {}
            for category, fields in available_fields.items():
                for field in fields:
                    all_fields.append(field)
                    field_categories[field] = category
            
            if not all_fields:
                st.warning("Aucun champ disponible. Assurez-vous d'avoir des données analysées.")
            else:
                # Configuration Panel
                st.subheader("⚙️ Configuration du Graphique")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    chart_type = st.selectbox(
                        "Type de graphique",
                        ["bar", "pie", "line", "scatter"],
                        format_func=lambda x: {
                            "bar": "📊 Barres",
                            "pie": "🥧 Camembert",
                            "line": "📈 Ligne",
                            "scatter": "🔵 Nuage de points"
                        }[x]
                    )
                
                with col2:
                    x_field = st.selectbox(
                        "Dimension (Axe X)",
                        all_fields,
                        format_func=lambda x: f"{x} ({field_categories[x]})"
                    )
                
                with col3:
                    if chart_type == "scatter":
                        y_field = st.selectbox(
                            "Métrique (Axe Y)",
                            [f for f in all_fields if f in ["urgency_score_final", "urgence_score"]],
                            help="Pour scatter plot, sélectionnez une métrique numérique"
                        )
                    else:
                        y_field = None
                        st.caption("Métrique: Count (automatique)")
                
                # Filters Panel
                st.markdown("---")
                st.subheader("🔍 Filtres")
                
                filter_col1, filter_col2 = st.columns(2)
                
                filters = {}
                
                with filter_col1:
                    urgency_filter = st.slider(
                        "Urgence minimum",
                        1, 5, 1,
                        help="Filtrer par score d'urgence"
                    )
                    if urgency_filter > 1:
                        filters["urgency_min"] = urgency_filter
                
                with filter_col2:
                    # Segment filter (if AI done)
                    if "segment_client" in all_fields:
                        all_segments = sorted({r.get("segment_client", "Inconnu") for r in results})
                        segment_filter = st.multiselect(
                            "Segments IA",
                            all_segments,
                            default=all_segments
                        )
                        if segment_filter != all_segments:
                            filters["segments"] = segment_filter
                
                # Generate Chart
                st.markdown("---")
                st.subheader("📊 Visualisation")
                
                if st.button("🚀 Générer le Graphique", type="primary", use_container_width=True):
                    with st.spinner("Génération en cours..."):
                        chart_data = prepare_chart_data(
                            results,
                            x_field,
                            y_field,
                            chart_type,
                            filters
                        )
                        
                        if not chart_data:
                            st.warning("Aucune donnée disponible avec ces filtres.")
                        else:
                            fig = create_custom_chart(
                                chart_data,
                                chart_type,
                                x_field,
                                y_field if y_field else "Count"
                            )
                            
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Data table
                                with st.expander("📋 Voir les données"):
                                    st.dataframe(pd.DataFrame(chart_data), use_container_width=True)
                                
                                # Export options
                                st.markdown("---")
                                st.subheader("💾 Export")
                                
                                export_col1, export_col2 = st.columns(2)
                                
                                with export_col1:
                                    # Export chart as HTML (Plotly interactive)
                                    chart_html = fig.to_html()
                                    st.download_button(
                                        "📊 Télécharger Graphique (HTML)",
                                        data=chart_html,
                                        file_name=f"chart_{x_field}_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                                        mime="text/html"
                                    )
                                
                                with export_col2:
                                    # Export data as CSV
                                    csv_export = pd.DataFrame(chart_data).to_csv(index=False).encode("utf-8")
                                    st.download_button(
                                        "📥 Télécharger Données (CSV)",
                                        data=csv_export,
                                        file_name=f"data_{x_field}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                        mime="text/csv"
                                    )
                            else:
                                st.error("Erreur lors de la génération du graphique.")
                
                # Quick Tips
                st.markdown("---")
                with st.expander("💡 Conseils d'utilisation"):
                    st.markdown("""
                    **Exemples de visualisations utiles:**
                    
                    - **Distribution géographique**: Barres avec `ville` en X
                    - **Répartition budgets**: Camembert avec `budget` en X
                    - **Évolution urgence**: Ligne avec `urgency_score_final` en X
                    - **Corrélation âge/urgence**: Scatter avec `age` en X et `urgency_score_final` en Y
                    - **Segments clients**: Camembert avec `segment_client` en X (après analyse IA)
                    
                    **Astuces:**
                    - Utilisez les filtres pour zoomer sur des sous-groupes
                    - Exportez en HTML pour garder l'interactivité
                    - Combinez plusieurs graphiques en exportant les données CSV
                    """)



if __name__ == "__main__":
    main()
