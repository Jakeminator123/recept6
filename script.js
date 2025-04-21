document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recipe-form');
    const loadingIndicator = document.getElementById('loading');
    const recipeResult = document.getElementById('recipe-result');
    const recipeContent = document.getElementById('recipe-content');
    const saveRecipeBtn = document.getElementById('save-recipe');
    
    // Använd relativ sökväg för API-anrop oavsett miljö
    const API_URL = '/generate';
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Visa laddningsindikator
        loadingIndicator.classList.remove('hidden');
        recipeResult.classList.add('hidden');
        
        // Hämta formulärdata
        const formData = new FormData(form);
        
        try {
            // Skicka till API 
            const response = await fetch(API_URL, {
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
                
                // Spara receptet i sessionStorage för att kunna använda "Spara"-knappen
                sessionStorage.setItem('currentRecipe', data.recipe);
                sessionStorage.setItem('recipeMeta', JSON.stringify({
                    difficulty: formData.get('difficulty'),
                    mealType: formData.get('meal_type'),
                    numPeople: formData.get('num_people'),
                    cuisinePref: formData.get('cuisine_pref') || '',
                    dietaryPref: formData.get('dietary_pref') || ''
                }));
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
    
    // Spara recept-funktion
    if (saveRecipeBtn) {
        saveRecipeBtn.addEventListener('click', () => {
            const recipe = sessionStorage.getItem('currentRecipe');
            const meta = JSON.parse(sessionStorage.getItem('recipeMeta') || '{}');
            
            if (!recipe) {
                alert('Inget recept att spara');
                return;
            }
            
            // Hämta första rubriken som receptnamn
            const titleMatch = recipe.match(/1\) Förslag på rätt:([\s\S]*?)(?=\n2\)|\n\n|$)/);
            const title = titleMatch ? titleMatch[1].trim() : 'Namnlöst recept';
            
            // Skapa recept-objekt
            const recipeObj = {
                id: Date.now().toString(),
                title: title,
                content: recipe,
                date: new Date().toISOString(),
                meta: meta
            };
            
            // Hämta befintliga recept från localStorage
            const existingRecipes = JSON.parse(localStorage.getItem('recipes') || '[]');
            existingRecipes.push(recipeObj);
            
            // Spara uppdaterad receptlista
            localStorage.setItem('recipes', JSON.stringify(existingRecipes));
            
            alert('Receptet har sparats!');
        });
    }
});

// Formatera recepttext för bättre läsbarhet
function formatRecipe(recipeText) {
    // Split på sektioner (1), 2), etc)
    const sections = recipeText.split(/\n(?=\d\))/);
    
    // Formatera och sammanfoga sektionerna
    return sections.map((section) => {
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