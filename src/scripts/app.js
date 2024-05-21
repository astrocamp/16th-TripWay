import Toast from "./message.js"
import showTab from "./schedules/index.js"
import "./schedules/update.js"
import "./trips/new.js"
import toggleFavorite from "./favorite.js"
import Swal from "sweetalert2";


window.Toast = Toast
window.showTab = showTab
window.toggleFavorite = toggleFavorite
window.Swal = Swal;

document
  .getElementById("delete-photo-btn")
  .addEventListener("click", function () {
    document.getElementById("delete-photo-modal").style.display = "block";
  });

document
  .getElementById("confirm-delete-btn")
  .addEventListener("click", function () {
    document.getElementById("delete-form").submit();
  });

document
  .getElementById("cancel-delete-btn")
  .addEventListener("click", function () {
    document.getElementById("delete-photo-modal").style.display = "none";
  });
