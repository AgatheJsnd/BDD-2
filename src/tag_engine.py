"""
Moteur de tagging - Convertit les analyses en profils structurés selon la nouvelle taxonomie
"""
from typing import Dict, List
import re
from config.taxonomy import TAXONOMY, LANGUAGE_MAPPING

class TagEngine:
    """Classe pour créer les profils tagués selon la taxonomie LVMH v2.0"""
    
    def __init__(self):
        self.taxonomy = TAXONOMY
    
    def create_profile(self, conversation: Dict, analysis: Dict) -> Dict:
        """Crée un profil client complet à partir des données analysées"""
        
        profile = {
            'client_id': conversation['client_id'],
            'metadata': {
                'date_conversation': conversation['date'],
                'duration': conversation['duration'],
                'language': LANGUAGE_MAPPING.get(conversation['language'], conversation['language']),
                'profile_version': '2.0'
            },
            'identite': self._build_identite(analysis),
            'localisation': self._build_localisation(analysis),
            'lifestyle_centres_interet': self._build_lifestyle(analysis),
            'style_personnel': self._build_style(analysis),
            'projet_achat': self._build_projet_achat(analysis),
            'preferences_contraintes': self._build_preferences(analysis),
            'suivi': self._build_suivi(analysis)
        }
        
        return profile
    
    def _build_identite(self, analysis: Dict) -> Dict:
        identite = {
            'genre': 'Autre',
            'statut_relationnel': 'Régulier'
        }
        
        # Genre
        if 'femme' in analysis.get('genre', []): identite['genre'] = 'Femme'
        elif 'homme' in analysis.get('genre', []): identite['genre'] = 'Homme'
        
        # Âge
        if analysis.get('age'): identite['age'] = analysis['age']
        
        # Statut
        statut_map = {'vip': 'VIP', 'fidele': 'Fidèle', 'nouveau': 'Nouveau', 'occasionnel': 'Occasionnel'}
        for k, v in statut_map.items():
            if k in analysis.get('statut', []):
                identite['statut_relationnel'] = v
                break

        # Langue
        identite['langue_parlee'] = [LANGUAGE_MAPPING.get(analysis.get('language', 'FR'), 'Français')]

        # Profession / Secteur (Nested)
        prof_raw = analysis.get('profession_raw', [])
        secteur = {}
        if 'Entrepreneur_Dirigeant' in prof_raw: secteur['Entrepreneur_Dirigeant'] = []
        if 'Cadre_Manager' in prof_raw: secteur['Cadre_Manager'] = []
        
        # Libérales
        liberal = []
        if 'avocat' in prof_raw: liberal.append('Avocat')
        if 'médecin' in prof_raw: liberal.append('Médecin')
        if 'architecte' in prof_raw: liberal.append('Architecte')
        if liberal: secteur['Profession_liberale'] = liberal

        # Finance
        if 'finance' in prof_raw: secteur['Finance_Investissement'] = ['Banquier'] # simplification
        if 'artiste' in prof_raw: secteur['Art_Creation'] = ['Artiste']
        if 'mode' in prof_raw: secteur['Mode_Luxe'] = ['Styliste']
        if 'tech' in prof_raw: secteur['Tech_Digital'] = ['Ingénieur']
        if 'marketing' in prof_raw: secteur['Medias_Communication'] = ['Marketing']
        if 'sportive' in prof_raw: secteur['Sport'] = ['Athlète']

        if secteur:
            identite['profession_secteur'] = secteur
        else:
            identite['profession_secteur'] = {"Autres": []}
            
        return identite
    
    def _build_localisation(self, analysis: Dict) -> Dict:
        loc = {}
        cities = analysis.get('cities', [])
        
        mapping = {
            'europe': ['Paris', 'Berlin', 'Milan', 'Madrid', 'London'],
            'amerique': ['Los Angeles', 'New York'],
            'moyen_orient_asie': ['Dubai', 'Tokyo', 'Hong Kong', 'Singapore'],
            'afrique': ['Maroc', 'Égypte', 'Afrique du Sud']
        }
        
        for region, city_list in mapping.items():
            found = [c for c in cities if c in city_list]
            if found:
                loc[region] = found
        
        return loc
    
    def _build_lifestyle(self, analysis: Dict) -> Dict:
        lifestyle = {}
        
        # Sport
        sport_raw = analysis.get('sport_raw', [])
        if sport_raw:
            sport_struct = {'collectif': [], 'individuel': {}}
            raquette = [s.capitalize() for s in sport_raw if s in ['tennis', 'padel', 'squash', 'badminton']]
            outdoor = [s.capitalize() for s in sport_raw if s in ['golf', 'ski', 'surf', 'escalade', 'randonnée']]
            bien_etre = [s.capitalize() for s in sport_raw if s in ['yoga', 'pilates', 'méditation']]
            endurance = [s.capitalize() for s in sport_raw if s in ['running', 'cyclisme', 'natation']]
            
            if raquette: sport_struct['individuel']['raquette'] = raquette
            if outdoor: sport_struct['individuel']['outdoor'] = outdoor
            if bien_etre: sport_struct['individuel']['bien_etre'] = bien_etre
            if endurance: sport_struct['individuel']['endurance'] = endurance
            
            collectifs = [s.capitalize() for s in sport_raw if s in ['football', 'rugby', 'basketball']]
            if collectifs: sport_struct['collectif'] = collectifs
            
            lifestyle['sport'] = sport_struct

        # Musique
        musique_raw = analysis.get('musique_raw', [])
        if musique_raw:
            m_struct = {}
            if 'classique' in musique_raw: m_struct['classique_elegant'] = ['Classique']
            if 'pop' in musique_raw: m_struct['moderne_populaire'] = ['Pop']
            if 'electro' in musique_raw: m_struct['electronique'] = ['Electro']
            if 'jazz' in musique_raw: m_struct['jazz_soul'] = ['Jazz']
            lifestyle['musique'] = m_struct

        # Voyage
        voyage_raw = analysis.get('voyage_raw', [])
        if voyage_raw:
            lifestyle['voyage'] = {
                'experience': [v.capitalize() for v in voyage_raw]
            }

        return lifestyle
    
    def _build_style(self, analysis: Dict) -> Dict:
        style = {}
        
        # Couleurs
        colors_raw = analysis.get('couleurs_raw', [])
        if colors_raw:
            c_struct = {'neutres_intemporelles': [], 'tons_chauds': [], 'tons_froids': [], 'pastels': [], 'metalliques': []}
            for c in colors_raw:
                if c in ['noir', 'blanc', 'beige', 'gris', 'marine']: c_struct['neutres_intemporelles'].append(c.capitalize())
                elif c in ['cognac', 'marron', 'bordeaux', 'rouge', 'orange']: c_struct['tons_chauds'].append(c.capitalize())
                elif c in ['bleu', 'vert', 'kaki', 'violet']: c_struct['tons_froids'].append(c.capitalize())
                elif c in ['or', 'argent', 'bronze']: c_struct['metalliques'].append(c.capitalize())
            
            # Clean empty lists
            style['couleurs_preferees'] = {k: v for k, v in c_struct.items() if v}

        # Matières
        mat_raw = analysis.get('matieres_raw', [])
        if mat_raw:
            m_struct = {'naturelles': [], 'premium': [], 'techniques': [], 'alternatives': []}
            for m in mat_raw:
                if m in ['cuir', 'cachemire', 'soie', 'laine', 'coton', 'lin', 'denim']: m_struct['naturelles'].append(m.capitalize())
                elif m == 'vegan': m_struct['alternatives'].append('Matières vegan')
            style['matieres_preferees'] = {k: v for k, v in m_struct.items() if v}

        # Pièces
        pieces_raw = analysis.get('pieces_raw', [])
        if pieces_raw:
            p_struct = {}
            if 'sacs' in pieces_raw: p_struct['sacs'] = ['Sac à main']
            if 'chaussures' in pieces_raw: p_struct['chaussures'] = ['Baskets / Sneakers']
            if 'manteaux' in pieces_raw: p_struct['manteaux'] = ['Veste légère']
            if 'accessoires' in pieces_raw: p_struct['accessoires'] = ['Montres']
            style['pieces_favorites'] = p_struct

        return style
    
    def _build_projet_achat(self, analysis: Dict) -> Dict:
        projet = {}
        if analysis.get('budget'):
            projet['budget'] = analysis['budget']
        
        # Motif
        motif_raw = analysis.get('motif_raw', [])
        if motif_raw:
            if 'cadeau' in motif_raw or 'anniversaire' in motif_raw:
                projet['motif_role'] = {'offrir': [m.capitalize() for m in motif_raw]}
            else:
                projet['motif_role'] = {'pour_soi': ['Plaisir personnel']}

        # Marques
        marques = analysis.get('marques_raw', [])
        if marques:
            projet['marques_preferees'] = {m: [] for m in marques}

        return projet
    
    def _build_preferences(self, analysis: Dict) -> Dict:
        prefs = {}
        
        # Régime
        regime = analysis.get('regime_raw', [])
        if regime:
            prefs['regime'] = [r.capitalize() for r in regime]
        else:
            prefs['regime'] = ["Aucun"]

        # Valeurs
        valeurs = analysis.get('valeurs_raw', [])
        if valeurs:
            v_map = {'éthique': 'Éthique / durable', 'qualité': 'Qualité & savoir-faire', 'exclusivité': 'Exclusivité'}
            prefs['valeurs'] = [v_map[v] for v in valeurs if v in v_map]

        return prefs
    
    def _build_suivi(self, analysis: Dict) -> Dict:
        return {
            'action': ['Rappeler'],
            'echeance': 'M+1',
            'canal_contact': 'Email'
        }
