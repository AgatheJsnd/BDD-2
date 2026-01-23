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
def load_all_data():
    """Charge toutes les données"""
    pg = ProfileGenerator()
    profiles = pg.get_all_profiles()
    stats = pg.get_statistics()
    
    try:
        csv = CSVProcessor("LVMH_Realistic_Merged_CA001-100.csv")
        conversations = csv.get_conversations()
    except:
        conversations = []
    
    return profiles, stats, conversations

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

def main():
    # Charger les données
    profiles, stats, conversations = load_all_data()
    kpis = calculate_kpis(profiles)
    
    # === HEADER ===
    st.markdown("""
    <div class="main-header">
        <h1>◆ LVMH Client Analytics</h1>
        <p>Dashboard Marketing • {} clients • {}</p>
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'ensemble",
        "👥 Clients",
        "📈 Analyses",
        "🎯 Actions",
        "🤖 IA Mistral"
    ])
    
    # ===== TAB 1: VUE D'ENSEMBLE =====
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Répartition par Statut")
            
            fig = go.Figure(data=[go.Pie(
                labels=list(kpis['segments'].keys()),
                values=list(kpis['segments'].values()),
                hole=0.5,
                marker_colors=COLORS,
                textinfo='label+percent',
                textposition='outside',
                textfont=dict(color='#1a1a1a', size=12)
            )])
            fig.update_layout(
                showlegend=False,
                margin=dict(t=30, b=30, l=30, r=30),
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[dict(text=f"<b>{kpis['total']}</b><br>clients", 
                                 x=0.5, y=0.5, font_size=18, font_color='#1a1a1a', showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Segments Clés")
            
            for statut, count in sorted(kpis['segments'].items(), key=lambda x: x[1], reverse=True):
                pct = count / kpis['total'] * 100
                st.markdown(f"""
                <div class="info-card">
                    <h4>{statut}</h4>
                    <div style="font-size:1.5rem; font-weight:700;">{count}</div>
                    <div style="color:#666666;">{pct:.0f}% du total</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Distribution budget
        st.subheader("Distribution par Budget")
        
        budget_order = ['<5k', '5-10k', '10-15k', '15-25k', '25k+']
        budget_df = pd.DataFrame([
            {'Budget': b, 'Clients': kpis['budgets'].get(b, 0)} 
            for b in budget_order if b in kpis['budgets'] or True
        ])
        budget_df['Budget'] = pd.Categorical(budget_df['Budget'], categories=budget_order, ordered=True)
        budget_df = budget_df.sort_values('Budget')
        
        fig = px.bar(budget_df, x='Budget', y='Clients', color_discrete_sequence=['#8B4513'])
        fig.update_layout(
            height=300,
            margin=dict(t=20, b=40, l=40, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#D4CFC9'),
            yaxis=dict(gridcolor='#D4CFC9')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Préférences
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Top Couleurs")
            for color, count in sorted(stats['couleurs_populaires'].items(), key=lambda x: x[1], reverse=True)[:5]:
                st.write(f"• **{color}**: {count} clients")
        
        with col2:
            st.subheader("Top Sports")
            for sport, count in sorted(stats['sports_populaires'].items(), key=lambda x: x[1], reverse=True)[:5]:
                st.write(f"• **{sport}**: {count} clients")
        
        with col3:
            st.subheader("Régimes Alimentaires")
            for regime, count in stats['regimes_alimentaires'].items():
                st.write(f"• **{regime}**: {count} clients")
    
    # ===== TAB 2: CLIENTS =====
    with tab2:
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
        filtered = profiles.copy()
        if filter_statut:
            filtered = [p for p in filtered if p.get('identite', {}).get('statut_relationnel') in filter_statut]
        if filter_budget:
            filtered = [p for p in filtered if p.get('projet_achat', {}).get('budget') in filter_budget]
        if search:
            filtered = [p for p in filtered if search.lower() in p.get('client_id', '').lower()]
        
        st.info(f"**{len(filtered)}** clients affichés")
        
        # Tableau des clients
        client_data = []
        for p in filtered:
            client_data.append({
                'ID': p.get('client_id', 'N/A'),
                'Genre': p.get('identite', {}).get('genre', 'N/A'),
                'Âge': p.get('identite', {}).get('age', 'N/A'),
                'Statut': p.get('identite', {}).get('statut_relationnel', 'N/A'),
                'Budget': p.get('projet_achat', {}).get('budget', 'N/A'),
                'Couleurs': ', '.join(p.get('style_personnel', {}).get('couleurs_preferees', [])[:2]),
                'Profession': p.get('identite', {}).get('profession', 'N/A')
            })
        
        if client_data:
            df = pd.DataFrame(client_data)
            st.dataframe(df, use_container_width=True, height=400)
        
        # Détail client
        st.subheader("Détail Client")
        selected_id = st.selectbox("Sélectionner un client", [p.get('client_id') for p in profiles])
        
        if selected_id:
            profile = next((p for p in profiles if p.get('client_id') == selected_id), None)
            if profile:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Identité**")
                    st.write(f"- Genre: {profile.get('identite', {}).get('genre', 'N/A')}")
                    st.write(f"- Âge: {profile.get('identite', {}).get('age', 'N/A')}")
                    st.write(f"- Profession: {profile.get('identite', {}).get('profession', 'N/A')}")
                    st.write(f"- Statut: {profile.get('identite', {}).get('statut_relationnel', 'N/A')}")
                
                with col2:
                    st.write("**Préférences**")
                    colors = profile.get('style_personnel', {}).get('couleurs_preferees', [])
                    st.write(f"- Couleurs: {', '.join(colors) if colors else 'N/A'}")
                    matieres = profile.get('style_personnel', {}).get('matieres_preferees', [])
                    st.write(f"- Matières: {', '.join(matieres) if matieres else 'N/A'}")
                    regime = profile.get('metadata_client', {}).get('regime_alimentaire', 'N/A')
                    st.write(f"- Régime: {regime}")
                
                with col3:
                    st.write("**Projet d'achat**")
                    st.write(f"- Budget: {profile.get('projet_achat', {}).get('budget', 'N/A')}")
                    st.write(f"- Motif: {profile.get('projet_achat', {}).get('motif', 'N/A')}")
                    pieces = profile.get('projet_achat', {}).get('pieces_cibles', [])
                    st.write(f"- Pièces: {', '.join(pieces) if pieces else 'N/A'}")

                # Affichage des Badges Amélioré
                st.write("---")
                st.subheader("Profil & Intérêts")
                
                badges = get_client_badges(profile)
                
                # CSS Badges
                st.markdown("""
                <style>
                .badge-group {
                    background: #ffffff;
                    border: 1px solid #EBE4DC;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 15px;
                    height: 100%;
                }
                .badge-header {
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #8B4513;
                    font-weight: 700;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .modern-badge {
                    display: inline-flex;
                    align-items: center;
                    padding: 4px 10px;
                    margin: 3px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    transition: all 0.2s;
                }
                .b-statut { background: #8B4513; color: white; border: 1px solid #8B4513; }
                .b-lifestyle { background: #FAF8F5; color: #5D4037; border: 1px solid #D7CCC8; }
                .b-style { background: #EFEBE9; color: #3E2723; border: 1px solid #BCAAA4; }
                .b-loc { background: #FFF3E0; color: #E65100; border: 1px solid #FFE0B2; }
                </style>
                """, unsafe_allow_html=True)
                
                # Groupes
                col_life, col_style, col_info = st.columns(3)
                
                # 1. Lifestyle
                with col_life:
                    lifestyle_badges = [b for b in badges if b['type'] == 'lifestyle']
                    st.markdown(f"""
                    <div class="badge-group">
                        <div class="badge-header">🧘 Lifestyle & Hobbies</div>
                        <div>
                            {''.join([f'<span class="modern-badge b-lifestyle">{b["text"]}</span>' for b in lifestyle_badges]) or '<span style="color:#999;font-style:italic">Aucune donnée</span>'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 2. Style & Goûts
                with col_style:
                    style_badges = [b for b in badges if b['type'] == 'style']
                    st.markdown(f"""
                    <div class="badge-group">
                        <div class="badge-header">🎨 Style & Préférences</div>
                        <div>
                            {''.join([f'<span class="modern-badge b-style">{b["text"]}</span>' for b in style_badges]) or '<span style="color:#999;font-style:italic">Aucune donnée</span>'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 3. Statut & Infos
                with col_info:
                    info_badges = [b for b in badges if b['type'] not in ['lifestyle', 'style']]
                    st.markdown(f"""
                    <div class="badge-group">
                        <div class="badge-header">🌍 Statut & Info</div>
                        <div>
                            {''.join([f'<span class="modern-badge b-{"statut" if b["type"]=="statut" else "loc"}">{b["text"]}</span>' for b in info_badges]) or '<span style="color:#999;font-style:italic">Aucune donnée</span>'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander("Voir le profil complet (JSON)"):
                    st.json(profile)
    
    # ===== TAB 3: ANALYSES =====
    with tab3:
        st.subheader("Analyses Croisées")
        
        # Démographie
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Répartition par Genre**")
            fig = go.Figure(data=[go.Pie(
                labels=list(kpis['genres'].keys()),
                values=list(kpis['genres'].values()),
                hole=0.6,
                marker_colors=['#8B4513', '#D2691E']
            )])
            fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Répartition par Âge**")
            age_order = ['18-25', '26-35', '36-45', '46-55', '56+']
            age_df = pd.DataFrame([
                {'Âge': a, 'Clients': kpis['ages'].get(a, 0)} 
                for a in age_order if kpis['ages'].get(a, 0) > 0
            ])
            fig = px.bar(age_df, x='Âge', y='Clients', color_discrete_sequence=['#A0522D'])
            fig.update_layout(height=250, margin=dict(t=20, b=40, l=40, r=20))
            st.plotly_chart(fig, use_container_width=True)
        
        # Matrice Budget x Statut
        st.subheader("Matrice Budget × Statut")
        
        matrix_data = []
        for statut in ['VIP', 'Fidèle', 'Régulier', 'Nouveau', 'Occasionnel']:
            row = {'Statut': statut}
            for budget in ['<5k', '5-10k', '10-15k', '15-25k', '25k+']:
                count = len([p for p in profiles 
                           if p.get('identite', {}).get('statut_relationnel') == statut
                           and p.get('projet_achat', {}).get('budget') == budget])
                row[budget] = count
            matrix_data.append(row)
        
        matrix_df = pd.DataFrame(matrix_data)
        st.dataframe(matrix_df.set_index('Statut'), use_container_width=True)
        
        # Corrélations VIP
        st.subheader("Profil Type VIP")
        
        vip_profiles = [p for p in profiles if p.get('identite', {}).get('statut_relationnel') == 'VIP']
        
        if vip_profiles:
            vip_colors = Counter()
            vip_sports = Counter()
            vip_budgets = Counter()
            
            for p in vip_profiles:
                for c in p.get('style_personnel', {}).get('couleurs_preferees', []):
                    vip_colors[c] += 1
                sports = p.get('lifestyle_centres_interet', {}).get('sport', {})
                for sport_list in sports.values():
                    if isinstance(sport_list, list):
                        for s in sport_list:
                            vip_sports[s] += 1
                vip_budgets[p.get('projet_achat', {}).get('budget', 'N/A')] += 1
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Couleurs préférées**")
                for c, cnt in vip_colors.most_common(5):
                    st.write(f"• {c}: {cnt}")
            
            with col2:
                st.write("**Sports pratiqués**")
                for s, cnt in vip_sports.most_common(5):
                    st.write(f"• {s}: {cnt}")
            
            with col3:
                st.write("**Budgets**")
                for b, cnt in vip_budgets.most_common():
                    st.write(f"• {b}: {cnt}")
    
    # ===== TAB 4: ACTIONS =====
    with tab4:
        st.subheader("Actions Marketing Prioritaires")
        
        # Calculs pour les actions
        budget_25k = len([p for p in profiles if p.get('projet_achat', {}).get('budget') == '25k+'])
        nouveaux = kpis['segments'].get('Nouveau', 0)
        yoga_count = stats['sports_populaires'].get('Yoga', 0)
        vegans = stats['regimes_alimentaires'].get('Végane', 0)
        
        actions = [
            {
                'priority': 'URGENT',
                'title': 'Contact VIP Budget 25K+',
                'description': f'{budget_25k} clients à contacter personnellement',
                'kpi': 'Taux de conversion',
                'target': '80%'
            },
            {
                'priority': 'IMPORTANT',
                'title': 'Programme Welcome Nouveaux',
                'description': f'{nouveaux} nouveaux clients à activer',
                'kpi': 'Taux d\'activation',
                'target': '50%'
            },
            {
                'priority': 'OPPORTUNITÉ',
                'title': 'Événement Wellness/Yoga',
                'description': f'{yoga_count} clients yoga identifiés',
                'kpi': 'Participation',
                'target': '30%'
            },
            {
                'priority': 'SEGMENT',
                'title': 'Collection Éco-responsable',
                'description': f'{vegans} clients véganes sensibles RSE',
                'kpi': 'Engagement',
                'target': '40%'
            }
        ]
        
        for action in actions:
            with st.expander(f"**{action['priority']}** - {action['title']}"):
                st.write(action['description'])
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("KPI", action['kpi'])
                with col2:
                    st.metric("Objectif", action['target'])
        
        st.subheader("Infos Événements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Régimes à prévoir (catering)**")
            total_special = sum(stats['regimes_alimentaires'].values())
            for regime, count in stats['regimes_alimentaires'].items():
                pct = count / kpis['total'] * 100
                st.write(f"• {regime}: {count} ({pct:.0f}%)")
        
        with col2:
            st.write("**Recommandations**")
            veggie_total = stats['regimes_alimentaires'].get('Végane', 0) + stats['regimes_alimentaires'].get('Végétarien', 0)
            st.warning(f"⚠️ {veggie_total} clients végétariens/véganes - Prévoir options dédiées")
    
    # ===== TAB 5: IA MISTRAL =====
    with tab5:
        st.subheader("Analyse IA avec Mistral")
        
        if not MISTRAL_OK:
            st.error("❌ Mistral IA non disponible. Vérifiez le fichier .env et les dépendances.")
        else:
            st.success("✅ Mistral IA connecté")
            
            if conversations:
                selected_client = st.selectbox("Sélectionner un client à analyser", 
                                              [c['client_id'] for c in conversations])
                
                conversation = next((c for c in conversations if c['client_id'] == selected_client), None)
                
                if conversation:
                    with st.expander("📄 Voir la transcription"):
                        st.text_area("", conversation['transcription'], height=200, disabled=True)
                    
                    if st.button("🚀 Analyser avec Mistral IA"):
                        with st.spinner("Analyse en cours..."):
                            try:
                                analyzer = MistralAnalyzer()
                                result = analyzer.analyze_transcription(conversation['transcription'], selected_client)
                                
                                if "error" not in result:
                                    st.success("✅ Analyse terminée")
                                    
                                    st.write("**📋 Résumé**")
                                    st.info(result.get('resume', 'N/A'))
                                    
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.write("**👤 Profil détecté**")
                                        profil = result.get('profil_client', {})
                                        st.write(f"- Genre: {profil.get('genre', 'N/A')}")
                                        st.write(f"- Âge: {profil.get('age_estime', 'N/A')}")
                                        st.write(f"- Profession: {profil.get('profession', 'N/A')}")
                                        st.write(f"- Statut: {profil.get('statut_vip', 'N/A')}")
                                    
                                    with col2:
                                        st.write("**💰 Projet d'achat**")
                                        projet = result.get('projet_achat', {})
                                        st.write(f"- Type: {projet.get('type', 'N/A')}")
                                        st.write(f"- Budget: {projet.get('budget_estime', 'N/A')}")
                                        st.write(f"- Urgence: {projet.get('urgence', 'N/A')}")
                                    
                                    st.write("**🏷️ Tags suggérés**")
                                    tags = result.get('tags_suggeres', [])
                                    st.write(", ".join(tags) if tags else "Aucun")
                                    
                                    st.write("**💡 Recommandations commerciales**")
                                    for i, rec in enumerate(result.get('recommandations_commerciales', []), 1):
                                        st.write(f"{i}. {rec}")
                                    
                                    st.metric("Score Potentiel", f"{result.get('score_potentiel', 0)}/100")
                                else:
                                    st.error(f"Erreur: {result.get('error')}")
                            except Exception as e:
                                st.error(f"Erreur: {str(e)}")
            else:
                st.warning("Aucune conversation disponible")

if __name__ == "__main__":
    main()
