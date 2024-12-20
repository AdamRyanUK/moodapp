$(document).ready(function () {
    // Fetch the feedback status first
    fetch('/weatherpreferences/check-feedback-status/')
        .then(response => response.json())
        .then(data => {
            // Check the response and show the modal if the user has not submitted feedback today
            if (data.has_submitted === false && isAuthenticated) {
                // Show the modal only if feedback hasn't been submitted today
                $('#helloModal').modal('show');
            }
        })
        .catch(error => {
            console.error('Error checking feedback status:', error);
        });

    // Highlight the selected rating button
    const buttons = document.querySelectorAll('.rating-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            // Remove 'active' class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));

            // Add 'active' class to the clicked button
            this.classList.add('active');
        });
    });

    // Submit the rating when the user clicks submit
    document.getElementById('submitRating').addEventListener('click', function () {
        if (!isAuthenticated) {
            alert('You must be logged in to submit a rating.');
            return;
        }

        // Find the active button
        const selectedButton = document.querySelector('.rating-btn.active');

        if (selectedButton) {
            const rating = selectedButton.getAttribute('data-value');
            const userHometown = this.getAttribute('data-hometown'); // Get from data attributes
            const latitude = this.getAttribute('data-latitude'); // Get from data attributes
            const longitude = this.getAttribute('data-longitude'); // Get from data attributes
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Fetch CSRF token from hidden input

            // Send data via AJAX
            fetch(this.getAttribute('data-url'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // Ensure CSRF token is sent in the headers
                },
                body: JSON.stringify({
                    rating: rating,
                    latitude: latitude,
                    longitude: longitude,
                    city: userHometown,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Your rating has been saved!');
                    // Close the modal
                    $('#helloModal').modal('hide');
                } else {
                    alert('Something went wrong. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
            });
        } else {
            alert('Please select a rating before submitting.');
        }
    });
});

