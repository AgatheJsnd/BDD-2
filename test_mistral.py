import os
from mistralai import Mistral
from dotenv import load_dotenv
import sys

# Load env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

print(f"API Key found: {bool(api_key)}")
if not api_key:
    sys.exit(1)

client = Mistral(api_key=api_key)

try:
    print("Sending request to Mistral...")
    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello LVMH' in JSON format like {\"message\": \"Hello\"}",
            },
        ]
    )
    print("Response received:")
    print(chat_response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
