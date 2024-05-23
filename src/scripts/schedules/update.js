
function endTimeInputValidation() {
    const startTimeInput = document.querySelector("#start_time");
    const endTimeInput = document.querySelector("#end_time");

    if (endTimeInput) {
        endTimeInput.addEventListener("input", function() {
        const startTime = new Date("1970-01-01 " + startTimeInput.value);
        const endTime = new Date("1970-01-01 " + endTimeInput.value);

        // 檢查離開時間是否早於或等於抵達時間
        if (endTime <= startTime) {
            endTimeInput.setCustomValidity("離開時間不可早於抵達時間！");
        } else {
            endTimeInput.setCustomValidity("");
        }
        })  
    }
};
endTimeInputValidation()
