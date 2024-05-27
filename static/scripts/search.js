document.getElementById('search-button').addEventListener('click', function() {
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
                    alert(
                        '名稱: ' + data.名稱 + '\n' +
                        '地址: ' + data.地址 + '\n' +
                        (data.城市 ? '城市: ' + data.城市 + '\n' : '') +
                        (data.電話 ? '電話: ' + data.電話 + '\n' : '') +
                        (data.網址 ? '網址: ' + data.網址 + '\n' : '') +
                        (data.評分 ? '評分: ' + data.評分 + '\n' : '')
                    );
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
});

document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('search-button').click();
    }
});
