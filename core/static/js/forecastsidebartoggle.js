document.addEventListener("DOMContentLoaded", function() {
    const forecastSidebar = document.querySelector('.forecast-sidebar'); // Select the forecast sidebar

    if (forecastSidebar) {
        // Function to show the forecast sidebar
        function showForecastSidebar() {
            forecastSidebar.style.display = 'flex';  // Make the sidebar visible
        }

        // Function to hide the forecast sidebar
        function hideForecastSidebar() {
            forecastSidebar.style.display = 'none';  // Hide the sidebar
        }

        // Add event listener for showing the sidebar
        const showButton = document.querySelector('.magnifying-glass'); // Select the button
        if (showButton) {
            showButton.addEventListener('click', showForecastSidebar);
        }

        // Add event listener for hiding the sidebar
        const hideButton = document.querySelector('.close-forecast-sidebar'); // Replace with actual class for close button
        if (hideButton) {
            hideButton.addEventListener('click', hideForecastSidebar);
        }
    } else {
        console.warn('Forecast Sidebar element not found in the HTML!');
    }
});
