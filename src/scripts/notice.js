document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('.notice-message');
    
    messages.forEach((element) => {
        const { message, tags: messageTags } = element.dataset;
        Toast.fire({
            icon: messageTags,
            title: message
        });
    });
});