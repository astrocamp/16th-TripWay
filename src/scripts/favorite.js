document.addEventListener("DOMContentLoaded", () => {
    // 設置事件委派給父元素，這裡假設父元素是 body
    document.body.addEventListener("click", (event) => {
        const target = event.target
        if (target && target.matches(".favoriteIcon")) {
            toggleFavorite(target)
        }
    })
})

// const icon = document.getElementById("favoriteIcon")

// let isFavorite = false

// if (icon) {
//     icon.addEventListener("click", () => {
//         toggleFavorite()
//     }
// )}


function toggleFavorite(element) {
    const toggleFavoriteUrl = element.dataset.toggleFavoriteUrl

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