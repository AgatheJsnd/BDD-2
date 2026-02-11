"""
Script de test pour vérifier l'installation de l'enregistrement vocal
"""
import sys
import os

def test_imports():
    """Teste que tous les modules nécessaires sont installés"""
    print("🧪 Test des imports...\n")
    
    tests = {
        "Streamlit": "streamlit",
        "Deepgram SDK": "deepgram",
        "Mistral AI": "mistralai",
        "Audio Recorder": "audio_recorder_streamlit",
        "Pydub": "pydub",
        "Plotly": "plotly",
        "Pandas": "pandas",
        "Python-dotenv": "dotenv"
    }
    
    results = []
    
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"✅ {name:20} : OK")
            results.append(True)
        except ImportError as e:
            print(f"❌ {name:20} : MANQUANT")
            print(f"   → Erreur: {e}")
            results.append(False)
    
    print(f"\n{'='*50}")
    print(f"Résultat : {sum(results)}/{len(results)} modules installés")
    print(f"{'='*50}\n")
    
    return all(results)


def test_env_vars():
    """Teste que les variables d'environnement sont configurées"""
    print("🔑 Test des clés API...\n")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    mistral_key = os.getenv("MISTRAL_API_KEY")
    deepgram_key = os.getenv("DEEPGRAM_API_KEY")
    
    if mistral_key:
        print(f"✅ MISTRAL_API_KEY  : Configurée ({mistral_key[:10]}...)")
    else:
        print("❌ MISTRAL_API_KEY  : Non configurée")
    
    if deepgram_key:
        print(f"✅ DEEPGRAM_API_KEY : Configurée ({deepgram_key[:10]}...)")
    else:
        print("⚠️  DEEPGRAM_API_KEY : Non configurée (requis pour la transcription)")
    
    print(f"\n{'='*50}")
    
    return mistral_key is not None


def test_voice_module():
    """Teste que le module voice_transcriber est accessible"""
    print("\n📦 Test du module voice_transcriber...\n")
    
    try:
        from src.voice_transcriber import VoiceTranscriber
        print("✅ Module voice_transcriber importé avec succès")
        
        # Tester l'initialisation
        transcriber = VoiceTranscriber()
        print("✅ VoiceTranscriber initialisé")
        
        print(f"\n{'='*50}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import : {e}")
        print(f"\n{'='*50}")
        return False


def main():
    """Fonction principale de test"""
    print("\n" + "="*50)
    print("🎤 TEST D'INSTALLATION - ENREGISTREMENT VOCAL")
    print("="*50 + "\n")
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    # Test 2: Variables d'environnement
    env_ok = test_env_vars()
    
    # Test 3: Module vocal
    module_ok = test_voice_module()
    
    # Résumé final
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    print(f"Imports        : {'✅ OK' if imports_ok else '❌ ÉCHEC'}")
    print(f"Variables env. : {'✅ OK' if env_ok else '⚠️  PARTIEL'}")
    print(f"Module vocal   : {'✅ OK' if module_ok else '❌ ÉCHEC'}")
    print("="*50 + "\n")
    
    if imports_ok and module_ok:
        print("🎉 INSTALLATION RÉUSSIE !")
        print("\n📝 Prochaines étapes :")
        print("   1. Ajoutez votre DEEPGRAM_API_KEY dans .env")
        print("      → Obtenez $200 gratuits sur https://console.deepgram.com/")
        print("   2. Lancez l'application : streamlit run app.py")
        print("   3. Connectez-vous avec : vendeur / vendeur123")
        print("\n✨ Vous êtes prêt à utiliser l'enregistrement vocal !\n")
        return 0
    else:
        print("❌ INSTALLATION INCOMPLÈTE")
        print("\n🔧 Actions requises :")
        if not imports_ok:
            print("   → Exécutez : pip install -r requirements.txt")
        if not module_ok:
            print("   → Vérifiez que src/voice_transcriber.py existe")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
