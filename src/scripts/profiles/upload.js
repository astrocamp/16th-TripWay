function imageUploader() {
    const imageInput = document.getElementById("image-profile");
    const imageBtn = document.getElementById("image-btn");
    const submitBtn = document.getElementById("submit-btn");
    const navAvatar = document.querySelector('.dropdown button');

    imageInput.addEventListener("change", function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = function (e) {

                imageBtn.classList.add('hidden');
                submitBtn.classList.remove('hidden');
            };
            reader.readAsDataURL(selectedFile);
        }
    });

    submitBtn.addEventListener("click", function (event) {
        event.preventDefault();

        const form = document.getElementById("upload-form");
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                navAvatar.style.backgroundImage = `url(${data.imageUrl})`;

                imageInput.value = '';
                submitBtn.classList.add('hidden');
                imageBtn.classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
    });
}

export default imageUploader;
