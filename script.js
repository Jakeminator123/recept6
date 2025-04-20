document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recipe-form');
    const loadingIndicator = document.getElementById('loading');
    const recipeResult = document.getElementById('recipe-result');
    const recipeContent = document.getElementById('recipe-content');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Visa laddningsindikator
        loadingIndicator.classList.remove('hidden');
        recipeResult.classList.add('hidden');
        
        // Hämta formulärdata
        const formData = new FormData(form);
        
        try {
            // Skicka till API (ändra till din verkliga API-slutpunkt på Render)
            const response = await fetch('https://longevity-recept-api.onrender.com/generate', {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error(`Server svarade med statuskod: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Visa receptet
            if (data.recipe) {
                recipeContent.innerHTML = formatRecipe(data.recipe);
                recipeResult.classList.remove('hidden');
            } else {
                throw new Error('Inget recept i svaret');
            }
        } catch (error) {
            console.error('Fel vid generering av recept:', error);
            recipeContent.innerHTML = `
                <div class="error">
                    <p>Något gick fel vid generering av recept. Vänligen försök igen.</p>
                    <p class="error-details">${error.message}</p>
                </div>
            `;
            recipeResult.classList.remove('hidden');
        } finally {
            // Dölj laddningsindikatorn
            loadingIndicator.classList.add('hidden');
        }
    });
    
    // Hantera ändring av filtyp baserat på val
    const choiceSelect = document.getElementById('choice');
    const fileInput = document.getElementById('ingredients-file');
    
    choiceSelect.addEventListener('change', () => {
        const choice = choiceSelect.value;
        if (choice === '1') {
            fileInput.accept = '.txt';
        } else if (choice === '2') {
            fileInput.accept = '.jpg,.jpeg,.png';
        }
    });
});

// Formatera recepttext för bättre läsbarhet
function formatRecipe(recipeText) {
    // Split på sektioner (1), 2), etc)
    const sections = recipeText.split(/\n(?=\d\))/);
    
    // Formatera och sammanfoga sektionerna
    return sections.map((section, index) => {
        const lines = section.split('\n');
        const title = lines[0];
        const content = lines.slice(1).join('\n');
        
        return `
            <div class="recipe-section">
                <h3 class="section-title">${title}</h3>
                <div class="section-content">${content}</div>
            </div>
        `;
    }).join('');
} 