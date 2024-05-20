const icon = document.getElementById("favoriteIcon")

if (icon) {
    icon.addEventListener("click", () => {
        if (icon.classList.contains("fa-regular")) {
            icon.classList.remove("fa-regular")
            icon.classList.add("fa-solid")
        } else {
            icon.classList.remove("fa-solid")
            icon.classList.add("fa-regular")
        }
    })
}

// 取得當前頁面的url
const currentUrl = window.location.href

// 從url中取出該景點的id
const spotId = currentUrl.split('/').slice(-2)[0]

// 重新組成路徑
const toggleFavoriteUrl = `/spots/${spotId}/toggle_favorite`

function toggleFavorite() {
    fetch(toggleFavoriteUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    // (暫時寫法，還未設置)
    .catch(error => console.error("Error:", error)) 
}

export default toggleFavorite