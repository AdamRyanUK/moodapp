document.addEventListener("DOMContentLoaded", function() {
    // Get static URL from the script tag
    const staticUrl = JSON.parse(document.getElementById('static-url').textContent);

    window.showHourlyData = function(date) {
        console.log(`Clicked on date: ${date}`);  // Confirming the function call
        const today = new Date();
        const clickedDate = new Date(date);
        
        // Check if the clicked date is within the next 2 days
        if (clickedDate <= today.setDate(today.getDate() + 2)) {
            fetch(`/weatherapi/hourly_forecast?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    console.log(`Received data: `, data);  // Confirming data reception
                    populateHourlyData(data, staticUrl);
                    document.getElementById('hourlyModal').style.display = 'block';
                })
                .catch(error => console.error('Error fetching hourly data:', error));
        } else {
            console.log('Date is beyond the allowed range.');
        }
    }

    window.populateHourlyData = function(data, staticUrl) {
        const container = document.getElementById('hourlyDataContainer');
        container.innerHTML = `
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Time</th>
                        <th scope="col">Temperature</th>
                        <th scope="col">Weather</th>
                        <th scope="col">Icon</th>
                        <th scope="col">Mood Score</th>
                        <th scope="col">Wind Speed</th>
                        <th scope="col">Wind Direction</th>
                        <th scope="col">Cloud Cover</th>
                        <th scope="col">Precipitation</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(hour => `
                        <tr>
                            <td>${new Date(hour.date).toLocaleTimeString()}</td>
                            <td>${hour.temperature}°C</td>
                            <td>${hour.weather}</td>
                            <td><img src="${staticUrl}images/icons/${hour.icon}.png" alt="Icon"></td>
                            <td>
                                <button class="mood-score-btn" 
                                        style="border-color: ${hour.mood_score_color}; color: ${hour.mood_score_color};">
                                        ${hour.mood_score}
                                </button>
                            </td>
                            <td>${hour.wind.speed} km/h</td>
                            <td>${hour.wind.dir} (${hour.wind.angle}°)</td>
                            <td>${hour.cloud_cover.total}%</td>
                            <td>${hour.precipitation.total} mm (${hour.precipitation.type})</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    // Close modal when the user clicks on <span> (x)
    document.querySelector('.hourly-close').onclick = function() {
        document.getElementById('hourlyModal').style.display = 'none';
    }

    // Close modal when the user clicks anywhere outside of the modal
    window.onclick = function(event) {
        if (event.target == document.getElementById('hourlyModal')) {
            document.getElementById('hourlyModal').style.display = 'none';
        }
    }
});
