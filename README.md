# Longevity Receptgenerator

En Shopify-applikation som genererar hälsosamma "longevity" recept baserat på tillgängliga ingredienser.

## Funktioner

- Ladda upp en textfil med ingredienser eller en bild på ditt kylskåp
- Ange måltidstyp, svårighetsgrad och andra preferenser
- Få ett receptförslag anpassat för långt och hälsosamt liv

## Snabbstart 🚀

För att komma igång snabbt, kör:

```
python all_in_one.py
```

Detta startar både API-servern och webbservern, och öppnar webbläsaren automatiskt.

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
- `test_script.py` - Kommandoradsverktyg för att testa API direkt
- `setup.py` - Hjälpskript för att konfigurera och starta projektet
- `all_in_one.py` - Kombinerad server som kör både frontend och backend

## Installation och körning

### Första gången

Kör setup-skriptet för att konfigurera din miljö:

```
python setup.py
```

Detta kommer att:
- Skapa en `.env`-fil för din API-nyckel
- Installera alla nödvändiga beroenden
- Skapa testfiler för att testa API:et
- Hjälpa dig konfigurera din OpenAI API-nyckel
- Erbjuda att starta alla tjänster

### Backend (API)

För att endast starta API-servern:

```
python api.py
```

Servern startar på http://localhost:8000

### Frontend

För att endast starta webbservern:

```
python serve.py
```

Detta öppnar webbläsaren med förhandsgranskningssidan.

### Direkttestning av API

För att testa API:et direkt från kommandoraden:

```
python test_script.py testdata/ingredienser.txt
```

För att testa med en bild:

```
python test_script.py "" kylskap.jpg
```

## Deployment

### Backend på Render.com

1. Skapa ett nytt Web Service på Render.com
2. Koppla till GitHub-repositoryt
3. Ange följande inställningar:
   - Runtime: Docker
   - Environment variables: Lägg till `OPENAI_API_KEY`

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