import Toast from "./message.js"
import showTab from "./schedules/index.js"
import "./schedules/update.js"
// import "./map.js"
import "./trips/new.js"
import toggleFavorite from "./favorite.js"
import Swal from "sweetalert2";

window.Toast = Toast
window.showTab = showTab
// window.initMap = initMap
window.toggleFavorite = toggleFavorite
window.Swal = Swal;

// JavaScript 監聽刪除圖片按鈕的點擊事件
document
  .getElementById("delete-photo-btn")
  .addEventListener("click", function () {
    // 顯示彈出視窗
    document.getElementById("delete-photo-modal").style.display = "block";
  });

// JavaScript 監聽確認按鈕的點擊事件
document
  .getElementById("confirm-delete-btn")
  .addEventListener("click", function () {
    // 在用戶確認刪除時，提交表單
    document.getElementById("delete-form").submit();
  });

// JavaScript 監聽取消按鈕的點擊事件
document
  .getElementById("cancel-delete-btn")
  .addEventListener("click", function () {
    // 隱藏彈出視窗
    document.getElementById("delete-photo-modal").style.display = "none";
  });
