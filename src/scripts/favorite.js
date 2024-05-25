const currentUrl = window.location.href
const spotId = currentUrl.split('/').slice(-2)[0]
const toggleFavoriteUrl = `/spots/${spotId}/toggle_favorite`
const icon = document.getElementById("favoriteIcon")

let isFavorite = false

if (icon && icon.classList.contains("fa-solid")) {
  isFavorite = true;
}

if (icon) {
    icon.addEventListener("click", () => {
        toggleFavorite()
        }
    )}

function toggleFavorite() {
    fetch(toggleFavoriteUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_favorite !== undefined) {
          isFavorite = data.is_favorite
          if (isFavorite) {
            icon.classList.remove("fa-regular")
            icon.classList.add("fa-solid")
        } else {
            icon.classList.remove("fa-solid")
            icon.classList.add("fa-regular")
        }
        } else {
          console.error("Error: Invalid response", data)
        }
    })
    .catch(error => console.error("Error:", error))
}

export default toggleFavorite