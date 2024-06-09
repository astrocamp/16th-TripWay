const imageInput = document.getElementById("image-profile")


if (imageInput){
    const imageBtn = document.getElementById("image-btn");
    const submitBtn = document.getElementById("submit-btn");

    imageInput.addEventListener("change", function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imageBtn.classList.add('hidden');
                submitBtn.classList.remove('hidden');
                document.querySelector("#image").src = e.target.result
            };
            reader.readAsDataURL(selectedFile);
        }
    });
}

