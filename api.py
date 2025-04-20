import os
import base64
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn
from dotenv import load_dotenv

# Ladda miljövariabler från .env-fil
load_dotenv()

app = FastAPI(title="Longevity Recept API")

# Konfigurera CORS för att tillåta förfrågningar från frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ersätt med specifika domäner i produktion
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfigurera OpenAI API-klient
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Varning: OPENAI_API_KEY miljövariabel är inte inställd")

@app.get("/")
async def root():
    return {"message": "Välkommen till Longevity Recept API"}

@app.post("/generate")
async def generate_recipe(
    choice: str = Form(...),
    file: UploadFile = File(...),
    difficulty: str = Form(...),
    meal_type: str = Form(...),
    num_people: str = Form(...),
    cuisine_pref: Optional[str] = Form(""),
    dietary_pref: Optional[str] = Form(""),
):
    """
    Generera ett longevity-recept baserat på användarinmatning och en fil med råvaror.
    
    - choice: 1 för textfil med inventarielista, 2 för bild på kylskåp
    - file: Uppladdad fil (txt eller bild)
    - difficulty: Svårighetsgrad (enkel, medel, svår)
    - meal_type: Måltidstyp (frukost, lunch, middag)
    - num_people: Antal personer
    - cuisine_pref: Föredraget kök (valfritt)
    - dietary_pref: Kostpreferenser (valfritt)
    """
    try:
        # Läs filinnehåll
        varulista = ""
        file_content = await file.read()
        
        # Behandla baserat på val
        if choice == "1":  # Textfil med inventarielista
            try:
                varulista = file_content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="Filen är inte en giltig textfil")
                
        elif choice == "2":  # Bild på kylskåp
            # Konvertera bilddata till base64
            base64_image = base64.b64encode(file_content).decode('utf-8')
            
            # Analysera bild med OpenAI
            response = client.chat.completions.create(
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
                ],
                max_tokens=500
            )
            
            # Extrahera listan med råvaror från svaret
            varulista = response.choices[0].message.content
        
        else:
            raise HTTPException(status_code=400, detail="Ogiltigt val")

        # Skapa prompt med användarinmatning
        prompt = f"""
Nedan finns en lista över tillgängliga varor. Skriv ett recept med fokus på "Longevity" (långt liv) som är:
- Svårighetsgrad: {difficulty}
- Måltid: {meal_type}
- Antal personer: {num_people}
- Föredraget kök/stilriktning: {cuisine_pref}
- Kostpreferenser: {dietary_pref}

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
{varulista}
"""

        # Skicka frågan till modellen
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # använder GPT-4 för bättre resultat
            messages=[{"role": "user", "content": prompt}]
        )

        # Hämta och returnera svaret
        recipe = response.choices[0].message.content
        
        return {"recipe": recipe}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Starta API-servern
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)