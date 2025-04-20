import os
import base64
import openai
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

# Konfigurera OpenAI API-nyckel
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("API-nyckel saknas! Kontrollera .env-filen")
    exit(1)

# Sökväg till testbild
image_path = "kyl.jpg"  # Lägg din testbild i samma mapp som skriptet

# Läs in och koda bilden
try:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        print(f"✅ Bild läst och kodad. Längd: {len(base64_image)} tecken")
except Exception as e:
    print(f"❌ Kunde inte läsa bilden: {e}")
    exit(1)

# Kontrollera OpenAI-version
print(f"OpenAI-version: {openai.__version__}")

# Anpassa anrop baserat på version
if openai.__version__.startswith("0."):
    # Anrop för äldre version (0.x.x)
    print("Använder format för OpenAI 0.x.x")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Testa denna modell
            messages=[
                {
                    "role": "user", 
                    "content": "Beskriv kort vad som finns i det här kylskåpet."
                }
            ],
            image=base64_image
        )
        print("✅ API-anrop lyckades!")
        print(f"Svar: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"❌ API-anrop misslyckades: {e}")
        
        # Testa alternativ modell
        try:
            print("\nTestar med alternativ modell...")
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Testa med vanlig gpt-4
                messages=[
                    {
                        "role": "user", 
                        "content": "Beskriv kort vad som finns i det här kylskåpet."
                    }
                ],
                image=base64_image
            )
            print("✅ API-anrop lyckades med alternativ modell!")
            print(f"Svar: {response['choices'][0]['message']['content']}")
        except Exception as e:
            print(f"❌ Även alternativt anrop misslyckades: {e}")
else:
    # Anrop för nyare version (1.x.x)
    print("Använder format för OpenAI 1.x.x")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Beskriv kort vad som finns i det här kylskåpet."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        print("✅ API-anrop lyckades!")
        print(f"Svar: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"❌ API-anrop misslyckades: {e}")
        
        # Testa alternativ modell
        try:
            print("\nTestar med alternativ modell...")
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Testa med gpt-4o istället
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Beskriv kort vad som finns i det här kylskåpet."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            print("✅ API-anrop lyckades med alternativ modell!")
            print(f"Svar: {response['choices'][0]['message']['content']}")
        except Exception as e:
            print(f"❌ Även alternativt anrop misslyckades: {e}")