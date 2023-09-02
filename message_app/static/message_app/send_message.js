document.addEventListener('DOMContentLoaded', function() {
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const messageInput = document.getElementById('messageInput');
    const responseDiv = document.getElementById('response');

    sendMessageBtn.addEventListener('click', () => {
        const message = messageInput.value;

        // Send the message to the server using a POST request
        fetch('/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
            },
            body: `message=${encodeURIComponent(message)}`,
        })
        .then(response => response.json())
        .then(result => {
            responseDiv.textContent = result.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
