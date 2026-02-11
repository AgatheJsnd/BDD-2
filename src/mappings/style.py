"""
Module Style - Pièces, Couleurs, Matières, Sensibilité, Tailles
Partie de la taxonomie LVMH complète
"""

# ============================================================================
# PIÈCES FAVORITES
# ============================================================================

PIECES_MAPPING = {
    # Sacs
    "Sac_main": ["sac à main", "handbag", "sac", "bag"],
    "Sac_dos": ["sac à dos", "backpack", "sac de randonnée"],
    "Sac_voyage": ["sac de voyage", "travel bag", "valise", "bagage"],
    "Pochette": ["pochette", "clutch", "minaudière"],
    
    # Chaussures
    "Baskets": ["baskets", "sneakers", "tennis", "running shoes"],
    "Escarpins": ["escarpins", "pumps", "talons", "heels"],
    "Bottes": ["bottes", "boots", "cuissardes"],
    "Bottines": ["bottines", "ankle boots", "chelsea boots"],
    "Mocassins": ["mocassins", "loafers", "slippers"],
    "Derbies": ["derbies", "richelieus", "oxford", "brogues"],
    "Sandales": ["sandales", "sandals", "nu-pieds"],
    "Talons": ["talons", "high heels", "stilettos"],
    
    # Manteaux
    "Trench": ["trench", "trench coat", "imperméable"],
    "Manteau_laine": ["manteau laine", "wool coat", "manteau"],
    "Doudoune": ["doudoune", "puffer jacket", "down jacket"],
    "Cape": ["cape", "poncho"],
    "Manteau_long": ["manteau long", "long coat", "pardessus"],
    "Veste_legere": ["veste légère", "light jacket", "blazer"],
    
    # Robes
    "Robe_courte": ["robe courte", "short dress", "mini dress"],
    "Robe_longue": ["robe longue", "long dress", "maxi dress"],
    "Robe_soiree": ["robe de soirée", "evening dress", "gown"],
    "Robe_cocktail": ["robe de cocktail", "cocktail dress"],
    
    # Costumes
    "Costume_classique": ["costume", "suit", "tailleur"],
    "Costume_business": ["costume business", "business suit"],
    "Smoking": ["smoking", "tuxedo", "tux"],
    
    # Accessoires
    "Chapeaux": ["chapeau", "hat", "casquette", "cap", "béret"],
    "Ceintures": ["ceinture", "belt"],
    "Foulards": ["foulard", "scarf", "écharpe", "châle"],
    "Lunettes": ["lunettes", "glasses", "sunglasses", "lunettes de soleil"],
    "Bijoux": ["bijoux", "jewelry", "jewellery", "bague", "collier", "bracelet", "boucles d'oreilles"],
    "Gants": ["gants", "gloves"],
    "Montres": ["montre", "watch", "timepiece"]
}

# ============================================================================
# COULEURS ENRICHIES
# ============================================================================

COULEURS_ADVANCED = {
    # Neutres & Intemporelles
    "Noir": ["noir", "black", "noire", "noirs", "sombre", "ébène"],
    "Blanc": ["blanc", "white", "ivoire", "ivory", "neige", "écru"],
    "Beige": ["beige", "écru", "crème", "cream", "sable", "nude", "taupe"],
    "Gris": ["gris", "grey", "gray", "anthracite", "argent", "silver", "charbon"],
    "Bleu_marine": ["navy", "bleu marine", "marine", "dark blue", "bleu nuit"],
    
    # Tons Chauds
    "Cognac": ["cognac", "caramel", "tan", "camel", "marron clair"],
    "Marron": ["marron", "brown", "chocolat", "brun"],
    "Bordeaux": ["bordeaux", "burgundy", "vin", "rouge sombre", "marsala"],
    "Rouge": ["rouge", "red", "vermillon", "carmin", "écarlate"],
    "Orange": ["orange", "orangé", "corail", "coral"],
    
    # Tons Froids
    "Bleu": ["bleu", "blue", "azur", "cyan"],
    "Vert": ["vert", "green", "émeraude", "emerald"],
    "Kaki": ["kaki", "khaki", "olive"],
    "Violet": ["violet", "purple", "mauve", "prune"],
    
    # Pastels
    "Rose_poudre": ["rose poudré", "powder pink", "rose pale", "blush"],
    "Bleu_ciel": ["bleu ciel", "sky blue", "bleu pastel"],
    "Lavande": ["lavande", "lavender", "lilas"],
    "Menthe": ["menthe", "mint", "vert d'eau"],
    
    # Métalliques
    "Or": ["or", "gold", "doré", "golden"],
    "Argent": ["argent", "silver", "argenté"],
    "Bronze": ["bronze", "bronzé", "cuivré", "copper"],
    "Rose_gold": ["rose gold", "or rose", "rosé", "pink gold"]
}

