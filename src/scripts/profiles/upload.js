function imageUploader() {
    document
        .getElementById("image-profile")
        .addEventListener("change", function (event) {
            const selectedFile = event.target.files[0];
            if (selectedFile) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    document.getElementById("image").src = e.target.result;
                };
                reader.readAsDataURL(selectedFile);
            }
        });
}
export default imageUploader