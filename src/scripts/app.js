import Toast from "./message.js"
import showTab from "./schedules/index.js"
import "./schedules/update.js"
// import "./map.js"
import Alpine from "alpinejs"
import "./trips/new.js"

window.Toast = Toast
window.showTab = showTab
// window.initMap = initMap
window.Alpine = Alpine

Alpine.start()