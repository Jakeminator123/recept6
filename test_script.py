#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test-skript för att testa Longevity Receptgeneratorn direkt från kommandoraden.
Detta är ett enkelt sätt att testa API:et utan att behöva starta webbservern.

Användning:
    python test_script.py [textfil] [bildfil]

Exempel:
    python test_script.py ingredienser.txt
    python test_script.py "" kylskap.jpg
"""

import os
import sys
import base64
import requests
from dotenv import load_dotenv
import json

# Ladda miljövariabler
load_dotenv()

# Kontrollera om OpenAI API-nyckeln är satt
if not os.getenv("OPENAI_API_KEY"):
    print("\n⚠️  OPENAI_API_KEY saknas! Skapa en .env-fil med din API-nyckel.")
    print("Exempel:")
    print("OPENAI_API_KEY=sk-din-api-nyckel-här\n")
    sys.exit(1)

def test_with_text_file(filename):
    """Testa API:et med en textfil som innehåller ingredienser"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            ingredients = f.read()
        
        print(f"\n📝 Läser ingredienser från filen: {filename}")
        print(f"Ingredienser: {ingredients[:100]}...\n")
        
        # Anropa OpenAI-API:et direkt
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        prompt = f"""
Nedan finns en lista över tillgängliga varor. Skriv ett recept med fokus på "Longevity" (långt liv) som är:
- Svårighetsgrad: medel
- Måltid: middag
- Antal personer: 2
- Föredraget kök/stilriktning: 
- Kostpreferenser: 

Receptet ska innehålla ingredienser som är kända för att främja ett långt och hälsosamt liv, som till exempel:
- Baljväxter (bönor, linser)
- Fullkorn
- Nötter och frön
- Bär och färska frukter
- Gröna bladgrönsaker
- Fisk rik på omega-3 (om inte vegetariskt/veganskt)
- Fermenterade livsmedel
- Olivolja och andra hälsosamma fetter

Struktur för svaret:
1) Förslag på rätt:
   - En kort kommentar om vad rätten heter, vilket land/ursprung den har, och varför den är bra för ett långt liv.

2) Gör såhär:
   - En mycket kortfattad beskrivning av hur man tillagar rätten.

3) Ingredienser du har:
   - Ange vilka av de tillgängliga varorna som används och hur mycket.

4) Har du?:
   - Lista eventuella småingredienser (salt, peppar, tomatpuré etc.) som inte är avgörande för rätten.

5) Longevity-fördelar:
   - En kort förklaring om hur ingredienserna i rätten bidrar till ett långt och hälsosamt liv.

Ditt svar ska vara på svenska.

Lista över tillgängliga varor:
{ingredients}
"""
        
        print("🔄 Genererar recept, vänta...")
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        recipe = response["choices"][0]["message"]["content"]
        
        print("\n✅ Recept genererat!\n")
        print("-" * 80)
        print(recipe)
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Fel vid generering av recept: {e}")

def test_with_image(filename):
    """Testa API:et med en bild på kylskåpet"""
    try:
        with open(filename, 'rb') as f:
            image_data = f.read()
        
        print(f"\n🖼️  Analyserar bild från filen: {filename}")
        
        # Konvertera bilddata till base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Anropa OpenAI-API:et direkt
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        print("🔍 Analyserar bilden, vänta...")
        image_analysis = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Detta är en bild av mitt kylskåp. Lista alla ingredienser och råvaror du kan identifiera i bilden. Var specifik och detaljerad. Lista råvarorna på svenska."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        
        ingredients = image_analysis["choices"][0]["message"]["content"]
        
        print(f"\n🧪 Identifierade ingredienser: {ingredients[:100]}...\n")
        
        # Generera recept baserat på identifierade ingredienser
        prompt = f"""
Nedan finns en lista över tillgängliga varor. Skriv ett recept med fokus på "Longevity" (långt liv) som är:
- Svårighetsgrad: medel
- Måltid: middag
- Antal personer: 2
- Föredraget kök/stilriktning: 
- Kostpreferenser: 

Receptet ska innehålla ingredienser som är kända för att främja ett långt och hälsosamt liv, som till exempel:
- Baljväxter (bönor, linser)
- Fullkorn
- Nötter och frön
- Bär och färska frukter
- Gröna bladgrönsaker
- Fisk rik på omega-3 (om inte vegetariskt/veganskt)
- Fermenterade livsmedel
- Olivolja och andra hälsosamma fetter

Struktur för svaret:
1) Förslag på rätt:
   - En kort kommentar om vad rätten heter, vilket land/ursprung den har, och varför den är bra för ett långt liv.

2) Gör såhär:
   - En mycket kortfattad beskrivning av hur man tillagar rätten.

3) Ingredienser du har:
   - Ange vilka av de tillgängliga varorna som används och hur mycket.

4) Har du?:
   - Lista eventuella småingredienser (salt, peppar, tomatpuré etc.) som inte är avgörande för rätten.

5) Longevity-fördelar:
   - En kort förklaring om hur ingredienserna i rätten bidrar till ett långt och hälsosamt liv.

Ditt svar ska vara på svenska.

Lista över tillgängliga varor:
{ingredients}
"""
        
        print("🔄 Genererar recept, vänta...")
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        recipe = response["choices"][0]["message"]["content"]
        
        print("\n✅ Recept genererat!\n")
        print("-" * 80)
        print(recipe)
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Fel vid generering av recept: {e}")

def main():
    """Huvudfunktion"""
    print("\n🍽️  Longevity Receptgenerator - Testskript 🍽️\n")
    
    # Kontrollera att det finns minst ett argument
    if len(sys.argv) < 2:
        print("Användning:")
        print("  python test_script.py [textfil] [bildfil]")
        print("\nExempel:")
        print("  python test_script.py ingredienser.txt")
        print("  python test_script.py \"\" kylskap.jpg\n")
        return
    
    # Hantera textfil
    if len(sys.argv) >= 2 and sys.argv[1]:
        test_with_text_file(sys.argv[1])
    
    # Hantera bildfil
    if len(sys.argv) >= 3 and sys.argv[2]:
        test_with_image(sys.argv[2])

if __name__ == "__main__":
    main() 