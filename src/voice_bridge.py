import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.voice_transcriber import VoiceTranscriber

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No audio file provided"}))
        return

    audio_path = sys.argv[1]
    
    try:
        # Initialize transcriber
        transcriber = VoiceTranscriber()
        
        # Read audio file
        with open(audio_path, 'rb') as f:
            audio_bytes = f.read()
            
        # Process recording
        result = transcriber.process_voice_recording(audio_bytes)
        
        # Output JSON for Node.js
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    main()
