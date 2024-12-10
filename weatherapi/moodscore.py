from weatherpreferences.models import WeatherPreferences
from django.core.exceptions import ObjectDoesNotExist

def calculate_mood_score(user, forecast):
    try:
        # Attempt to fetch the user's preferences
        preferences = WeatherPreferences.objects.get(user=user)
    except ObjectDoesNotExist:
        # Handle case where preferences don't exist (e.g., set default preferences)
        preferences = None
        
    # Initialize the mood score
    mood_score = 10  # Start with the highest score

    if preferences:
        # Temperature Max Calculation (quadratic adjustment)
        if preferences.ideal_temp_max:
            ideal_temp_max = float(preferences.ideal_temp_max)
            actual_temp_max = forecast.temperature_max
            if actual_temp_max is not None:
                temp_diff = abs(ideal_temp_max - actual_temp_max)
                # Apply a quadratic scale: squaring the temperature difference 
                # (higher difference causes a steeper drop in score)
                mood_score -= (temp_diff ** 2) / 30  # Adjust the divisor to fine-tune the impact

        # Wind Speed Calculation
        if preferences.wind_hater and forecast.wind_speed is not None:
            wind_speed = forecast.wind_speed
            if preferences.wind_hater == 'true' and wind_speed > 10:
                mood_score -= 3  # Subtract if wind is too high for the user
            elif preferences.wind_hater == 'false' and wind_speed < 5:
                mood_score += 2  # Add if wind is low (preferred by the user)

        # Sun Lover Calculation (based on weather icon)
        if preferences.sun_lover is not None and forecast.icon is not None:
            icon = forecast.icon
            sun_lover = preferences.sun_lover  # 'true' or 'false'

            # Define impact based on the weather icon
            if icon == 2:  # Sunny (maximum positive impact)
                impact = 3
            elif icon == 3:  # Partly sunny (moderate positive impact)
                impact = 2
            elif icon == 4:  # Cloudy (neutral impact)
                impact = 0
            elif icon == 5:  # Overcast (slightly negative impact)
                impact = -1
            elif 6 <= icon <= 36:  # Bad weather (negative impact)
                impact = -2
            else:
                impact = 0  # Default if icon is unknown

            # Adjust mood score based on sun_lover preference
            if sun_lover == 'true':
                # Sun lovers react positively to sunny weather and negatively to bad weather
                mood_score += impact
            else:
                # Non-sun lovers react negatively to sunny weather and positively to bad weather
                mood_score -= impact

    # Final mood score, capped between 1 and 10
    return max(min(mood_score, 10), 1)
