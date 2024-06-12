document.addEventListener('DOMContentLoaded', function() {

    function performSearch() {
        var query = document.getElementById('search-input').value;
        if (query) {
            fetch('/spots/search/?q=' + encodeURIComponent(query))
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        return response.text().then(text => {
                            throw new Error(text);
                        });
                    }
                })
                .then(data => {
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    } else if (data.名稱) {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        }
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('發生錯誤: ' + error.message);
                });
        } else {
            alert('請輸入搜索關鍵詞');
        }
    }

    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    if (searchButton && searchInput) {
        
        searchButton.addEventListener('click', function() {
            performSearch();
        });

        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }
});

