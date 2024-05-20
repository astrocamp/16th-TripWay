
function endTimeInputValidation() {
    document.addEventListener("DOMContentLoaded", function() {
        // 找到抵達時間和離開時間的 input 元素
        const startTimeInput = document.getElementById("start_time");
        const endTimeInput = document.getElementById("end_time");

        // 監聽離開時間的輸入事件
        endTimeInput.addEventListener("input", function() {
        // 取得抵達時間和離開時間的值
        const startTime = new Date("1970-01-01 " + startTimeInput.value);
        const endTime = new Date("1970-01-01 " + endTimeInput.value);
        //"1970-01-01" 是 UNIX 時間的起始點

        // 檢查離開時間是否早於或等於抵達時間
        if (endTime <= startTime) {
            // 如果是，顯示錯誤訊息
            endTimeInput.setCustomValidity("離開時間不可早於抵達時間！");
        } else {
            // 如果不是，清除錯誤訊息
            endTimeInput.setCustomValidity("");
        }
        });
    });
}
endTimeInputValidation()
export default endTimeInputValidation; 
