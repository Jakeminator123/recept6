from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

# Konfigurera OpenAI-klienten
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sökväg till testbild
image_path = "kyl.jpg"  # Lägg din testbild i samma mapp som skriptet

# Läs in och koda bilden
def encode_image(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

try:
    base64_image = encode_image(image_path)
    print(f"✅ Bild läst och kodad. Längd: {len(base64_image)} tecken")
except Exception as e:
    print(f"❌ Kunde inte läsa bilden: {e}")
    exit(1)

# Anropa API med bild
try:
    response = client.chat.completions.create(
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
    print(f"Svar: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API-anrop misslyckades: {e}") 