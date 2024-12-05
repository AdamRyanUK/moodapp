document.addEventListener('DOMContentLoaded', function () {
    const hometownInput = document.getElementById('hometown');
    const searchInput = document.getElementById('search-location');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const suggestionBox = document.getElementById('suggestions');

    function parseCoordinate(coord) {
        const value = parseFloat(coord);
        if (coord.includes('S') || coord.includes('W')) {
            return -value;
        }
        return value;
    }

    async function fetchCitySuggestions(query) {
        suggestionBox.innerHTML = ''; // Clear previous suggestions

        if (query.length < 3) {
            return; // Only fetch suggestions for inputs with 3 or more characters
        }

        try {
            const response = await fetch(`/weatherapi/city-autocomplete/?q=${query}`);
            const text = await response.text(); // Read the response as text first
            console.log('API response:', text); // Log the response text to see what it contains

            const data = JSON.parse(text); // Attempt to parse the JSON
            const suggestions = data.suggestions || [];
            const uniquePlaceIds = new Set();

            suggestions.forEach(city => {
                console.log('City data:', city); // Log the city object to check its content

                if (!uniquePlaceIds.has(city.place_id)) {
                    uniquePlaceIds.add(city.place_id);

                    const li = document.createElement('li');
                    li.className = 'list-group-item list-group-item-action';
                    li.innerHTML = `
                        <img src="https://flagcdn.com/16x12/${city.country_code}.png" alt="${city.country}" style="margin-right: 5px;">
                        <strong>${city.name}</strong>, ${city.adm_area1}, ${city.country}
                    `;
                    li.onclick = () => {
                        if (hometownInput) {
                            hometownInput.value = `${city.name}, ${city.adm_area1}, ${city.country}`;
                            latitudeInput.value = parseCoordinate(city.lat);
                            longitudeInput.value = parseCoordinate(city.lon);
                            console.log(`Latitude: ${latitudeInput.value}, Longitude: ${longitudeInput.value}`); // Debug log
                        } else if (searchInput) {
                            searchInput.value = `${city.name}, ${city.adm_area1}, ${city.country}`;
                            latitudeInput.value = parseCoordinate(city.lat);
                            longitudeInput.value = parseCoordinate(city.lon);
                            console.log(`Latitude: ${latitudeInput.value}, Longitude: ${longitudeInput.value}`); // Debug log
                        }
                        suggestionBox.innerHTML = '';
                    };
                    suggestionBox.appendChild(li);
                }
            });

            console.log('Unique place IDs:', uniquePlaceIds); // Log the set to check for uniqueness
        } catch (err) {
            console.error('Error fetching city suggestions:', err);
        }
    }

    if (hometownInput) {
        hometownInput.addEventListener('keyup', function () {
            const query = hometownInput.value.trim();
            fetchCitySuggestions(query);
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const query = searchInput.value.trim();
            fetchCitySuggestions(query);
        });
    }

    // Log the hidden input fields to ensure they are properly referenced
    console.log('Latitude Input:', latitudeInput);
    console.log('Longitude Input:', longitudeInput);
});
