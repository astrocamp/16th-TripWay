document.getElementById("delete-photo-btn").addEventListener("click", function () {
  document.getElementById("delete-photo-modal").style.display = "block";
});

document.getElementById("confirm-delete-btn").addEventListener("click", function () {
  document.getElementById("delete-form").submit();
});

