"""
Module d'analyse de texte pour extraire les informations des transcriptions
"""
import re
from typing import Dict, List, Set


class TextAnalyzer:
    """Classe pour analyser le texte des transcriptions et extraire les informations"""

    def __init__(self):
        # Patterns pour extraction
        self.age_pattern = r'(\d+)\s*ans?'
        self.budget_pattern = r'(\d+)[kK€]'

        # Dictionnaires de mots-clés multilingues
        self.keywords = {
            'genre': {
                'femme': ['mme', 'madame', 'mrs', 'ms', 'signora', 'sra', 'frau', 'elle', 'wife', 'épouse', 'moglie', 'esposa', 'ehefrau'],
                'homme': ['m.', 'monsieur', 'mr', 'signor', 'sr', 'herr', 'lui', 'husband', 'mari', 'marito', 'marido', 'ehemann']
            },
            'statut': {
                'vip': ['vip', 'excellent', 'exceptionnel', 'exceptional', 'eccezionale'],
                'fidele': ['fidèle', 'depuis', 'long-time', 'regular', 'fedele', 'treue', 'cliente'],
                'nouveau': ['nouveau', 'nouvelle', 'first', 'new', 'primo', 'neu', 'primera'],
                'occasionnel': ['occasionnel', 'occasional', 'gelegentliche']
            },
            'profession': {
                'Entrepreneur_Dirigeant': ['entrepreneur', 'fondateur', 'dirigeant', 'ceo', 'found', 'owner', 'entreprise', 'business'],
                'Cadre_Manager': ['manager', 'cadre', 'directeur', 'director', 'responsable'],
                'avocat': ['avocat', 'lawyer', 'legal', 'avvocato'],
                'médecin': ['médecin', 'doctor', 'medico', 'chirurgien', 'surgeon'],
                'architecte': ['architecte', 'architect', 'architetto'],
                'finance': ['banquier', 'banker', 'finance', 'trader', 'investissement', 'investment', 'wealth'],
                'artiste': ['artiste', 'artist', 'peintre', 'sculpteur', 'musique', 'musicien'],
                'mode': ['styliste', 'fashion', 'mode', 'luxe', 'retail'],
                'tech': ['ingénieur', 'engineer', 'tech', 'digital', 'développeur', 'developer', 'data', 'ia', 'ai'],
                'marketing': ['marketing', 'communication', 'journaliste', 'publique', 'relations'],
                'sportive': ['athlète', 'coach', 'sportif', 'sportive']
            },
            'sport': {
                'football': ['football', 'soccer', 'ballon'],
                'tennis': ['tennis', 'raquette'],
                'padel': ['padel'],
                'golf': ['golf'],
                'ski': ['ski', 'station', 'montagne'],
                'yoga': ['yoga', 'pilates', 'méditation', 'bien-être'],
                'running': ['course', 'marathon', 'running'],
                'natation': ['natation', 'piscine', 'swimming'],
                'fitness': ['fitness', 'gym', 'musculation'],
                'f1': ['formule 1', 'f1', 'grand prix']
            },
            'musique': {
                'classique': ['classique', 'opéra', 'orchestre', 'instrumental'],
                'pop': ['pop', 'radio'],
                'rock': ['rock'],
                'hip_hop': ['hip hop', 'rap'],
                'electro': ['electro', 'house', 'techno', 'dj'],
                'jazz': ['jazz', 'soul', 'blues']
            },
            'voyage': {
                'luxe': ['luxe', 'luxury', 'palace', 'hôtel 5', 'resort'],
                'aventure': ['aventure', 'safari', 'trek', 'expédition'],
                'culturel': ['culture', 'histoire', 'visite', 'musée'],
                'détente': ['détente', 'repos', 'plage', 'spa']
            },
            'couleurs': {
                'noir': ['noir', 'black', 'nero', 'schwarz'],
                'blanc': ['blanc', 'white', 'bianco'],
                'beige': ['beige', 'sable', 'taupe'],
                'gris': ['gris', 'grey', 'gray'],
                'marine': ['marine', 'navy'],
                'cognac': ['cognac', 'marron', 'brown', 'camel'],
                'bordeaux': ['bordeaux', 'burgundy'],
                'rouge': ['rouge', 'red', 'rosso'],
                'bleu': ['bleu', 'blue', 'azzurro'],
                'vert': ['vert', 'green', 'verde'],
                'or': ['or', 'gold', 'doré'],
                'argent': ['argent', 'silver']
            },
            'matieres': {
                'cuir': ['cuir', 'leather', 'pelle'],
                'cachemire': ['cachemire', 'cashmere'],
                'soie': ['soie', 'silk', 'seta'],
                'laine': ['laine', 'wool'],
                'coton': ['coton', 'cotton'],
                'lin': ['lin', 'linen'],
                'vegan': ['vegan', 'éco', 'recyclé', 'durable']
            },
            'regime': {
                'vegetarien': ['végétarien', 'vegetarian', 'vegetariano'],
                'vegane': ['végane', 'vegan'],
                'pescetarien': ['pescetarien', 'pescatarian']
            },
            'pieces': {
                'sacs': ['sac', 'bag', 'borsa', 'pochette', 'handbag'],
                'chaussures': ['chaussure', 'shoe', 'scarpa', 'baskets', 'sneakers', 'escarpins', 'bottes', 'mocassins'],
                'manteaux': ['manteau', 'coat', 'trench', 'veste', 'jacket', 'doudoune'],
                'robes': ['robe', 'dress', 'soirée', 'cocktail'],
                'costumes': ['costume', 'suit', 'smoking'],
                'accessoires': ['montre', 'watch', 'bijou', 'jewelry', 'lunettes', 'glasses', 'ceinture', 'belt', 'chapeau', 'hat']
            },
            'motif': {
                'cadeau': ['cadeau', 'gift', 'offrir', 'regalo'],
                'anniversaire': ['anniversaire', 'birthday'],
                'mariage': ['mariage', 'wedding'],
                'diplome': ['diplôme', 'graduation'],
                'plaisir': ['plaisir', 'personnel', 'moi', 'investissement']
            },
            'marques': {
                'Louis Vuitton': ['louis vuitton', 'vuitton', 'lv'],
                'Dior': ['dior'],
                'Gucci': ['gucci'],
                'Loro Piana': ['loro piana'],
                'Bulgari': ['bulgari'],
                'Tiffany': ['tiffany'],
                'Celine': ['celine'],
                'Fendi': ['fendi'],
                'Sephora': ['sephora']
            },
            'valeurs': {
                'éthique': ['éthique', 'durable', 'responsable', 'écologique', 'environnement'],
                'qualité': ['qualité', 'artisanat', 'savoir-faire', 'made in', 'artisanal'],
                'exclusivité': ['exclusif', 'rare', 'limité', 'sur-mesure', 'private']
            }
        }

    def extract_age(self, text: str) -> str:
        """Extrait l'âge du texte et le convertit en tranche de la taxonomie"""
        if not isinstance(text, str) or not text.strip():
            return None
        
        text_lower = text.lower()
        age = None
        
        # Patterns multiples
        patterns = [
            r'(\d+)\s*ans?',           
            r'(\d+)\s*years?',         
            r'(\d+)\s*anni',           
            r'(\d+)\s*años',           
            r'(\d+)\s*jahre',          
            r'aged?\s*(\d+)',          
            r'environ\s*(\d+)',        
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    age = int(matches[0])
                    if 15 <= age <= 100:
                        break
                    else:
                        age = None
                except ValueError:
                    continue
        
        if age:
            if age < 26: return "18-25"
            elif age < 36: return "26-35"
            elif age < 46: return "36-45"
            elif age < 56: return "46-55"
            else: return "56+"
        
        return None

    def extract_budget(self, text: str) -> str:
        """Extrait le budget et le convertit en tranche de la taxonomie"""
        if not isinstance(text, str) or not text.strip():
            return None

        text_lower = text.lower()
        
        patterns = [
            (r'(\d+)\s*[kK]', 1000),                    
            (r'(\d+(?:[.,]\d+)?)\s*[€$£]', 1),          
            (r'[€$£]\s*(\d+(?:[.,]\d+)?)', 1),          
            (r'(\d+(?:[.,]\d+)?)\s*euros?', 1),         
        ]
        
        budget = None
        for pattern, multiplier in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    val = str(matches[0]).replace(',', '').replace('.', '')
                    budget = int(val) * multiplier
                    if budget < 100: budget *= 1000
                    break
                except (ValueError, IndexError):
                    continue
        
        if budget:
            if budget < 5000: return "<5k"
            elif budget < 10000: return "5–10k" # Use en-dash as in taxonomy
            elif budget < 15000: return "10–15k"
            elif budget < 25000: return "15–25k"
            else: return "25k+"

        return None

    def extract_keywords(self, text: str, category: str) -> List[str]:
        """Extrait les mots-clés d'une catégorie donnée"""
        text_lower = text.lower()
        found = []

        if category in self.keywords:
            for key, keywords_list in self.keywords[category].items():
                for keyword in keywords_list:
                    if keyword in text_lower:
                        found.append(key)
                        break

        return list(set(found))

    def extract_cities(self, text: str) -> List[str]:
        """Extrait les villes mentionnées"""
        cities = {
            'paris': 'Paris', 'berlin': 'Berlin', 'milan': 'Milan', 'milano': 'Milan',
            'madrid': 'Madrid', 'london': 'London', 'londres': 'London',
            'new york': 'New York', 'los angeles': 'Los Angeles', 'la': 'Los Angeles',
            'dubai': 'Dubai', 'tokyo': 'Tokyo', 'hong kong': 'Hong Kong', 
            'singapore': 'Singapore', 'singapour': 'Singapore',
            'maroc': 'Maroc', 'égypte': 'Égypte', 'afrique du sud': 'Afrique du Sud'
        }

        text_lower = text.lower()
        found_cities = []
        for city_key, city_name in cities.items():
            # Use word boundaries for cities to avoid matching partial words
            if re.search(r'\b' + re.escape(city_key) + r'\b', text_lower):
                found_cities.append(city_name)

        return list(set(found_cities))

    def analyze_full_text(self, text: str) -> Dict:
        """Analyse complète du texte"""
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        
        return {
            'age': self.extract_age(text),
            'budget': self.extract_budget(text),
            'genre': self.extract_keywords(text, 'genre'),
            'statut': self.extract_keywords(text, 'statut'),
            'profession_raw': self.extract_keywords(text, 'profession'),
            'sport_raw': self.extract_keywords(text, 'sport'),
            'musique_raw': self.extract_keywords(text, 'musique'),
            'voyage_raw': self.extract_keywords(text, 'voyage'),
            'couleurs_raw': self.extract_keywords(text, 'couleurs'),
            'matieres_raw': self.extract_keywords(text, 'matieres'),
            'regime_raw': self.extract_keywords(text, 'regime'),
            'pieces_raw': self.extract_keywords(text, 'pieces'),
            'motif_raw': self.extract_keywords(text, 'motif'),
            'marques_raw': self.extract_keywords(text, 'marques'),
            'valeurs_raw': self.extract_keywords(text, 'valeurs'),
            'cities': self.extract_cities(text)
        }
