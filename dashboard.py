"""
LVMH Client Analytics - Dashboard Complet
Version professionnelle avec toutes les fonctionnalités
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.profile_generator import ProfileGenerator
from src.csv_processor import CSVProcessor
from collections import Counter
from datetime import datetime
from pathlib import Path
import hashlib
import re
import json

# Import Mistral
try:
    from src.mistral_analyzer import MistralAnalyzer
    MISTRAL_OK = True
except:
    MISTRAL_OK = False

# Config
st.set_page_config(
    page_title="LVMH Client Analytics",
    page_icon="◆",
    layout="wide"
)

# CSS - Palette Beige/Marron sobre
st.markdown("""
<style>
    /* === BASE === */
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 100%;
        background: #FAF8F5;
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    /* Textes */
    h1, h2, h3, p, span, div, label {
        color: #1a1a1a !important;
    }
    
    /* Header */
    .main-header {
        background: #1a1a1a;
        color: #FAF8F5 !important;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    
    .main-header h1 {
        color: #FAF8F5 !important;
        font-size: 1.8rem;
        margin: 0;
    }
    
    .main-header p {
        color: #A39E98 !important;
        margin: 0.3rem 0 0 0;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: #F5F0EB;
        border: 1px solid #D4CFC9;
        border-radius: 10px;
        padding: 1rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #F5F0EB;
        border-radius: 10px;
        padding: 0.4rem;
        gap: 0.3rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        color: #666666 !important;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FAF8F5 !important;
        color: #1a1a1a !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Cards */
    .info-card {
        background: #F5F0EB;
        border: 1px solid #D4CFC9;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .info-card h4 {
        color: #8B4513 !important;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #F5F0EB !important;
        color: #1a1a1a !important;
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #8B4513 !important;
        color: #FAF8F5 !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: #6B4423 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: #F5F0EB;
        border-color: #D4CFC9;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #D4CFC9;
        border-radius: 8px;
    }
    
    /* Alerts */
    .stAlert {
        background: #F5F0EB !important;
        border: 1px solid #D4CFC9;
        color: #1a1a1a !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1a1a1a;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #FAF8F5 !important;
    }
</style>
""", unsafe_allow_html=True)

# Couleurs graphiques
COLORS = ['#8B4513', '#A0522D', '#D2691E', '#CD853F', '#DEB887']

@st.cache_data
def load_kpis_stats():
    """Charge KPIs et stats via SQL (scalable)."""
    pg = ProfileGenerator()
    return pg.get_kpis_sql(), pg.get_stats_sql()

@st.cache_data
def load_conversations():
    """Charge les conversations (optionnel)."""
    try:
        csv = CSVProcessor("LVMH_Realistic_Merged_CA001-100.csv")
        return csv.get_conversations()
    except:
        return []

def build_time_series(conversations):
    if not conversations:
        return pd.DataFrame(), pd.DataFrame()
    df = pd.DataFrame(conversations)
    if "date" not in df.columns:
        return pd.DataFrame(), pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["date"])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df["week"] = df["date"].dt.to_period("W").dt.start_time
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    weekly = df.groupby("week").size().reset_index(name="new_clients")
    monthly = df.groupby("month").size().reset_index(name="new_clients")
    return weekly, monthly

def calculate_kpis(profiles):
    """Calcule tous les KPIs"""
    total = len(profiles)
    
    # Segments
    segments = Counter([p.get('identite', {}).get('statut_relationnel', 'N/A') for p in profiles])
    
    # Budgets
    budgets = Counter([p.get('projet_achat', {}).get('budget', 'N/A') for p in profiles])
    budget_values = {'<5k': 3000, '5-10k': 7500, '10-15k': 12500, '15-25k': 20000, '25k+': 35000}
    pipeline = sum(budget_values.get(p.get('projet_achat', {}).get('budget', '<5k'), 3000) for p in profiles)
    
    # Démographie
    genres = Counter([p.get('identite', {}).get('genre', 'N/A') for p in profiles])
    ages = Counter([p.get('identite', {}).get('age', 'N/A') for p in profiles])
    
    return {
        'total': total,
        'segments': dict(segments),
        'budgets': dict(budgets),
        'pipeline': pipeline,
        'avg_basket': pipeline / total if total > 0 else 0,
        'genres': dict(genres),
        'ages': dict(ages),
        'vip_count': segments.get('VIP', 0),
        'vip_pct': segments.get('VIP', 0) / total * 100 if total > 0 else 0,
        'high_value': budgets.get('25k+', 0) + budgets.get('15-25k', 0)
    }

def get_client_badges(profile):
    """Extrait tous les badges/tags d'un profil"""
    badges = []
    
    # Identité
    if profile.get('identite', {}).get('statut_relationnel'):
        badges.append({'text': profile['identite']['statut_relationnel'], 'type': 'statut'})
    
    # Localisation
    loc = profile.get('localisation', {})
    for region, villes in loc.items():
        if isinstance(villes, list):
            for ville in villes:
                badges.append({'text': ville, 'type': 'loc'})
    
    # Lifestyle
    lifestyle = profile.get('lifestyle_centres_interet', {})
    for cat, content in lifestyle.items():
        if isinstance(content, dict):
            for subcat, items in content.items():
                if isinstance(items, list):
                    for item in items:
                        badges.append({'text': item, 'type': 'lifestyle'})
        elif isinstance(content, list):
            for item in content:
                badges.append({'text': item, 'type': 'lifestyle'})
                
    # Style
    style = profile.get('style_personnel', {})
    for key in ['couleurs_preferees', 'matieres_preferees', 'pieces_favorites']:
        if key in style and isinstance(style[key], list):
            for item in style[key]:
                badges.append({'text': item, 'type': 'style'})
                
    # Mobilité
    mobilite = profile.get('mobilite_rythme_vie', {}).get('frequence_deplacement')
    if mobilite:
        badges.append({'text': mobilite, 'type': 'mobilite'})
        
    return badges

def generate_ice_breaker(profile):
    """Genere une phrase d'accroche simple a partir du profil."""
    identite = profile.get('identite', {})
    projet = profile.get('projet_achat', {})
    style = profile.get('style_personnel', {})
    metadata = profile.get('metadata', {})

    pieces = projet.get('pieces_cibles', [])
    motif = projet.get('motif', '')
    couleurs = style.get('couleurs_preferees', [])
    date_conv = metadata.get('date_conversation', '')

    if motif:
        return f"Revenir sur le motif mentionne ({motif}) et verifier si le besoin est toujours d'actualite."
    if pieces:
        return f"Demander si la piece ciblee ({pieces[0]}) est toujours prioritaire."
    if couleurs:
        return f"Proposer des nouveautes dans la couleur {couleurs[0]}."
    if date_conv:
        return "Demander si les attentes ont evolue depuis la derniere visite."
    return "Engager la conversation sur ses dernieres envies ou projets."

def next_best_action(profile):
    """Retourne une action recommande et sa justification."""
    statut = profile.get('identite', {}).get('statut_relationnel', '')
    budget = profile.get('projet_achat', {}).get('budget', '')
    regime = profile.get('metadata_client', {}).get('regime_alimentaire', '')
    pieces = profile.get('projet_achat', {}).get('pieces_cibles', [])

    if statut == 'VIP' and budget in ['15-25k', '25k+']:
        return ("Proposer un RDV prive en boutique", "Client VIP a fort potentiel.")
    if regime in ['Vegan', 'Végane', 'Vegetarien', 'Végétarien']:
        return ("Mettre en avant les collections responsables", "Sensibilite RSE detectee.")
    if pieces:
        return (f"Suggere une piece complementaire a {pieces[0]}", "Interet produit explicite.")
    return ("Programmer un suivi a J+7", "Maintenir l'engagement.")

def get_product_image(profile):
    """Retourne une image produit si disponible (URL ou asset local)."""
    projet = profile.get("projet_achat", {})
    url = projet.get("product_image_url") or profile.get("product_image_url")
    if url:
        return url
    pieces = projet.get("pieces_cibles", [])
    if not pieces:
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", pieces[0].lower()).strip("-")
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        p = Path("assets") / "products" / f"{slug}{ext}"
        if p.exists():
            return str(p)
    return None

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def get_contact_info(client_id, show_simulated=True):
    if not show_simulated:
        return "", ""
    h = hashlib.md5(client_id.encode("utf-8")).hexdigest()
    suffix = int(h[:4], 16) % 1000
    email = f"{client_id.lower()}_{suffix}@lvmh-client.test"
    phone = f"+33 6 {h[4:6]} {h[6:8]} {h[8:10]} {h[10:12]}"
    return email, phone

def assign_seller(client_id):
    """Attribution deterministe d'un vendeur (simulation)."""
    sellers = ["Camille", "Lucas", "Ines", "Noah", "Sarah", "Lina"]
    h = hashlib.md5(client_id.encode("utf-8")).hexdigest()
    idx = int(h[:2], 16) % len(sellers)
    return sellers[idx]

def build_team_metrics_from_counts(total: int, vip_count: int, high_value: int):
    """Construit des KPIs par vendeur (simulation) sans charger tous les profils."""
    sellers = ["Camille", "Lucas", "Ines", "Noah", "Sarah", "Lina"]
    weights = []
    for s in sellers:
        w = int(hashlib.md5(s.encode("utf-8")).hexdigest()[:2], 16) + 1
        weights.append(w)
    total_w = sum(weights)

    def distribute(value):
        raw = [int(value * w / total_w) for w in weights]
        # Ajuster pour respecter la somme
        diff = value - sum(raw)
        i = 0
        while diff > 0:
            raw[i % len(raw)] += 1
            diff -= 1
            i += 1
        return raw

    profiles_counts = distribute(total)
    vip_counts = distribute(vip_count)
    high_counts = distribute(high_value)

    team = {}
    for i, s in enumerate(sellers):
        team[s] = {
            "profiles": profiles_counts[i],
            "vip": vip_counts[i],
            "high_value": high_counts[i]
        }
    return team

def build_tag_trends_from_sql(pg, top_n=20):
    """Construit une liste de tags frequents (tendance) via SQL."""
    rows = pg.get_top_tags(top_n)
    return [(r["tag"], r["count"]) for r in rows]

def parse_segment_query(query):
    """Parse une requete simple de segmentation en criteres."""
    q = query.lower()
    criteria = {"statut": None, "budget": None, "budget_any": None, "city": None, "color": None, "tag_any": []}
    if "vip" in q:
        criteria["statut"] = "VIP"
    elif "fidele" in q:
        criteria["statut"] = "Fidèle"
    elif "nouveau" in q:
        criteria["statut"] = "Nouveau"

    if "plus de 10k" in q or ">=10k" in q or "sup a 10k" in q:
        criteria["budget_any"] = ["10-15k", "15-25k", "25k+"]
    elif "25k" in q:
        criteria["budget"] = "25k+"
    elif "15-25" in q or "15k" in q:
        criteria["budget"] = "15-25k"
    elif "10-15" in q or "10k" in q:
        criteria["budget"] = "10-15k"
    elif "5-10" in q or "5k" in q:
        criteria["budget"] = "5-10k"

    m_city = re.search(r"(paris|milan|london|madrid|berlin|tokyo|dubai|hong_kong|singapore|new_york)", q)
    if m_city:
        criteria["city"] = m_city.group(1).replace("_", " ").title()

    color_map = {
        "Rouge": ["rouge", "red", "vermillon", "bordeaux"],
        "Beige": ["beige", "sable", "taupe"],
        "Noir": ["noir", "black", "ebene"],
        "Blanc": ["blanc", "white", "ivoire"],
        "Bleu": ["bleu", "blue", "marine", "azur"],
        "Vert": ["vert", "green", "kaki"],
        "Marron": ["marron", "brun", "chocolat"],
        "Camel": ["camel"],
        "Or": ["or", "gold", "dore"]
    }
    for canonical, variants in color_map.items():
        if any(v in q for v in variants):
            criteria["color"] = canonical
            break

    if "cuir vegan" in q or "vegan leather" in q:
        criteria["tag_any"].append("Cuir Vegan")
    if "durable" in q or "durabilite" in q or "responsable" in q:
        criteria["tag_any"].append("Durabilite")

    return criteria

def filter_profiles_with_query(profiles, query):
    criteria = parse_segment_query(query)
    filtered = profiles
    if criteria["statut"]:
        filtered = [p for p in filtered if p.get("identite", {}).get("statut_relationnel") == criteria["statut"]]
    if criteria["budget"]:
        filtered = [p for p in filtered if p.get("projet_achat", {}).get("budget") == criteria["budget"]]
    if criteria["budget_any"]:
        filtered = [p for p in filtered if p.get("projet_achat", {}).get("budget") in criteria["budget_any"]]
    if criteria["city"]:
        filtered = [p for p in filtered if criteria["city"] in sum(p.get("localisation", {}).values(), [])]
    if criteria["color"]:
        filtered = [p for p in filtered if criteria["color"] in p.get("style_personnel", {}).get("couleurs_preferees", [])]
    if criteria["tag_any"]:
        wanted = set([t.lower() for t in criteria["tag_any"]])
        def has_tag(p):
            tags = set([b["text"].lower() for b in get_client_badges(p)])
            return any(t in tags for t in wanted)
        filtered = [p for p in filtered if has_tag(p)]
    return filtered

def next_best_action(profile):
    """Retourne une action recommande et sa justification."""
    statut = profile.get('identite', {}).get('statut_relationnel', '')
    budget = profile.get('projet_achat', {}).get('budget', '')
    regime = profile.get('metadata_client', {}).get('regime_alimentaire', '')
    pieces = profile.get('projet_achat', {}).get('pieces_cibles', [])

    if statut == 'VIP' and budget in ['15-25k', '25k+']:
        return ("Proposer un RDV prive en boutique", "Client VIP a fort potentiel.")
    if regime in ['Vegan', 'Végane', 'Vegetarien', 'Végétarien']:
        return ("Mettre en avant les collections responsables", "Sensibilite RSE detectee.")
    if pieces:
        return (f"Suggere une piece complementaire a {pieces[0]}", "Interet produit explicite.")
    return ("Programmer un suivi a J+7", "Maintenir l'engagement.")

def get_product_image(profile):
    """Retourne une image produit si disponible (URL ou asset local)."""
    projet = profile.get("projet_achat", {})
    url = projet.get("product_image_url") or profile.get("product_image_url")
    if url:
        return url
    pieces = projet.get("pieces_cibles", [])
    if not pieces:
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", pieces[0].lower()).strip("-")
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        p = Path("assets") / "products" / f"{slug}{ext}"
        if p.exists():
            return str(p)
    return None

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def get_contact_info(client_id, show_simulated=True):
    if not show_simulated:
        return "", ""
    h = hashlib.md5(client_id.encode("utf-8")).hexdigest()
    suffix = int(h[:4], 16) % 1000
    email = f"{client_id.lower()}_{suffix}@lvmh-client.test"
    phone = f"+33 6 {h[4:6]} {h[6:8]} {h[8:10]} {h[10:12]}"
    return email, phone

def assign_seller(client_id):
    """Attribution deterministe d'un vendeur (simulation)."""
    sellers = ["Camille", "Lucas", "Ines", "Noah", "Sarah", "Lina"]
    h = hashlib.md5(client_id.encode("utf-8")).hexdigest()
    idx = int(h[:2], 16) % len(sellers)
    return sellers[idx]

def build_team_metrics_from_counts(total: int, vip_count: int, high_value: int):
    """Construit des KPIs par vendeur (simulation) sans charger tous les profils."""
    sellers = ["Camille", "Lucas", "Ines", "Noah", "Sarah", "Lina"]
    weights = []
    for s in sellers:
        w = int(hashlib.md5(s.encode("utf-8")).hexdigest()[:2], 16) + 1
        weights.append(w)
    total_w = sum(weights)

    def distribute(value):
        raw = [int(value * w / total_w) for w in weights]
        # Ajuster pour respecter la somme
        diff = value - sum(raw)
        i = 0
        while diff > 0:
            raw[i % len(raw)] += 1
            diff -= 1
            i += 1
        return raw

    profiles_counts = distribute(total)
    vip_counts = distribute(vip_count)
    high_counts = distribute(high_value)

    team = {}
    for i, s in enumerate(sellers):
        team[s] = {
            "profiles": profiles_counts[i],
            "vip": vip_counts[i],
            "high_value": high_counts[i]
        }
    return team

def build_tag_trends_from_sql(pg, top_n=20):
    """Construit une liste de tags frequents (tendance) via SQL."""
    rows = pg.get_top_tags(top_n)
    return [(r["tag"], r["count"]) for r in rows]

def parse_segment_query(query):
    """Parse une requete simple de segmentation en criteres."""
    q = query.lower()
    criteria = {"statut": None, "budget": None, "budget_any": None, "city": None, "color": None, "tag_any": []}
    if "vip" in q:
        criteria["statut"] = "VIP"
    elif "fidele" in q:
        criteria["statut"] = "Fidèle"
    elif "nouveau" in q:
        criteria["statut"] = "Nouveau"

    if "plus de 10k" in q or ">=10k" in q or "sup a 10k" in q:
        criteria["budget_any"] = ["10-15k", "15-25k", "25k+"]
    elif "25k" in q:
        criteria["budget"] = "25k+"
    elif "15-25" in q or "15k" in q:
        criteria["budget"] = "15-25k"
    elif "10-15" in q or "10k" in q:
        criteria["budget"] = "10-15k"
    elif "5-10" in q or "5k" in q:
        criteria["budget"] = "5-10k"

    m_city = re.search(r"(paris|milan|london|madrid|berlin|tokyo|dubai|hong_kong|singapore|new_york)", q)
    if m_city:
        criteria["city"] = m_city.group(1).replace("_", " ").title()

    color_map = {
        "Rouge": ["rouge", "red", "vermillon", "bordeaux"],
        "Beige": ["beige", "sable", "taupe"],
        "Noir": ["noir", "black", "ebene"],
        "Blanc": ["blanc", "white", "ivoire"],
        "Bleu": ["bleu", "blue", "marine", "azur"],
        "Vert": ["vert", "green", "kaki"],
        "Marron": ["marron", "brun", "chocolat"],
        "Camel": ["camel"],
        "Or": ["or", "gold", "dore"]
    }
    for canonical, variants in color_map.items():
        if any(v in q for v in variants):
            criteria["color"] = canonical
            break

    if "cuir vegan" in q or "vegan leather" in q:
        criteria["tag_any"].append("Cuir Vegan")
    if "durable" in q or "durabilite" in q or "responsable" in q:
        criteria["tag_any"].append("Durabilite")

    return criteria

def filter_profiles_with_query(profiles, query):
    criteria = parse_segment_query(query)
    filtered = profiles
    if criteria["statut"]:
        filtered = [p for p in filtered if p.get("identite", {}).get("statut_relationnel") == criteria["statut"]]
    if criteria["budget"]:
        filtered = [p for p in filtered if p.get("projet_achat", {}).get("budget") == criteria["budget"]]
    if criteria["budget_any"]:
        filtered = [p for p in filtered if p.get("projet_achat", {}).get("budget") in criteria["budget_any"]]
    if criteria["city"]:
        filtered = [p for p in filtered if criteria["city"] in sum(p.get("localisation", {}).values(), [])]
    if criteria["color"]:
        filtered = [p for p in filtered if criteria["color"] in p.get("style_personnel", {}).get("couleurs_preferees", [])]
    if criteria["tag_any"]:
        wanted = set([t.lower() for t in criteria["tag_any"]])
        def has_tag(p):
            tags = set([b["text"].lower() for b in get_client_badges(p)])
            return any(t in tags for t in wanted)
        filtered = [p for p in filtered if has_tag(p)]
    return filtered

def main():
    # Charger les données
    pg = ProfileGenerator()
    kpis, stats = load_kpis_stats()
    conversations = load_conversations()

    # Sidebar options
    with st.sidebar:
        st.header("Options")
        mode_admin = st.toggle("Mode Admin (Technique)", value=False)
        mode_clienteling = st.toggle("Mode clienteling (iPad)", value=False)
        show_simulated = st.toggle("Afficher donnees simulees", value=True)
        st.caption("Mode Admin affiche les onglets techniques (IA, Data, Equipe).")
    
    # === HEADER ===
    st.markdown("""
    <div class="main-header">
        <h1>LVMH Client Analytics</h1>
        <p>Dashboard Marketing - {} clients - {}</p>
    </div>
    """.format(kpis['total'], datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)
    
    # === KPIs PRINCIPAUX ===
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Clients", kpis['total'])
    with col2:
        st.metric("Clients VIP", kpis['vip_count'], f"{kpis['vip_pct']:.0f}%")
    with col3:
        st.metric("Pipeline Total", f"{kpis['pipeline']/1000:.0f}K€")
    with col4:
        st.metric("Panier Moyen", f"{kpis['avg_basket']:,.0f}€")
    with col5:
        st.metric("High Value (15K+)", kpis['high_value'])
    
    st.markdown("---")
    
    # === ONGLETS PRINCIPAUX ===
    # Définition dynamique des onglets
    tabs_def = [
        ("Vue d'ensemble", True),
        ("Clients", True),
        ("Actions", True),
        ("Analyses", True),
        ("IA Mistral", mode_admin),
        ("Equipe & Tendances", mode_admin),
        ("Data & Ops", mode_admin)
    ]
    active_tabs_names = [t[0] for t in tabs_def if t[1]]
    tabs_list = st.tabs(active_tabs_names)
    tabs = {name: tab for name, tab in zip(active_tabs_names, tabs_list)}
    
    # ===== TAB 1: VUE D'ENSEMBLE =====
    if "Vue d'ensemble" in tabs:
        with tabs["Vue d'ensemble"]:
            st.markdown("### 🎯 Tableau de Bord Simplifié")
            
            # 3 Chiffres Clés (Calculés)
            nouveaux = kpis['segments'].get('Nouveau', 0)
            vip = kpis['vip_count']
            to_contact = kpis['total'] # Par défaut
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <h2 style="font-size: 3rem; margin:0;">{to_contact}</h2>
                    <p>CLIENTS TOTAL</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <h2 style="font-size: 3rem; margin:0;">{nouveaux}</h2>
                    <p>NOUVEAUX</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <h2 style="font-size: 3rem; margin:0;">{vip}</h2>
                    <p>VIP</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.info("💡 Sélectionnez l'onglet 'Clients' pour filtrer et contacter.")

    # ===== TAB 2: CLIENTS =====
    if "Clients" in tabs:
        with tabs["Clients"]:
            st.subheader("Base Clients")
            
            # Filtres
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_statut = st.multiselect("Filtrer par statut", list(kpis['segments'].keys()))
            with col2:
                filter_budget = st.multiselect("Filtrer par budget", ['<5k', '5-10k', '10-15k', '15-25k', '25k+'])
            with col3:
                search = st.text_input("Rechercher (ID)")
            
            # Filtrer les profils
            total_filtered = pg.count_clients(filter_statut, filter_budget, search)
            page_size = 10 if mode_clienteling else 20
            total_pages = max(1, (total_filtered + page_size - 1) // page_size)
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
            offset = (page - 1) * page_size
            client_ids = pg.get_client_ids_page(filter_statut, filter_budget, search, limit=page_size, offset=offset)
            profiles_page = pg.get_profiles_by_ids(client_ids)

            st.info(f"**{total_filtered}** clients affiches (page {page}/{total_pages})")
            
            # === Feature: Copy Actions ===
            if profiles_page:
                emails_to_copy = []
                for p in profiles_page:
                    eid, _ = get_contact_info(p.get('client_id', ''), show_simulated)
                    if eid: emails_to_copy.append(eid)
                
                with st.expander("📋 Copier les emails (Presse-papiers)", expanded=False):
                    st.markdown("Cliquer pour copier la liste des emails pour Outlook :")
                    st.code("; ".join(emails_to_copy), language="text")
            # =============================
            
            if mode_clienteling:
                st.subheader("Vue clienteling")
                for p in profiles_page:
                    ice = generate_ice_breaker(p)
                    action, reason = next_best_action(p)
                    image = get_product_image(p)
                    if image:
                        st.image(image, width=160)
                    st.markdown(f"""
                    <div class=\"info-card\">
                        <h4>{p.get('client_id', 'Client')}</h4>
                        <div><b>Statut:</b> {p.get('identite', {}).get('statut_relationnel', 'N/A')} | <b>Budget:</b> {p.get('projet_achat', {}).get('budget', 'N/A')}</div>
                        <div><b>Couleurs:</b> {', '.join(p.get('style_personnel', {}).get('couleurs_preferees', [])[:3]) or 'N/A'}</div>
                        <div><b>A dire aujourd'hui:</b> {ice}</div>
                        <div><b>Next Best Action:</b> {action} <span style=\"color:#666\">({reason})</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption(f"Page {page}/{total_pages} - {total_filtered} clients au total")
            else:
                client_data = []
                for p in profiles_page:
                    email, phone = get_contact_info(p.get('client_id', ''), show_simulated)
                    client_data.append({
                        'ID': p.get('client_id', 'N/A'),
                        'Genre': p.get('identite', {}).get('genre', 'N/A'),
                        'Age': p.get('identite', {}).get('age', 'N/A'),
                        'Statut': p.get('identite', {}).get('statut_relationnel', 'N/A'),
                        'Budget': p.get('projet_achat', {}).get('budget', 'N/A'),
                        'Couleurs': ', '.join(p.get('style_personnel', {}).get('couleurs_preferees', [])[:2]),
                        'Profession': p.get('identite', {}).get('profession', 'N/A'),
                        'Email': email,
                        'Tel': phone
                    })
                if client_data:
                    df = pd.DataFrame(client_data)
                    st.dataframe(df, use_container_width=True, height=400)
                    filters_label = "all"
                    if filter_statut or filter_budget or search:
                        filters_label = "filtered"
                    filename = f"clients_{filters_label}_{total_filtered}_{datetime.now().strftime('%Y%m%d')}.csv"
                    st.download_button("Exporter CSV", df.to_csv(index=False).encode("utf-8"), filename, "text/csv")

            # Détail client
            st.subheader("Détail Client")
            selected_id = st.text_input("ID client")
            
            if selected_id:
                profile = pg.get_profile(selected_id)
                if profile:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("**Identité**")
                        st.write(f"- Genre: {profile.get('identite', {}).get('genre', 'N/A')}")
                        st.write(f"- Statut: {profile.get('identite', {}).get('statut_relationnel', 'N/A')}")
                    with col2:
                        st.write("**Préférences**")
                        colors = profile.get('style_personnel', {}).get('couleurs_preferees', [])
                        st.write(f"- Couleurs: {', '.join(colors) if colors else 'N/A'}")
                    with col3:
                        st.write("**Projet**")
                        st.write(f"- Budget: {profile.get('projet_achat', {}).get('budget', 'N/A')}")
                    
                    st.write("---")
                    st.info(generate_ice_breaker(profile))

                    action, reason = next_best_action(profile)
                    st.write(f"**Next Action:** {action} ({reason})")

                    # === Feature: Quick Action ===
                    st.markdown("**Action Rapide (SMS/WhatsApp)**")
                    quick_info = f"{profile.get('identite', {}).get('statut_relationnel', 'Client')} - {profile.get('client_id', 'Inconnu')} - {get_contact_info(profile.get('client_id', ''), True)[1]}"
                    st.code(quick_info, language="text")
                    # =============================

                    with st.expander("Voir le profil complet"):
                        st.json(profile)

    # ===== TAB 3: ANALYSES =====
    if "Analyses" in tabs:
        with tabs["Analyses"]:
            st.subheader("Analyses Croisees")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Répartition par Genre**")
                fig = go.Figure(data=[go.Pie(labels=list(kpis['genres'].keys()), values=list(kpis['genres'].values()), hole=0.6)])
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.write("**Répartition par Âge**")
                age_order = ['18-25', '26-35', '36-45', '46-55', '56+']
                age_df = pd.DataFrame([{'Âge': a, 'Clients': kpis['ages'].get(a, 0)} for a in age_order if kpis['ages'].get(a, 0)>0])
                fig = px.bar(age_df, x='Âge', y='Clients')
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)

            query = st.text_input("Segmentation IA (ex: VIP Paris budget 25k)")
            if query:
                criteria = parse_segment_query(query)
                st.info(f"Critères identifiés: {criteria}")

    # ===== TAB 4: ACTIONS =====
    if "Actions" in tabs:
        with tabs["Actions"]:
            st.subheader("Actions Marketing Prioritaires")
            budget_25k = kpis['budgets'].get('25k+', 0)
            nouveaux = kpis['segments'].get('Nouveau', 0)
            
            actions = [
                {'priority': 'URGENT', 'title': 'Contact VIP Budget 25K+', 'description': f'{budget_25k} clients à contacter', 'kpi': 'Conversion', 'target': '80%'},
                {'priority': 'IMPORTANT', 'title': 'Programme Welcome Nouveaux', 'description': f'{nouveaux} nouveaux clients', 'kpi': 'Activation', 'target': '50%'}
            ]
            for action in actions:
                with st.expander(f"**{action['priority']}** - {action['title']}"):
                    st.write(action['description'])
                    c1, c2 = st.columns(2)
                    c1.metric("KPI", action['kpi'])
                    c2.metric("Objectif", action['target'])

    # ===== TAB 5: IA MISTRAL =====
    if "IA Mistral" in tabs:
        with tabs["IA Mistral"]:
            st.subheader("Analyse IA avec Mistral")
            if MISTRAL_OK:
                st.success("✅ Mistral IA connecté")
                if conversations:
                     st.info("Sélectionnez un client pour analyser sa conversation.")
                else:
                    st.warning("Pas de conversations.")
            else:
                st.error("Mistral IA non disponible.")

    # ===== TAB 6: EQUIPE =====
    if "Equipe & Tendances" in tabs:
        with tabs["Equipe & Tendances"]:
            st.subheader("Performance Equipe")
            team = build_team_metrics_from_counts(kpis['total'], kpis['vip_count'], kpis['high_value'])
            if show_simulated:
                 st.dataframe(pd.DataFrame(team).T)
            else:
                st.info("Donnees masquées.")

    # ===== TAB 7: DATA & OPS =====
    if "Data & Ops" in tabs:
        with tabs["Data & Ops"]:
            st.subheader("Gestionnaire CSV")
            uploaded = st.file_uploader("Uploader CSV", type=["csv"])
            if uploaded:
                st.success("Fichier reçu (simulation).")

if __name__ == "__main__":
    main()
