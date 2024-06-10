function markNotificationsAsRead() {
    fetch("{% url 'notifies:mark_as_read' %}", {
        method: 'POST',
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.href = link.getAttribute("href");
        }
    })
    .catch(error => console.error("Error updating notification status:", error));
}
