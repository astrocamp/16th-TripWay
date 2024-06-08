const handleDateChange = document.querySelector("#start_date")

if (handleDateChange) {
    (function () {
        handleDateChange.addEventListener("change", function() {
            let startDateValue = this.value;
            document.querySelector("#end_date").min = startDateValue;
        });
    })()
}


const upload = document.querySelector("#image-upload")

function imageUpload(){
    document.querySelector("#image-upload").addEventListener("change", function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = function (e) {
            document.querySelector("#image").src = e.target.result;
            };
            reader.readAsDataURL(selectedFile);
        }
    });
}

if (upload) {
    imageUpload()
}
