document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", (event) => {
        const favoriteIcon = event.target
        if (favoriteIcon && favoriteIcon.matches(".fa-heart")) {
            event.stopPropagation()
            event.preventDefault()
            toggleFavorite(favoriteIcon)
        }
    })
})

function toggleFavorite(element) {
    const toggleFavoriteUrl = element.dataset.toggleFavoriteUrl

    fetch(toggleFavoriteUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "added") {
            favoriteIcon.classList.remove("fa-regular")
            favoriteIcon.classList.add("fa-solid", "text-btn-red")
        } else if (data.status === "removed") {
            favoriteIcon.classList.remove("fa-solid", "text-btn-red")
            favoriteIcon.classList.add("fa-regular")
        }
    })
}

export default toggleFavorite