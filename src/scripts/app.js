import Toast from "./message.js"
import openTab from "./schedules/index.js"
import endTimeInputValidation from "./schedules/update.js"
import "./map.js"
import Alpine from "alpinejs"
import handleDateChange from "./trips/new.js"
import toggleFavorite from "./favorite.js"

window.Toast = Toast
window.openTab = openTab
window.initMap = initMap
window.Alpine = Alpine

Alpine.start()
window.endTimeInputValidation = endTimeInputValidation
window.handleDateChange = handleDateChange
window.toggleFavorite = toggleFavorite
