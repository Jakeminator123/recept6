document.addEventListener('DOMContentLoaded', () => {
    const libraryList = document.getElementById('library-list');
    const recipeDetails = document.getElementById('recipe-details');
    const recipeTitle = document.getElementById('recipe-title');
    const recipeContent = document.getElementById('recipe-content');
    const downloadBtn = document.getElementById('download-recipe');
    const backToListBtn = document.getElementById('back-to-list');
    
    // Ladda biblioteksrecept vid sidladdning
    loadLibraryRecipes();
    
    // Tillbaka till listan-knapp
    if (backToListBtn) {
        backToListBtn.addEventListener('click', () => {
            recipeDetails.classList.add('hidden');
            libraryList.classList.remove('hidden');
        });
    }
    
    // Ladda ner recept-funktion
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const currentRecipe = JSON.parse(sessionStorage.getItem('currentViewingLibraryRecipe') || '{}');
            
            if (!currentRecipe.id) {
                alert('Inget recept att ladda ner');
                return;
            }
            
            // Skapa länk till receptet för nedladdning
            const link = document.createElement('a');
            link.href = `/api/library/recipes/${currentRecipe.id}`;
            link.download = currentRecipe.filename || `${currentRecipe.id}.txt`;
            link.click();
        });
    }
    
    async function loadLibraryRecipes() {
        try {
            // Använd absolut URL till API-servern
            const response = await fetch('/api/library/recipes');
            
            if (!response.ok) {
                throw new Error(`Server svarade med statuskod: ${response.status}`);
            }
            
            const recipes = await response.json();
            
            if (recipes.length === 0) {
                libraryList.innerHTML = `
                    <div class="recipe-empty">
                        <p>Inga recept hittades i biblioteket.</p>
                        <p>Lägg till textfiler i mappen "recipes_library" för att se dem här.</p>
                    </div>
                `;
                return;
            }
            
            const recipesHTML = recipes.map(recipe => {
                const date = new Date(recipe.date * 1000).toLocaleDateString('sv-SE');
                const size = `${Math.round(recipe.size / 1024 * 10) / 10} KB`;
                
                return `
                    <div class="recipe-card library-recipe" data-id="${recipe.id}" data-filename="${recipe.filename}">
                        <h3>${recipe.title}</h3>
                        <div class="recipe-meta">
                            <span>${date}</span>
                            <span>${size}</span>
                        </div>
                    </div>
                `;
            }).join('');
            
            libraryList.innerHTML = recipesHTML;
            
            // Lägg till klickhändelser på recept-korten
            document.querySelectorAll('.library-recipe').forEach(card => {
                card.addEventListener('click', () => {
                    const recipeId = card.getAttribute('data-id');
                    const filename = card.getAttribute('data-filename');
                    showRecipeDetails(recipeId, filename);
                });
            });
            
        } catch (error) {
            console.error('Fel vid laddning av receptbibliotek:', error);
            libraryList.innerHTML = `
                <div class="error">
                    <p>Något gick fel vid laddning av receptbiblioteket. Vänligen försök igen.</p>
                    <p class="error-details">${error.message}</p>
                </div>
            `;
        }
    }
    
    async function showRecipeDetails(recipeId, filename) {
        try {
            // Använd absolut URL till API-servern
            const response = await fetch(`/api/library/recipes/${recipeId}`);
            
            if (!response.ok) {
                throw new Error(`Server svarade med statuskod: ${response.status}`);
            }
            
            const recipeText = await response.text();
            
            // Spara aktuellt recept i sessionStorage
            sessionStorage.setItem('currentViewingLibraryRecipe', JSON.stringify({
                id: recipeId,
                filename: filename
            }));
            
            // Visa receptdetaljer
            recipeTitle.textContent = filename.replace('.txt', '').replace(/_/g, ' ');
            recipeContent.textContent = recipeText;
            
            libraryList.classList.add('hidden');
            recipeDetails.classList.remove('hidden');
            
        } catch (error) {
            console.error('Fel vid hämtning av receptdetaljer:', error);
            alert(`Kunde inte ladda receptet: ${error.message}`);
        }
    }
}); 