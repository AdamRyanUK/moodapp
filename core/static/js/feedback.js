document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    const feedbackPopup = document.getElementById("feedback-popup");
    console.log("Feedback popup:", feedbackPopup);
    const closePopupBtn = document.getElementById("close-popup");
    console.log("Close popup button:", closePopupBtn);

    function showPopup() {
        console.log("Showing popup");
        if (feedbackPopup) {
            feedbackPopup.style.display = "block";
        } else {
            console.error("Popup element not found.");
        }
    }

    function hidePopup() {
        if (feedbackPopup) {
            feedbackPopup.style.display = "none";
        }
    }

    // Show the popup on page load if feedback hasn't been submitted yet
    if (!localStorage.getItem("feedbackSubmitted")) {
        setTimeout(showPopup, 1000); // Delay for better UX
    }

    // Close the popup when the user clicks the close button
    if (closePopupBtn) {
        closePopupBtn.addEventListener("click", hidePopup);
    } else {
        console.error("Close button not found.");
    }

    // Handle feedback form submission
    const feedbackForm = document.getElementById("feedback-form");
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const rating = document.getElementById("rating").value;

            fetch("/weather/submit-feedback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
                },
                body: `rating=${rating}`,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        alert("Thank you for your feedback!");
                        localStorage.setItem("feedbackSubmitted", "true"); // Prevent the popup from showing again
                        hidePopup();
                    } else {
                        alert(data.error || "Something went wrong. Please try again.");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                });
        });
    } else {
        console.error("Feedback form not found.");
    }
});
