document.addEventListener('DOMContentLoaded', () => {
    const categoryFilter = document.getElementById('category-filter');
    const sortByFilter = document.getElementById('sort-by-filter');
    const filterButton = document.getElementById('filter-button');
    const resultsContainer = document.getElementById('user-results');
    const paginationContainer = document.getElementById('pagination');

    let currentPage = 1;
    let totalPages = 1;

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
    function loadArtworks(categoryId = 'all', sortBy = 'date_published', page = 1) {
        const url = `/api/literary_works/?category=${categoryId}&sort_by=${sortBy}&page=${page}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                paginationContainer.innerHTML = '';

                if (data.results.length === 0) {
                    resultsContainer.innerHTML = '<div>No literary works found.</div>';
                } else {
                    data.results.forEach(work => {
                        const div = document.createElement('div');
                        div.innerHTML = `
                            ${work.image ? `<img src="${work.image}" alt="${work.title}">` : ''}
                            <h3>${work.title}</h3>
                            <p><strong>Author:</strong> ${work['user__username']}</p>
                            <p><strong>Category:</strong> ${work['category__name']}</p>
                            <p>${work.description.slice(0, 150)}${work.description.length > 150 ? '...' : ''}</p>
                            <p><strong>Average Rating:</strong> ${work.average_rating ? work.average_rating.toFixed(1) : 'No Ratings'}</p>
                            <p><strong>Number of Ratings:</strong> ${work.num_ratings}</p>
                            <p><strong>Number of Comments:</strong> ${work.num_comments}</p>
                            <a href="/api/literary_work/${work.id}/">Read More</a>
                        `;
                        resultsContainer.appendChild(div);
                    });

                    // Paginácia
                    totalPages = data.num_pages;
                    for (let i = 1; i <= totalPages; i++) {
                        const pageButton = document.createElement('button');
                        pageButton.textContent = i;
                        pageButton.disabled = (i === parseInt(data.page));
                        pageButton.addEventListener('click', () => {
                            loadArtworks(categoryId, sortBy, i);
                        });
                        paginationContainer.appendChild(pageButton);
                    }
                }
            })
            .catch(error => console.error('Error loading artworks:', error));
    }

    loadCategories();

    filterButton.addEventListener('click', () => {
        const selectedCategory = categoryFilter.value;
        const selectedSortBy = sortByFilter.value;
        loadArtworks(selectedCategory, selectedSortBy, 1);
    });

    loadArtworks();
});
