import Toast from "./message.js"
import openTab from "./schedules/index.js"
import "./schedules/update.js"
import Alpine from "alpinejs"
import "./trips/new.js"
import toggleFavorite from "./favorite.js"

window.Toast = Toast
window.openTab = openTab
window.Alpine = Alpine

Alpine.start()

window.toggleFavorite = toggleFavorite
