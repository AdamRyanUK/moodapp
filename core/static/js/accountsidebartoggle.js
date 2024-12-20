// Ensure this file only runs when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const accountSidebar = document.querySelector('.account-sidebar'); // Select the account sidebar

    if (accountSidebar) {
        // Function to show the account sidebar
        function showAccountSidebar() {
            accountSidebar.style.display = 'flex';  // Make the account sidebar visible
        }

        // Function to hide the account sidebar
        function hideAccountSidebar() {
            accountSidebar.style.display = 'none';  // Hide the account sidebar
        }

        // Attach the show/hide functionality to the HTML elements with onclick events
        document.querySelectorAll('[onclick="showAccountSidebar()"]').forEach(button => {
            button.addEventListener('click', showAccountSidebar);
        });

        document.querySelectorAll('[onclick="hideAccountSidebar()"]').forEach(button => {
            button.addEventListener('click', hideAccountSidebar);
        });
    } else {
        console.warn('Account Sidebar element not found in the HTML!');
    }
});