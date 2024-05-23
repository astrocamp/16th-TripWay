const handleDateChange = document.querySelector("#start_date")

if (handleDateChange) {
    (function () {
        handleDateChange.addEventListener("change", function() {
            let startDateValue = this.value;
            document.querySelector("#end_date").min = startDateValue;
        });
    })()
}

