#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ett all-in-one skript för Longevity Receptgenerator.
Detta skript kombinerar både backend-API och frontend-server i en enda fil
för att göra det enkelt att starta hela applikationen med ett enda kommando.

Användning:
    python all_in_one.py

Detta startar både API-servern och webbservern och öppnar webbläsaren automatiskt.
"""

import os
import sys
import time
import threading
import webbrowser
import multiprocessing
import http.server
import socketserver
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# --------------------------------------------------------
# Konfigurera miljö
# --------------------------------------------------------

# Ladda miljövariabler
load_dotenv()

# Konfigurera portar
API_PORT = int(os.getenv("PORT", 8000))
WEB_PORT = 8080

# Kontrollera att OpenAI API-nyckeln är satt
if not os.getenv("OPENAI_API_KEY"):
    print("\n⚠️ OPENAI_API_KEY saknas! Skapa en .env-fil med din API-nyckel.")
    print("Exempel:")
    print("OPENAI_API_KEY=sk-din-api-nyckel-här\n")
    
    # Försök automatiskt skapa .env-fil från env.example
    env_example_path = Path('env.example')
    env_path = Path('.env')
    
    if env_example_path.exists() and not env_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print("✅ .env-fil skapad från env.example")
        print("⚠️ Öppna .env-filen och lägg till din OpenAI API-nyckel\n")
    
    choice = input("Vill du fortsätta ändå? Vissa funktioner kommer inte att fungera. (j/n): ")
    if choice.lower() not in ('j', 'ja', 'y', 'yes'):
        sys.exit(1)

# --------------------------------------------------------
# API-server (backend)
# --------------------------------------------------------

def start_api_server():
    """Starta FastAPI-servern för backend"""
    try:
        # Importera nödvändiga bibliotek för API-servern
        import base64
        from fastapi import FastAPI, File, Form, UploadFile, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
        import openai
    except ImportError:
        print("❌ Nödvändiga bibliotek saknas för API-servern. Kör 'pip install -r requirements.txt'")
        sys.exit(1)
    
    # Skapa FastAPI-appen
    app = FastAPI(title="Longevity Recept API")
    
    # Konfigurera CORS för att tillåta förfrågningar från frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Konfigurera OpenAI API-nyckel
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Hemstartsida
    @app.get("/")
    async def root():
        return {"message": "Välkommen till Longevity Recept API"}
    
    # API-slutpunkt för att generera recept
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
                # Kontrollera att API-nyckeln är satt
                if not openai.api_key:
                    raise HTTPException(status_code=500, detail="OpenAI API-nyckel saknas")
                
                # Konvertera bilddata till base64
                base64_image = base64.b64encode(file_content).decode('utf-8')
                
                # Analysera bild med OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "user",
                            "content": "Detta är en bild av mitt kylskåp. Lista alla ingredienser och råvaror du kan identifiera i bilden. Var specifik och detaljerad. Lista råvarorna på svenska."
                        }
                    ],
                    image=base64_image
                )
                
                # Extrahera listan med råvaror från svaret
                varulista = response["choices"][0]["message"]["content"]
            
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
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            # Hämta och returnera svaret
            recipe = response["choices"][0]["message"]["content"]
            
            return {"recipe": recipe}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # Starta API-servern
    print(f"🚀 Startar API-server på http://localhost:{API_PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)

# --------------------------------------------------------
# Webbserver (frontend)
# --------------------------------------------------------

def start_web_server():
    """Starta en enkel HTTP-server för frontend"""
    # Skapa en enkel HTTP-server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", WEB_PORT), handler) as httpd:
            print(f"🌐 Webbserver igång på http://localhost:{WEB_PORT}")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Port används redan
            print(f"❌ Port {WEB_PORT} används redan. Välj en annan port.")
        else:
            print(f"❌ Fel vid start av webbserver: {e}")
        sys.exit(1)

def open_browser():
    """Öppna webbläsaren efter en kort fördröjning"""
    time.sleep(2)  # Vänta lite så att servern hinner starta
    print("🔍 Öppnar webbläsare...")
    webbrowser.open(f"http://localhost:{WEB_PORT}/preview.html")

# --------------------------------------------------------
# Huvudprogram
# --------------------------------------------------------

def main():
    """Huvudfunktion"""
    print("\n🍽️  Longevity Receptgenerator - All-in-One 🍽️\n")
    
    # Kontrollera att API-servern kan startas
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("❌ FastAPI och/eller uvicorn saknas. Installera beroenden med:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Starta webbservern i en separat tråd
    web_server_thread = threading.Thread(target=start_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()
    
    # Öppna webbläsaren i en separat tråd
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Starta API-servern i huvudtråden (kommer att blockera)
    start_api_server()

if __name__ == "__main__":
    # Använd multiprocessing för att hantera CTRL+C korrekt
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Avslutar Longevity Receptgenerator...")
        sys.exit(0) 