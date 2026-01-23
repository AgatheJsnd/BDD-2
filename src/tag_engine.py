"""
Moteur de tagging - Convertit les analyses en profils structurés selon la taxonomie
"""
from typing import Dict, List
from config.taxonomy import TAXONOMY, LANGUAGE_MAPPING

class TagEngine:
    """Classe pour créer les profils tagués selon la taxonomie"""
    
    def __init__(self):
        self.taxonomy = TAXONOMY
    
    def create_profile(self, conversation: Dict, analysis: Dict) -> Dict:
        """Crée un profil client complet à partir des données analysées"""
        
        profile = {
            'client_id': conversation['client_id'],
            'metadata': {
                'date_conversation': conversation['date'],
                'duration': conversation['duration'],
                'language': LANGUAGE_MAPPING.get(conversation['language'], conversation['language'])
            },
            'identite': self._build_identite(analysis),
            'localisation': self._build_localisation(analysis),
            'mobilite_rythme_vie': self._build_mobilite(analysis),
            'lifestyle_centres_interet': self._build_lifestyle(analysis),
            'style_personnel': self._build_style(analysis),
            'projet_achat': self._build_projet_achat(analysis),
            'appetence_evenementielle': self._build_appetence(analysis),
            'relation_produit_innovation': self._build_relation_produit(analysis),
            'reseau_influence': self._build_reseau(analysis),
            'suivi': self._build_suivi(conversation, analysis),
            'metadata_client': self._build_metadata(analysis)
        }
        
        return profile
    
    def _build_identite(self, analysis: Dict) -> Dict:
        """Construit la section Identité"""
        identite = {}
        
        # Genre
        if 'femme' in analysis.get('genre', []):
            identite['genre'] = 'Femme'
        elif 'homme' in analysis.get('genre', []):
            identite['genre'] = 'Homme'
        
        # Âge
        if analysis.get('age'):
            identite['age'] = analysis['age']
        
        # Statut relationnel
        if 'vip' in analysis.get('statut', []):
            identite['statut_relationnel'] = 'VIP'
        elif 'fidele' in analysis.get('statut', []):
            identite['statut_relationnel'] = 'Fidèle'
        elif 'nouveau' in analysis.get('statut', []):
            identite['statut_relationnel'] = 'Nouveau'
        elif 'occasionnel' in analysis.get('statut', []):
            identite['statut_relationnel'] = 'Occasionnel'
        else:
            identite['statut_relationnel'] = 'Régulier'
        
        # Profession
        prof = analysis.get('profession', [])
        if 'entrepreneur' in prof:
            identite['profession'] = 'Entrepreneur'
        elif 'cadre' in prof:
            identite['profession'] = 'Cadre'
        elif 'profession_liberale' in prof:
            identite['profession'] = 'Profession_libérale'
        elif 'artiste' in prof:
            identite['profession'] = 'Artiste'
        
        return identite
    
    def _build_localisation(self, analysis: Dict) -> Dict:
        """Construit la section Localisation"""
        localisation = {}
        cities = analysis.get('cities', [])
        
        if cities:
            # Catégoriser par région
            europe_cities = ['Paris', 'Berlin', 'Milan', 'Madrid', 'London']
            amerique_cities = ['New_York']
            asie_cities = ['Dubai', 'Tokyo', 'Hong_Kong', 'Singapore']
            
            for city in cities:
                if city in europe_cities:
                    if 'europe' not in localisation:
                        localisation['europe'] = []
                    localisation['europe'].append(city)
                elif city in amerique_cities:
                    if 'amerique' not in localisation:
                        localisation['amerique'] = []
                    localisation['amerique'].append(city)
                elif city in asie_cities:
                    if 'moyen_orient_asie' not in localisation:
                        localisation['moyen_orient_asie'] = []
                    localisation['moyen_orient_asie'].append(city)
        
        return localisation
    
    def _build_mobilite(self, analysis: Dict) -> Dict:
        """Construit la section Mobilité et rythme de vie"""
        mobilite = {}
        
        # Détection de mobilité basée sur mentions de voyages
        if 'voyage' in str(analysis).lower():
            if 'constant' in str(analysis).lower() or 'frequently' in str(analysis).lower():
                mobilite['frequence_deplacement'] = 'Très_mobile'
            elif 'voyage' in str(analysis).lower():
                mobilite['frequence_deplacement'] = 'Mobile'
        
        return mobilite
    
    def _build_lifestyle(self, analysis: Dict) -> Dict:
        """Construit la section Lifestyle et centres d'intérêt"""
        lifestyle = {}
        
        # Sports
        sports = analysis.get('sport', [])
        if sports:
            sport_section = {}
            collectifs = ['football']
            individuels = ['golf', 'tennis', 'yoga', 'running', 'fitness', 'ski', 'natation']
            
            for sport in sports:
                if sport in collectifs:
                    if 'collectif' not in sport_section:
                        sport_section['collectif'] = []
                    sport_section['collectif'].append(sport.capitalize())
                elif sport in individuels:
                    if 'individuel' not in sport_section:
                        sport_section['individuel'] = []
                    sport_section['individuel'].append(sport.capitalize())
            
            if sport_section:
                lifestyle['sport'] = sport_section
        
        # Art et culture
        art = analysis.get('art_culture', [])
        if art:
            lifestyle['art_culture'] = [a.capitalize() for a in art]
        
        # Voyage
        voyage = analysis.get('voyage', [])
        if voyage:
            lifestyle['voyage'] = [v.capitalize() for v in voyage]
        
        return lifestyle
    
    def _build_style(self, analysis: Dict) -> Dict:
        """Construit la section Style personnel"""
        style = {}
        
        # Couleurs préférées
        couleurs = analysis.get('couleurs', [])
        if couleurs:
            style['couleurs_preferees'] = [c.capitalize() for c in couleurs]
        
        # Matières préférées
        matieres = analysis.get('matieres', [])
        if matieres:
            style['matieres_preferees'] = [m.capitalize() for m in matieres]
        
        # Pièces favorites
        pieces = analysis.get('pieces', [])
        if pieces:
            style['pieces_favorites'] = [p.capitalize() for p in pieces]
        
        return style
    
    def _build_projet_achat(self, analysis: Dict) -> Dict:
        """Construit la section Projet d'achat"""
        projet = {}
        
        # Motif
        motifs = analysis.get('motif', [])
        if motifs:
            projet['motif'] = motifs[0].capitalize()
        
        # Budget
        if analysis.get('budget'):
            projet['budget'] = analysis['budget']
        
        return projet
    
    def _build_appetence(self, analysis: Dict) -> Dict:
        """Construit la section Appétence événementielle"""
        # Section pour développement futur
        return {}
    
    def _build_relation_produit(self, analysis: Dict) -> Dict:
        """Construit la section Relation produit & Innovation"""
        # Section pour développement futur
        return {}
    
    def _build_reseau(self, analysis: Dict) -> Dict:
        """Construit la section Réseau & Influence"""
        reseau = {}
        
        # Détection basique d'influence
        if 'vip' in analysis.get('statut', []):
            reseau['influence'] = 'Réseau_affluent'
        
        return reseau
    
    def _build_suivi(self, conversation: Dict, analysis: Dict) -> Dict:
        """Construit la section Suivi"""
        suivi = {
            'action': 'Rappeler',
            'echeance': 'M+1',
            'canal_contact': 'Email'
        }
        
        return suivi
    
    def _build_metadata(self, analysis: Dict) -> Dict:
        """Construit les métadonnées clients"""
        metadata = {}
        
        # Régime alimentaire
        regime = analysis.get('regime', [])
        if 'vegane' in regime:
            metadata['regime_alimentaire'] = 'Végane'
        elif 'vegetarien' in regime:
            metadata['regime_alimentaire'] = 'Végétarien'
        elif 'pescetarien' in regime:
            metadata['regime_alimentaire'] = 'Pescetarien'
        
        # Allergies
        allergies = analysis.get('allergies', [])
        if allergies:
            metadata['allergies'] = allergies
        
        return metadata
