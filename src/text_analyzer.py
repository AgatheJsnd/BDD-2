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
        self.budget_pattern = r'(\d+)[kKâ‚¬]'

        # Dictionnaires de mots-clÃ©s multilingues
        self.keywords = {
            'genre': {
                'femme': ['mme', 'madame', 'mrs', 'ms', 'signora', 'sra', 'frau', 'elle', 'wife', 'Ã©pouse', 'moglie', 'esposa', 'ehefrau'],
                'homme': ['m.', 'monsieur', 'mr', 'signor', 'sr', 'herr', 'lui', 'husband', 'mari', 'marito', 'marido', 'ehemann']
            },
            'statut': {
                'vip': ['vip', 'excellent', 'exceptionnel', 'exceptional', 'eccezionale'],
                'fidele': ['fidÃ¨le', 'depuis', 'long-time', 'regular', 'fedele', 'treue', 'cliente'],
                'nouveau': ['nouveau', 'nouvelle', 'first', 'new', 'primo', 'neu', 'primera'],
                'occasionnel': ['occasionnel', 'occasional', 'gelegentliche']
            },
            'profession': {
                'entrepreneur': ['entrepreneur', 'entreprise', 'business', 'imprenditore', 'empresario', 'unternehmer'],
                'cadre': ['dirigeant', 'directeur', 'director', 'ceo', 'manager', 'direttore', 'direktor'],
                'profession_liberale': ['avocat', 'mÃ©decin', 'chirurgien', 'lawyer', 'doctor', 'surgeon', 'avvocato', 'medico', 'abogado', 'arzt', 'rechtsanwalt'],
                'artiste': ['artiste', 'artist', 'peintre', 'sculpteur', 'musicien', 'gallerie', 'galleriste']
            },
            'sport': {
                'golf': ['golf'],
                'tennis': ['tennis'],
                'yoga': ['yoga', 'pilates'],
                'running': ['course', 'marathon', 'running', 'corsa'],
                'fitness': ['fitness', 'gym', 'training'],
                'ski': ['ski', 'skiing'],
                'football': ['football', 'soccer', 'calcio', 'fuÃŸball'],
                'natation': ['natation', 'swimming', 'nuoto']
            },
            'art_culture': {
                'musees': ['musÃ©e', 'museum', 'museo', 'galerie', 'gallery', 'galleria'],
                'opera': ['opÃ©ra', 'opera', 'oper'],
                'art': ['art', 'arte', 'kunst', 'collectionn', 'collect']
            },
            'voyage': {
                'luxe': ['luxe', 'luxury', 'lusso', 'lujo', 'cruise', 'croisiÃ¨re', 'yacht'],
                'culturel': ['culturel', 'cultural', 'culturale', 'museum', 'musÃ©e'],
                'aventure': ['safari', 'trek', 'aventure', 'adventure']
            },
            'couleurs': {
                'noir': ['noir', 'black', 'nero', 'schwarz'],
                'cognac': ['cognac', 'cognac', 'camel'],
                'beige': ['beige'],
                'bordeaux': ['bordeaux', 'burgundy', 'bordeaux'],
                'navy': ['navy', 'marine', 'blu'],
                'blanc': ['blanc', 'white', 'bianco', 'blanco', 'weiÃŸ'],
                'rose_gold': ['rosÃ© gold', 'rose gold', 'oro rosa'],
                'gris': ['gris', 'gray', 'grey', 'grigio', 'grau']
            },
            'matieres': {
                'cuir': ['cuir', 'leather', 'cuoio', 'pelle', 'leder'],
                'cachemire': ['cachemire', 'cashmere', 'kaschmir'],
                'soie': ['soie', 'silk', 'seta', 'seda', 'seide']
            },
            'regime': {
                'vegetarien': ['vÃ©gÃ©tarien', 'vegetarian', 'vegetariano', 'vegetarisch'],
                'vegane': ['vÃ©gane', 'vegan', 'vegano'],
                'pescetarien': ['pescetarien', 'pescatarian', 'pescetariano']
            },
            'pieces': {
                'sacs': ['sac', 'bag', 'borsa', 'bolso', 'tasche', 'handbag'],
                'portefeuille': ['portefeuille', 'wallet', 'portafoglio', 'cartera', 'geldbÃ¶rse'],
                'chaussures': ['chaussure', 'shoe', 'scarpa', 'zapato', 'schuh'],
                'montres': ['montre', 'watch', 'orologio', 'reloj', 'uhr']
            },
            'motif': {
                'cadeau': ['cadeau', 'gift', 'regalo', 'geschenk'],
                'anniversaire': ['anniversaire', 'birthday', 'compleanno', 'cumpleaÃ±os', 'geburtstag'],
                'mariage': ['mariage', 'wedding', 'matrimonio', 'boda', 'hochzeit'],
                'diplome': ['diplÃ´me', 'graduation', 'laurea', 'diplomation']
            }
        }

    def extract_age(self, text: str) -> str:
        """Extrait l'âge du texte - version améliorée multi-formats"""
        if not isinstance(text, str) or not text.strip():
            return None
        
        text_lower = text.lower()
        age = None
        
        # Patterns multiples pour différents formats
        patterns = [
            r'(\d+)\s*ans?',           # FR: 45 ans
            r'(\d+)\s*years?',         # EN: 45 years
            r'(\d+)\s*anni',           # IT: 45 anni
            r'(\d+)\s*años',           # ES: 45 años
            r'(\d+)\s*jahre',          # DE: 45 Jahre
            r'aged?\s*(\d+)',          # EN: aged 45, age 45
            r'around\s*(\d+)',         # EN: around 45
            r'environ\s*(\d+)',        # FR: environ 45
            r'circa\s*(\d+)',          # IT: circa 45
        ]
        
        # Patterns pour expressions approximatives (early, late, mid)
        approx_patterns = [
            (r'early\s*(\d+)0s', lambda m: int(m.group(1)) * 10 + 2),   # early 50s -> 52
            (r'late\s*(\d+)0s', lambda m: int(m.group(1)) * 10 + 8),    # late 50s -> 58
            (r'mid[- ]?(\d+)0s', lambda m: int(m.group(1)) * 10 + 5),   # mid-50s -> 55
            (r'(\d+)0s', lambda m: int(m.group(1)) * 10 + 5),           # 50s -> 55
        ]
        
        # Essayer les patterns approximatifs d'abord
        for pattern, calc in approx_patterns:
            match = re.search(pattern, text_lower)
            if match:
                age = calc(match)
                break
        
        # Sinon, essayer les patterns standards
        if age is None:
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    try:
                        age = int(matches[0])
                        if 15 <= age <= 100:  # Filtrer les âges valides
                            break
                        else:
                            age = None
                    except ValueError:
                        continue
        
        # Convertir l'âge en tranche
        if age:
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
        """Extrait le budget du texte - version améliorée multi-formats"""
        if not isinstance(text, str) or not text.strip():
            return None

        text_lower = text.lower()
        
        # Patterns améliorés pour capturer plus de formats
        patterns = [
            # Formats avec K
            (r'(\d+)\s*[kK]', 1000),                    # 5K, 5k -> *1000
            (r'(\d+)-(\d+)\s*[kK]', 1000),              # 3-4K -> prend le max
            
            # Formats avec symboles monétaires
            (r'(\d+(?:[.,]\d+)?)\s*[€$£]', 1),          # 5000€, 5000$
            (r'[€$£]\s*(\d+(?:[.,]\d+)?)', 1),          # €5000, $5000
            
            # Formats textuels
            (r'(\d+(?:[.,]\d+)?)\s*euros?', 1),         # 5000 euros
            (r'(\d+(?:[.,]\d+)?)\s*dollars?', 1),       # 5000 dollars
            
            # Multilingue
            (r'budget[o]?\s*(?:de\s*)?(?:around\s*)?(\d+)', 1),   # budget 5000, budgeto
            (r'presupuesto\s*(?:de\s*)?(\d+)', 1),      # ES: presupuesto 5000
            (r'(\d+)\s*(?:très\s*)?(?:flexible|genereux|généreux)', 1),  # 5000 flexible
        ]
        
        budget = None
        
        # Essayer d'abord les ranges (prendre le max)
        range_match = re.search(r'(\d+)\s*[-à]\s*(\d+)\s*[kK€$]?', text_lower)
        if range_match:
            try:
                val1 = int(range_match.group(1))
                val2 = int(range_match.group(2))
                budget = max(val1, val2)
                if budget < 100:
                    budget = budget * 1000
            except ValueError:
                pass
        
        # Sinon essayer les patterns standards
        if budget is None:
            for pattern, multiplier in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    try:
                        # Gérer les tuples (pour les ranges)
                        val = matches[0] if isinstance(matches[0], str) else matches[0][-1]
                        # Nettoyer le nombre (remplacer , par .)
                        val = str(val).replace(',', '').replace('.', '')
                        budget = int(val) * multiplier
                        
                        # Normaliser: si < 100, c'est probablement en K
                        if budget < 100:
                            budget = budget * 1000
                        break
                    except (ValueError, IndexError):
                        continue
        
        # Convertir en tranche
        if budget:
            if budget < 5000:
                return "<5k"
            elif budget < 10000:
                return "5-10k"
            elif budget < 15000:
                return "10-15k"
            elif budget < 25000:
                return "15-25k"
            else:
                return "25k+"

        return None

    def extract_keywords(self, text: str, category: str) -> List[str]:
        """Extrait les mots-clÃ©s d'une catÃ©gorie donnÃ©e"""
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
        """Extrait les villes mentionnÃ©es dans le texte"""
        cities = {
            'paris': 'Paris', 'berlin': 'Berlin', 'milan': 'Milan', 'milano': 'Milan',
            'madrid': 'Madrid', 'london': 'London', 'londres': 'London',
            'new york': 'New_York', 'dubai': 'Dubai', 'tokyo': 'Tokyo',
            'hong kong': 'Hong_Kong', 'singapore': 'Singapore', 'singapour': 'Singapore',
            'maroc': 'Maroc', 'tunisie': 'Tunisie', 'algÃ©rie': 'AlgÃ©rie',
            'Ã©gypte': 'Ã‰gypte', 'egypt': 'Ã‰gypte'
        }

        text_lower = text.lower()
        found_cities = []
        for city_key, city_name in cities.items():
            if city_key in text_lower:
                found_cities.append(city_name)

        return list(set(found_cities))

    def extract_allergies(self, text: str) -> List[str]:
        """Extrait les allergies mentionnÃ©es"""
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
                if keyword in text_lower and ('allergi' in text_lower or 'intolÃ©r' in text_lower):
                    allergies.append(allergy)
                    break

        return list(set(allergies))

    def analyze_full_text(self, text: str) -> Dict:
        """Analyse complÃ¨te du texte"""
        # Validation de l'entree
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        if not text.strip():
            return {
                'age': None,
                'budget': None,
                'genre': [],
                'statut': [],
                'profession': [],
                'sport': [],
                'art_culture': [],
                'voyage': [],
                'couleurs': [],
                'matieres': [],
                'regime': [],
                'pieces': [],
                'motif': [],
                'cities': [],
                'allergies': []
            }
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
