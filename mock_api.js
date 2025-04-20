// Mock API för att testa receptgeneratorn utan backend
(function() {
    // Kontrollera om vi redan har ersatt fetch
    if (window.originalFetch) return;
    
    // Spara originalet
    window.originalFetch = window.fetch;
    
    // Ersätt fetch med vår mock-version
    window.fetch = function(url, options) {
        console.log('Mock API anropad:', url, options);
        
        // Om anropet är för receptgenerering
        if (url.includes('/generate') && options.method === 'POST') {
            return new Promise((resolve) => {
                // Simulera en kort fördröjning
                setTimeout(() => {
                    // Skapa ett mock-svar
                    resolve({
                        ok: true,
                        json: () => Promise.resolve({
                            recipe: `1) Förslag på rätt:
Mediterran Omega-3 Laxbowl - En frisk och näringsrik rätt från medelhavsregionen, känd för sina longevity-fördelar och rika innehåll av essentiella fettsyror.

2) Gör såhär:
Koka quinoa enligt anvisningar. Under tiden, stek laxfilén i olivolja med citron och örter. Tillred en sallad med grönkål, rucola, körsbärstomater, gurka och rödlök. Blanda en dressing av olivolja, citron och vitlök. Servera laxen på quinoa-bädden, toppad med salladen, fetaost, olivor och rostade valnötter.

3) Ingredienser du har:
- 1 laxfilé (ca 150g per person)
- 1 dl quinoa (torr) per person
- 2 nävar grönkål
- 1 näve rucola
- 10-12 körsbärstomater, halverade
- 1/4 gurka, tärnad
- 1/4 rödlök, tunt skivad
- 50g fetaost, smulad
- 10 kalamataoliver
- Handfull valnötter, rostade
- 1 citron, saft och zest

4) Har du?:
- Olivolja (2-3 msk)
- Vitlök (1 klyfta)
- Salt och svartpeppar
- Torkad oregano och timjan
- Honung (1 tsk till dressingen)

5) Longevity-fördelar:
Denna rätt kombinerar flera longevity-främjande ingredienser: Lax rik på omega-3 som stödjer hjärt-kärlhälsan, quinoa som ger komplett protein och fibrer, gröna bladgrönsaker fulla med antioxidanter, nötter med hälsosamma fetter, och olivolja som är grunden i medelhavskosten. Tillsammans bildar de en antiinflammatorisk måltid som stödjer hjärnhälsa, immunförsvar och cellförnyelse.`
                        })
                    });
                }, 1500);
            });
        }
        
        // För alla andra anrop, använd det vanliga fetch
        return window.originalFetch(url, options);
    };
    
    console.log('Mock API aktiverat för testning. Backend-anrop simuleras.');
})(); 