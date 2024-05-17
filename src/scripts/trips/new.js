function handleDateChange() {
    // 當出發日期發生變化時觸發
    document.getElementById("start_date").addEventListener("change", function() {
        // 獲取出發日期的值
        let startDateValue = this.value;
        // 更新結束日期的最小值
        document.getElementById("end_date").min = startDateValue;
    });
}
handleDateChange()
export default handleDateChange; 