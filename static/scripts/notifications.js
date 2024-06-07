function markNotificationsAsRead() {
    fetch("{% url 'notifies:mark_as_read' %}", {
        method: 'POST',
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
        },
    })
    .then(response => {
        if (response.ok) {
            document.querySelectorAll(".notification-dot").forEach(dot => dot.style.display = "none");
        }
    })
    .catch(error => console.error("Error updating notification status:", error));
}
