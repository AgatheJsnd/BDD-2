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
                'entrepreneur': ['entrepreneur', 'entreprise', 'business', 'imprenditore', 'empresario', 'unternehmer'],
                'cadre': ['dirigeant', 'directeur', 'director', 'ceo', 'manager', 'direttore', 'direktor'],
                'profession_liberale': ['avocat', 'médecin', 'chirurgien', 'lawyer', 'doctor', 'surgeon', 'avvocato', 'medico', 'abogado', 'arzt', 'rechtsanwalt'],
                'artiste': ['artiste', 'artist', 'peintre', 'sculpteur', 'musicien', 'gallerie', 'galleriste']
            },
            'sport': {
                'golf': ['golf'],
                'tennis': ['tennis'],
                'yoga': ['yoga', 'pilates'],
                'running': ['course', 'marathon', 'running', 'corsa'],
                'fitness': ['fitness', 'gym', 'training'],
                'ski': ['ski', 'skiing'],
                'football': ['football', 'soccer', 'calcio', 'fußball'],
                'natation': ['natation', 'swimming', 'nuoto']
            },
            'art_culture': {
                'musees': ['musée', 'museum', 'museo', 'galerie', 'gallery', 'galleria'],
                'opera': ['opéra', 'opera', 'oper'],
                'art': ['art', 'arte', 'kunst', 'collectionn', 'collect']
            },
            'voyage': {
                'luxe': ['luxe', 'luxury', 'lusso', 'lujo', 'cruise', 'croisière', 'yacht'],
                'culturel': ['culturel', 'cultural', 'culturale', 'museum', 'musée'],
                'aventure': ['safari', 'trek', 'aventure', 'adventure']
            },
            'couleurs': {
                'noir': ['noir', 'black', 'nero', 'schwarz'],
                'cognac': ['cognac', 'cognac', 'camel'],
                'beige': ['beige'],
                'bordeaux': ['bordeaux', 'burgundy', 'bordeaux'],
                'navy': ['navy', 'marine', 'blu'],
                'blanc': ['blanc', 'white', 'bianco', 'blanco', 'weiß'],
                'rose_gold': ['rosé gold', 'rose gold', 'oro rosa'],
                'gris': ['gris', 'gray', 'grey', 'grigio', 'grau']
            },
            'matieres': {
                'cuir': ['cuir', 'leather', 'cuoio', 'pelle', 'leder'],
                'cachemire': ['cachemire', 'cashmere', 'kaschmir'],
                'soie': ['soie', 'silk', 'seta', 'seda', 'seide']
            },
            'regime': {
                'vegetarien': ['végétarien', 'vegetarian', 'vegetariano', 'vegetarisch'],
                'vegane': ['végane', 'vegan', 'vegano'],
                'pescetarien': ['pescetarien', 'pescatarian', 'pescetariano']
            },
            'pieces': {
                'sacs': ['sac', 'bag', 'borsa', 'bolso', 'tasche', 'handbag'],
                'portefeuille': ['portefeuille', 'wallet', 'portafoglio', 'cartera', 'geldbörse'],
                'chaussures': ['chaussure', 'shoe', 'scarpa', 'zapato', 'schuh'],
                'montres': ['montre', 'watch', 'orologio', 'reloj', 'uhr']
            },
            'motif': {
                'cadeau': ['cadeau', 'gift', 'regalo', 'geschenk'],
                'anniversaire': ['anniversaire', 'birthday', 'compleanno', 'cumpleaños', 'geburtstag'],
                'mariage': ['mariage', 'wedding', 'matrimonio', 'boda', 'hochzeit'],
                'diplome': ['diplôme', 'graduation', 'laurea', 'diplomation']
            }
        }
    
    def extract_age(self, text: str) -> str:
        """Extrait l'âge du texte"""
        matches = re.findall(self.age_pattern, text.lower())
        if matches:
            age = int(matches[0])
            if age < 26:
                return "18-25"
            elif age < 36:
                return "26-35"
            elif age < 46:
                return "36-45"
            elif age < 56:
                return "46-55"
            else:
                return "56+"
        return None
    
    def extract_budget(self, text: str) -> str:
        """Extrait le budget du texte"""
        matches = re.findall(self.budget_pattern, text.lower())
        if matches:
            budget = int(matches[0])
            if budget < 5:
                return "<5k"
            elif budget < 10:
                return "5-10k"
            elif budget < 15:
                return "10-15k"
            elif budget < 25:
                return "15-25k"
            else:
                return "25k+"
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
        
        return list(set(found))  # Supprime les doublons
    
    def extract_cities(self, text: str) -> List[str]:
        """Extrait les villes mentionnées dans le texte"""
        cities = {
            'paris': 'Paris', 'berlin': 'Berlin', 'milan': 'Milan', 'milano': 'Milan',
            'madrid': 'Madrid', 'london': 'London', 'londres': 'London',
            'new york': 'New_York', 'dubai': 'Dubai', 'tokyo': 'Tokyo',
            'hong kong': 'Hong_Kong', 'singapore': 'Singapore', 'singapour': 'Singapore',
            'maroc': 'Maroc', 'tunisie': 'Tunisie', 'algérie': 'Algérie',
            'égypte': 'Égypte', 'egypt': 'Égypte'
        }
        
        text_lower = text.lower()
        found_cities = []
        for city_key, city_name in cities.items():
            if city_key in text_lower:
                found_cities.append(city_name)
        
        return list(set(found_cities))
    
    def extract_allergies(self, text: str) -> List[str]:
        """Extrait les allergies mentionnées"""
        allergy_keywords = {
            'nickel': ['nickel', 'nichel'],
            'latex': ['latex'],
            'gluten': ['gluten'],
            'lactose': ['lactose', 'lait', 'lattosio'],
            'fruits_coque': ['fruits coque', 'nut', 'noci'],
            'mariscos': ['mariscos', 'shellfish', 'fruits mer']
        }
        
        text_lower = text.lower()
        allergies = []
        
        for allergy, keywords in allergy_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and ('allergi' in text_lower or 'intolér' in text_lower):
                    allergies.append(allergy)
                    break
        
        return list(set(allergies))
    
    def analyze_full_text(self, text: str) -> Dict:
        """Analyse complète du texte"""
        return {
            'age': self.extract_age(text),
            'budget': self.extract_budget(text),
            'genre': self.extract_keywords(text, 'genre'),
            'statut': self.extract_keywords(text, 'statut'),
            'profession': self.extract_keywords(text, 'profession'),
            'sport': self.extract_keywords(text, 'sport'),
            'art_culture': self.extract_keywords(text, 'art_culture'),
            'voyage': self.extract_keywords(text, 'voyage'),
            'couleurs': self.extract_keywords(text, 'couleurs'),
            'matieres': self.extract_keywords(text, 'matieres'),
            'regime': self.extract_keywords(text, 'regime'),
            'pieces': self.extract_keywords(text, 'pieces'),
            'motif': self.extract_keywords(text, 'motif'),
            'cities': self.extract_cities(text),
            'allergies': self.extract_allergies(text)
        }
