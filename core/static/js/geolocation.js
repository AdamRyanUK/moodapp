function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

document.addEventListener('DOMContentLoaded', () => {
    navigator.geolocation.getCurrentPosition((position) => {
        const { latitude, longitude } = position.coords;

        // Send location to the server
        fetch('/update-location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ latitude, longitude })
        });
    }, (error) => {
        console.error("Geolocation error: ", error.message);
    });
});
