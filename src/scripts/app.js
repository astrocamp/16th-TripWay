import Toast from "./message.js"
import showTab from "./schedules/index.js"
import endTimeInputValidation from "./schedules/update.js"
import "./map.js"
import Alpine from "alpinejs"
import handleDateChange from "./trips/new.js"

window.Toast = Toast
window.showTab = showTab
window.initMap = initMap
window.Alpine = Alpine

Alpine.start()
window.endTimeInputValidation = endTimeInputValidation
window.handleDateChange = handleDateChange

document.addEventListener("DOMContentLoaded", function() {
    handleDateChange();
});

document.addEventListener("DOMContentLoaded", function() {
    endTimeInputValidation();
});