const favoriteIcon = document.getElementById("favoriteIcon").addEventListener("click", () =>{
  let icon = document.getElementById("heartIcon")
  if (icon.classList.contains("fa-regular")) {
    icon.classList.remove("fa-regular")
    icon.classList.add("fa-solid")
  } else {
    icon.classList.remove("fa-solid")
    icon.classList.add("fa-regular")
  }
})

export default favoriteIcon