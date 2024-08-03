
document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Zabránime defaultnej akcii formulára

    const title = document.getElementById('searchTitle').value;
    const author = document.getElementById('searchAuthor').value;
    const genre = document.getElementById('searchGenre').value;
    const filterByAuthor = document.getElementById('filterByAuthor').checked;
    const filterByGenre = document.getElementById('filterByGenre').checked;

    fetchBooks(title, author, genre, filterByAuthor, filterByGenre, 1); // Načítaj prvú stránku
});

function fetchBooks(title, author, genre, filterByAuthor, filterByGenre, page) {
    let query = `/search-books/?title=${encodeURIComponent(title)}&page=${page}`;

    if (filterByAuthor && author) {
        query += `&author=${encodeURIComponent(author)}`;
    }
    if (filterByGenre && genre) {
        query += `&genre=${encodeURIComponent(genre)}`;
    }

    fetch(query)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';

            if (data.error) {
                resultsDiv.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            data.docs.forEach(book => {
                const coverUrl = book.cover_url ? `https://covers.openlibrary.org/b/id/${book.cover_url}-M.jpg` : '';
                resultsDiv.innerHTML += `
                     <div>
                        <img src="${coverUrl}" alt="${book.title} cover" />
                        <h3>${book.title}</h3>
                        <p>by <strong>${book.author_name}</strong></p>
                        <p>Genres: ${book.genres.join(', ')}</p>
                        
                    </div>
                `;
            });

            const paginationDiv = document.getElementById('pagination');
            paginationDiv.innerHTML = '';

            if (data.current_page > 1) {
                paginationDiv.innerHTML += `<a href="#" onclick="fetchBooks('${title}', '${author}', '${genre}', ${filterByAuthor}, ${filterByGenre}, ${data.current_page - 1}); return false;">Previous</a> `;
            }
            if (data.current_page < data.total_pages) {
                paginationDiv.innerHTML += `<a href="#" onclick="fetchBooks('${title}', '${author}', '${genre}', ${filterByAuthor}, ${filterByGenre}, ${data.current_page + 1}); return false;">Next</a>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results').innerHTML = `<p>Error fetching data</p>`;
        });
}


document.addEventListener('DOMContentLoaded', function() {
    // Funkcia na pridať knihu do obľúbených
    window.addToMyBooks = function(isbn) {
        fetch('/add-to-my-books/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ isbn: isbn })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Book added to your collection!');
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the book.');
        });
    };

    // Funkcia na zobrazenie zoznamu obľúbených kníh
    function addToMyBooks(isbn) {
    fetch('/add-to-my-books/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ isbn: isbn }) // Skontrolujte, že používate 'isbn'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Book added to your collection!');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the book.');
    });
}

    // Načítanie zoznamu obľúbených kníh pri načítaní stránky
    loadMyBooks();

    // Ak chcete pridať knihu do obľúbených
    document.getElementById('fetchButtonBooks').addEventListener('click', function() {
        // Príklad ISBN, treba upraviť podľa vašich potrieb
        addToMyBooks('9781234567890');
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



