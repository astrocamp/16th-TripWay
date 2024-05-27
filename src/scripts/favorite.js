const currentUrl = window.location.href
const spotId = currentUrl.split("/").slice(-2)[0]
const toggleFavoriteUrl = `/spots/${spotId}/favorite`
const icon = document.getElementById("favoriteIcon")

let isFavorite = false

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
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "added") {
            isFavorite = true
            icon.classList.remove("fa-regular")
            icon.classList.add("fa-solid")
        } else if (data.status === "removed") {
            isFavorite = false
            icon.classList.remove("fa-solid")
            icon.classList.add("fa-regular")
        }
    })
}

export default toggleFavorite