# ============================================================================
# MATIÈRES ENRICHIES
# ============================================================================

MATIERES_ADVANCED = {
    # Matières Naturelles
    "Cuir": ["cuir", "leather", "veau", "agneau", "vachette", "peau"],
    "Daim": ["daim", "suede", "nubuck", "velours"],
    "Cachemire": ["cachemire", "cashmere", "mohair", "angora"],
    "Soie": ["soie", "silk", "satin"],
    "Laine": ["laine", "wool", "mérinos", "merino"],
    "Coton": ["coton", "cotton"],
    "Lin": ["lin", "linen"],
    "Denim": ["denim", "jean", "jeans"],
    
    # Matières Premium
    "Cuir_exotique": ["cuir exotique", "exotic leather", "python", "crocodile", "alligator", "autruche", "ostrich"],
    "Fourrure": ["fourrure", "fur", "vison", "mink", "renard", "fox"],
    "Velours": ["velours", "velvet"],
    "Tweed": ["tweed"],
    "Flanelle": ["flanelle", "flannel"],
    
    # Matières Techniques
    "Nylon": ["nylon"],
    "Polyester": ["polyester"],
    "Gore_Tex": ["gore-tex", "goretex", "imperméable", "waterproof"],
    "Matieres_sport": ["matière sport", "technical fabric", "performance fabric", "stretch"],
    
    # Matières Alternatives
    "Vegan": ["vegan", "végane", "faux cuir", "simili cuir", "cuir végétal"],
    "Recyclees": ["recyclé", "recycled", "upcyclé", "upcycled", "éco-responsable"],
    "Eco_responsables": ["éco-responsable", "sustainable", "durable", "bio", "organic"]
}

# ============================================================================
# SENSIBILITÉ MODE
# ============================================================================

SENSIBILITE_MODE = {
    "Tendance": ["tendance", "trendy", "à la mode", "fashion forward", "avant-garde", "mode", "fashion"],
    "Intemporel": ["intemporel", "timeless", "classique chic", "élégant", "indémodable"],
    "Classique": ["classique", "classic", "traditionnel", "traditional", "sobre"]
}

# ============================================================================
# TAILLES / MENSURATIONS
# ============================================================================

TAILLES_MAPPING = {
    # Taille vêtements
    "XXS": ["xxs", "très petit", "extra small"],
    "XS": ["xs", "extra small", "petit"],
    "S": ["s", "small", "taille s"],
    "M": ["m", "medium", "taille m", "moyen"],
    "L": ["l", "large", "taille l", "grand"],
    "XL": ["xl", "extra large", "très grand"],
    "Sur_mesure": ["sur mesure", "bespoke", "custom", "made to measure", "couture"],
    
    # Pointure
    "35_37": ["35", "36", "37", "petite pointure"],
    "38_40": ["38", "39", "40", "pointure moyenne"],
    "41_43": ["41", "42", "43", "grande pointure"],
    "44_46": ["44", "45", "46", "très grande pointure"],
    
    # Coupe préférée
    "Ajustee": ["ajusté", "fitted", "slim", "près du corps", "cintrée"],
    "Oversize": ["oversize", "oversized", "ample", "large", "loose"],
    "Standard": ["standard", "regular", "normale", "classique"],
    
    # Morphologie
    "Fine": ["silhouette fine", "mince", "slim", "petite"],
    "Moyenne": ["silhouette moyenne", "normale", "average"],
    "Athletique": ["silhouette athlétique", "sportive", "athletic", "musclée"],
    "Genereuse": ["silhouette généreuse", "ronde", "curvy", "plus size"]
}
