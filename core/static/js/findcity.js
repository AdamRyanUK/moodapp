document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-location');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const suggestionBox = document.getElementById('suggestions');
    const form = document.querySelector('form');

    function parseCoordinate(coord) {
        const value = parseFloat(coord);
        if (coord.includes('S') || coord.includes('W')) {
            return -value;
        }
        return value;
    }

    async function fetchNearestPlace(lat, lon) {
        try {
            const response = await fetch(`/weatherapi/nearest-place/?lat=${lat}&lon=${lon}`);
            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }
            const placeData = await response.json();
            return placeData;
        } catch (error) {
            console.error('Error fetching nearest place:', error);
            return null;
        }
    }

    function getCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                console.log('Geolocation - Latitude:', lat, 'Longitude:', lon);

                // Call backend to get the nearest city name
                const cityData = await fetchNearestPlace(lat, lon);

                if (cityData) {
                    // Update inputs with the fetched city data
                    searchInput.value = `${cityData.name}, ${cityData.adm_area1 || ''}, ${cityData.country || ''}`.trim();
                    latitudeInput.value = parseCoordinate(cityData.lat);
                    longitudeInput.value = parseCoordinate(cityData.lon);

                    // Auto-submit the form if required
                    form.submit();
                } else {
                    alert('Unable to fetch nearest city. Please try again.');
                }
            }, function (error) {
                console.error('Error fetching geolocation:', error);
                alert('Unable to retrieve your location. Please try again.');
            });
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    }

    async function fetchCitySuggestions(query) {
        suggestionBox.innerHTML = ''; // Clear previous suggestions

        if (query.length < 3) {
            return; // Only fetch suggestions for inputs with 3 or more characters
        }

        try {
            const response = await fetch(`/weatherapi/city-autocomplete/?q=${query}`);
            const data = await response.json();
            const suggestions = data.suggestions || [];
            const uniquePlaceIds = new Set();

            // Add city suggestions to the list
            suggestions.forEach(city => {
                if (!uniquePlaceIds.has(city.place_id)) {
                    uniquePlaceIds.add(city.place_id);

                    const li = document.createElement('li');
                    li.className = 'list-group-item list-group-item-action';
                    li.innerHTML = `
                        <img src="https://flagcdn.com/16x12/${city.country_code}.png" alt="${city.country}" style="margin-right: 5px;">
                        <strong>${city.name}</strong>, ${city.adm_area1 || ''}, ${city.country || ''}
                    `;
                    li.onclick = () => {
                        searchInput.value = `${city.name}, ${city.adm_area1 || ''}, ${city.country || ''}`;
                        latitudeInput.value = parseCoordinate(city.lat);
                        longitudeInput.value = parseCoordinate(city.lon);
                        suggestionBox.innerHTML = ''; // Clear suggestions
                        form.submit(); // Submit the form after city selection
                    };
                    suggestionBox.appendChild(li);
                }
            });
        } catch (err) {
            console.error('Error fetching city suggestions:', err);
        }
    }

    // Show "Use current location" when the input is focused
    if (searchInput) {
        searchInput.addEventListener('focus', function () {
            // Clear previous suggestions
            suggestionBox.innerHTML = '';

            // Add "Use current location" option
            const useLocationItem = document.createElement('li');
            useLocationItem.className = 'list-group-item list-group-item-action d-flex align-items-center';
            useLocationItem.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5f6368" style="margin-right: 8px;">
                    <path d="M440-42v-80q-125-14-214.5-103.5T122-440H42v-80h80q14-125 103.5-214.5T440-838v-80h80v80q125 14 214.5 103.5T838-520h80v80h-80q-14 125-103.5 214.5T520-122v80h-80Zm40-158q116 0 198-82t82-198q0-116-82-198t-198-82q-116 0-198 82t-82 198q0 116 82 198t198 82Zm0-120q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm0-80q33 0 56.5-23.5T560-480q0-33-23.5-56.5T480-560q-33 0-56.5 23.5T400-480q0 33 23.5 56.5T480-400Zm0-80Z"/>
                </svg>
                Use current location
            `;
            useLocationItem.onclick = () => {
                getCurrentLocation(); // Call geolocation function
                suggestionBox.innerHTML = ''; // Clear suggestions
            };
            suggestionBox.appendChild(useLocationItem);
        });

        // Handle search input changes (fetch city suggestions)
        searchInput.addEventListener('keyup', function () {
            const query = searchInput.value.trim();

            // Clear the dropdown if query is empty
            if (!query) {
                suggestionBox.innerHTML = '';
                return;
            }

            // Fetch city suggestions if query length is 3 or more characters
            if (query.length >= 3) {
                fetchCitySuggestions(query);
            }
        });
    }

    // Detect clicks outside the suggestion box to close it
    document.addEventListener('click', function (event) {
        if (suggestionBox && !suggestionBox.contains(event.target) &&
            (searchInput && !searchInput.contains(event.target))) {
            suggestionBox.innerHTML = ''; // Clear suggestion box
        }
    });

    form.addEventListener('submit', function () {
        console.log('Form submitted with:');
        console.log('Latitude:', latitudeInput.value);
        console.log('Longitude:', longitudeInput.value);
    });
});
