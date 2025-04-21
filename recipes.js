document.addEventListener('DOMContentLoaded', () => {
    const recipesList = document.getElementById('recipes-list');
    const recipeDetails = document.getElementById('recipe-details');
    const recipeTitle = document.getElementById('recipe-title');
    const recipeContent = document.getElementById('recipe-content');
    const downloadBtn = document.getElementById('download-recipe');
    const backToListBtn = document.getElementById('back-to-list');
    
    // Visa receptlistan vid sidladdning
    loadRecipesList();
    
    // Tillbaka till listan-knapp
    if (backToListBtn) {
        backToListBtn.addEventListener('click', () => {
            recipeDetails.classList.add('hidden');
            recipesList.classList.remove('hidden');
        });
    }
    
    // Ladda ner recept-funktion
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const currentRecipe = JSON.parse(sessionStorage.getItem('currentViewingRecipe') || '{}');
            
            if (!currentRecipe.content) {
                alert('Inget recept att ladda ner');
                return;
            }
            
            // Skapa text-fil med receptet
            const fileName = `${currentRecipe.title.replace(/[^a-zA-Z0-9åäöÅÄÖ]/g, '_')}.txt`;
            const fileContent = currentRecipe.content;
            
            const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = fileName;
            link.click();
            URL.revokeObjectURL(link.href);
        });
    }
    
    function loadRecipesList() {
        const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
        
        if (recipes.length === 0) {
            recipesList.innerHTML = `
                <div class="recipe-empty">
                    <p>Inga sparade recept hittades.</p>
                    <p>Generera recept i huvudvyn och spara dem för att se dem här.</p>
                </div>
            `;
            return;
        }
        
        // Sortera recept med senaste först
        recipes.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        const recipesHTML = recipes.map(recipe => {
            const date = new Date(recipe.date).toLocaleDateString('sv-SE');
            const meta = recipe.meta || {};
            
            return `
                <div class="recipe-card" data-id="${recipe.id}">
                    <h3>${recipe.title}</h3>
                    <div class="recipe-meta">
                        <span>${date}</span>
                        <span>${meta.mealType || 'Måltid ej angiven'}</span>
                        <span>${meta.difficulty || 'Svårighetsgrad ej angiven'}</span>
                    </div>
                </div>
            `;
        }).join('');
        
        recipesList.innerHTML = recipesHTML;
        
        // Lägg till klickhändelser på recept-korten
        document.querySelectorAll('.recipe-card').forEach(card => {
            card.addEventListener('click', () => {
                const recipeId = card.getAttribute('data-id');
                showRecipeDetails(recipeId);
            });
        });
    }
    
    function showRecipeDetails(recipeId) {
        const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
        const recipe = recipes.find(r => r.id === recipeId);
        
        if (!recipe) {
            alert('Receptet hittades inte');
            return;
        }
        
        // Spara aktuellt recept i sessionStorage
        sessionStorage.setItem('currentViewingRecipe', JSON.stringify(recipe));
        
        // Visa receptdetaljer
        recipeTitle.textContent = recipe.title;
        recipeContent.innerHTML = formatRecipe(recipe.content);
        
        recipesList.classList.add('hidden');
        recipeDetails.classList.remove('hidden');
    }
    
    // Formatera recepttext för bättre läsbarhet (samma som i script.js)
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
}); 