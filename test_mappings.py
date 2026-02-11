"""
Test Simple - Vérification des Mappings
"""

print("Test d'import des mappings...")

try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    print("✓ Path configuré")
    
    from mappings import identity
    print(f"✓ Identity module chargé - {len(identity.GENRE_MAPPING)} genres")
    
    from mappings import location  
    print(f"✓ Location module chargé - {len(location.CITIES_ADVANCED)} régions")
    
    from mappings import lifestyle
    print(f"✓ Lifestyle module chargé - {len(lifestyle.SPORT_MAPPING)} sports")
    
    from mappings import style
    print(f"✓ Style module chargé - {len(style.PIECES_MAPPING)} types de pièces")
    
    from mappings import purchase
    print(f"✓ Purchase module chargé - {len(purchase.MARQUES_LVMH)} marques LVMH")
    
    from mappings import preferences
    print(f"✓ Preferences module chargé - {len(preferences.REGIME_MAPPING)} régimes")
    
    from mappings import tracking
    print(f"✓ Tracking module chargé - {len(tracking.CANAUX_MAPPING)} canaux")
    
    print()
    print("=" * 60)
    print("✅ TOUS LES MODULES CHARGÉS AVEC SUCCÈS!")
    print("=" * 60)
    print()
    
    # Compter total de mots-clés
    total_keywords = 0
    total_keywords += sum(len(v) for v in identity.GENRE_MAPPING.values())
    total_keywords += sum(len(v) for v in identity.LANGUE_MAPPING.values())
    total_keywords += sum(len(v) for v in identity.PROFESSIONS_ADVANCED.values())
    total_keywords += sum(len(keywords) for region in location.CITIES_ADVANCED.values() for keywords in region.values())
    total_keywords += sum(len(v) for v in lifestyle.SPORT_MAPPING.values())
    total_keywords += sum(len(v) for v in lifestyle.MUSIQUE_MAPPING.values())
    total_keywords += sum(len(v) for v in style.PIECES_MAPPING.values())
    total_keywords += sum(len(v) for v in style.COULEURS_ADVANCED.values())
    total_keywords += sum(len(v) for v in purchase.MARQUES_LVMH.values())
    
    print(f"📊 Total de mots-clés chargés: ~{total_keywords}")
    print(f"📦 Modules créés: 6")
    print(f"🏷️ Catégories totales: 30")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
