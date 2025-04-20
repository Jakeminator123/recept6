import os
import base64
import traceback
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
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

# Montera statiska filer
app.mount("/static", StaticFiles(directory="."), name="static")

# Konfigurera OpenAI API-klient
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
if not api_key:
    print("Varning: OPENAI_API_KEY miljövariabel är inte inställd")
else:
    print(f"API-nyckel hittad: {api_key[:5]}...{api_key[-4:]}")

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return {"message": f"Kunde inte läsa index.html: {str(e)}"}

@app.get("/styles.css")
async def get_css():
    return FileResponse("styles.css", media_type="text/css")

@app.get("/script.js")
async def get_js():
    return FileResponse("script.js", media_type="application/javascript")

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
        print(f"Begäran mottagen: choice={choice}, filnamn={file.filename}, filstorlek={file.size if hasattr(file, 'size') else 'okänd'}")
        
        # Läs filinnehåll
        varulista = ""
        file_content = await file.read()
        print(f"Fil läst, storlek: {len(file_content)} bytes")
        
        # Behandla baserat på val
        if choice == "1":  # Textfil med inventarielista
            try:
                varulista = file_content.decode("utf-8")
                print(f"Textfil avkodad, längd: {len(varulista)} tecken")
            except UnicodeDecodeError:
                print("Fel vid avkodning av textfil")
                raise HTTPException(status_code=400, detail="Filen är inte en giltig textfil")
                
        elif choice == "2":  # Bild på kylskåp
            try:
                # Konvertera bilddata till base64
                base64_image = base64.b64encode(file_content).decode('utf-8')
                print(f"Bild kodad till base64, längd: {len(base64_image)} tecken")
                
                # Verifiera att API-nyckeln är inställd
                if not api_key:
                    print("Saknar API-nyckel")
                    raise HTTPException(status_code=500, detail="OpenAI API-nyckel saknas")
                
                # Skriv ut information om bilden
                print(f"Skickar bild till OpenAI, filtyp: {file.content_type}, bildstorlek: {len(file_content)}")
                
                # Analysera bild med OpenAI
                try:
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
                    print(f"Bilden analyserad framgångsrikt, svarslängd: {len(varulista)} tecken")
                    
                except Exception as api_error:
                    print(f"OpenAI API-fel: {str(api_error)}")
                    error_details = str(api_error)
                    traceback.print_exc()
                    raise HTTPException(status_code=500, detail=f"Fel vid bildanalys: {error_details}")
            
            except Exception as img_error:
                print(f"Bildhanteringsfel: {str(img_error)}")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Fel vid bildhantering: {str(img_error)}")
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
        print("Skickar prompt till GPT-4...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # använder GPT-4 för bättre resultat
            messages=[{"role": "user", "content": prompt}]
        )

        # Hämta och returnera svaret
        recipe = response.choices[0].message.content
        print(f"Recept genererat framgångsrikt, längd: {len(recipe)} tecken")
        
        return {"recipe": recipe}
        
    except Exception as e:
        print(f"Oväntat fel: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Starta API-servern
    port = int(os.getenv("PORT", 8000))
    print(f"Startar server på port {port}...")
    uvicorn.run("api:app", host="0.0.0.0", port=port)