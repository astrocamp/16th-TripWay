import Toast from "./message.js"
import openTab from "./schedules/index.js"
import "./map.js"
import Alpine from "alpinejs"

window.Toast = Toast
window.openTab = openTab
window.initMap = initMap
window.Alpine = Alpine

Alpine.start()
