import Toast from "./message.js"
import "./notice.js"
import showTab from "./schedules/index.js"
import toggleMenu from "./navbar.js"
import "./schedules/update.js"
import "./spots/comments.js"
import "./trips/index.js"
import "./trips/new.js"
import toggleFavorite from "./favorite.js"
import Swal from "sweetalert2";
import Alpine from "alpinejs";

window.Toast = Toast
window.Alpine = Alpine
window.showTab = showTab
window.toggleFavorite = toggleFavorite
window.toggleMenu = toggleMenu
window.Swal = Swal;

Alpine.start();