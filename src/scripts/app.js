import Toast from "./message.js"
import showTab from "./schedules/index.js"
import "./notice.js"
import "./profile/tab.js"
import "./profile/upload.js"
import "./notice.js"
import "./navbar.js"
import "./schedules/update.js"
import "./spots/comments.js"
import "./trips/index.js"
import "./trips/new.js"
import "./blogs/edit.js"
import toggleFavorite from "./favorite.js"
import Swal from "sweetalert2"
import Alpine from "alpinejs"

window.Toast = Toast
window.Alpine = Alpine
window.showTab = showTab
window.toggleFavorite = toggleFavorite
window.Swal = Swal

Alpine.start()