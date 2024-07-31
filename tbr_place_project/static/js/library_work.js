document.addEventListener('DOMContentLoaded', () => {
    const categoryFilter = document.getElementById('category-filter');
    const filterButton = document.getElementById('filter-button');
    const resultsContainer = document.getElementById('user-results');

    // Načítanie kategórií
    function loadCategories() {
        fetch('/api/categories/')
            .then(response => response.json())
            .then(data => {
                data.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    categoryFilter.appendChild(option);
                });
            })
            .catch(error => console.error('Error loading categories:', error));
    }

    // Načítanie diel
    function loadArtworks(categoryId = 'all') {
        const url = categoryId === 'all' ? '/api/literary_works/' : `/api/literary_works/?category=${categoryId}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<div>No literary works found.</div>';
                } else {
                    data.forEach(work => {
                        const div = document.createElement('div');
                        div.innerHTML = `
                            ${work.image ? `<img src="/media/${work.image}" alt="${work.title}">` : ''}
                            <h3>${work.title}</h3>
                            <p><strong>Author:</strong> ${work['user__username']}</p>
                            <p><strong>Category:</strong> ${work['category__name']}</p>
                            <p>${work.description.slice(0, 150)}${work.description.length > 150 ? '...' : ''}</p>
                            <a href="/api/literary_work/${work.id}/">Read More</a> 
                        `;
                        resultsContainer.appendChild(div);
                    });
                }
            })
            .catch(error => console.error('Error loading artworks:', error));
    }

    loadCategories();

    filterButton.addEventListener('click', () => {
        const selectedCategory = categoryFilter.value;
        loadArtworks(selectedCategory);
    });

    loadArtworks();
});
