# Longevity Receptgenerator

En Shopify-applikation som genererar hälsosamma "longevity" recept baserat på tillgängliga ingredienser.

## Funktioner

- Ladda upp en textfil med ingredienser eller en bild på ditt kylskåp
- Ange måltidstyp, svårighetsgrad och andra preferenser
- Få ett receptförslag anpassat för långt och hälsosamt liv

## Projektstruktur

- `index.html` - Frontend-gränssnitt
- `styles.css` - Stilmallar
- `script.js` - Frontend-logik
- `api.py` - Backend API (FastAPI)
- `requirements.txt` - Python-beroenden
- `Dockerfile` - För deployment av backend
- `preview.html` - Förhandsgranskning av applikationen
- `serve.py` - Lokal utvecklingsserver
- `mock_api.js` - Simulerar API-svar för testning utan backend

## Installation och körning

### Backend (API)

1. Installera beroenden:
   ```
   pip install -r requirements.txt
   ```

2. Skapa en `.env`-fil baserad på `env.example` och ange din OpenAI API-nyckel:
   ```
   cp env.example .env
   ```

3. Starta API-servern:
   ```
   python api.py
   ```
   
   Servern startar på http://localhost:8000

### Frontend

Öppna `index.html` i en webbläsare eller ladda upp filerna till en webbserver.

### Förhandsgranskning

För att enkelt förhandsvisa hur applikationen kommer att se ut på din Shopify-sida:

1. Starta den lokala utvecklingsservern:
   ```
   python serve.py
   ```

2. Din webbläsare öppnas automatiskt med förhandsgranskningen på http://localhost:8080/preview.html

3. **Teståtkomst utan backend**: Förhandsgranskningen använder ett mockup-API så att du kan testa hela flödet utan att behöva starta backend-servern.

## Deployment

### Backend på Render.com

1. Skapa ett nytt Web Service på Render.com
2. Koppla till GitHub-repositoryt
3. Ange följande inställningar:
   - Runtime: Docker
   - Environment variables: Lägg till OPENAI_API_KEY

### Frontend på Shopify

1. Ladda upp frontend-filerna (index.html, styles.css, script.js) till en webbserver
2. Skapa en app-extension i din Shopify-butik
3. Använd iframe för att bädda in applikationen:
   ```html
   <iframe src="https://din-webbplats.se/recept" width="100%" height="650px" frameborder="0"></iframe>
   ```

## Utveckling

### Mock API för testning

För att testa frontend utan att behöva köra backend:
- `mock_api.js` fångar anrop till API:et och returnerar exempelsvar
- Detta aktiveras automatiskt i utvecklingsmiljö (localhost)
- Perfekt för att snabbt testa UI och användarupplevelse

### API-dokumentation

När backend-servern körs, besök `/docs` för fullständig API-dokumentation (genererad av Swagger UI).

## Licensiering

Detta projekt är inte öppen källkod och får endast användas med tillstånd.

## Kontakt

För frågor, kontakta [din e-postadress]. 