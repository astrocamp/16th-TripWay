const handleDateChange = document.querySelector("#start_date")

if (handleDateChange) {
    (function () {
        handleDateChange.addEventListener("change", function() {
            // 獲取出發日期的值
            let startDateValue = this.value;
            // 更新結束日期的最小值
            document.querySelector("#end_date").min = startDateValue;
        });
    })()
}

