# middleware.py
from datetime import date
from weatherapi.services import fetch_and_save_forecast

class ForecastMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the user's latest forecast
            user = request.user
            latest_forecast = user.dailyforecast_set.order_by('-date').first()
            
            # Check if there's no forecast or if the latest forecast is outdated
            today = date.today()
            if not latest_forecast or latest_forecast.date < today:
                try:
                    fetch_and_save_forecast(user)
                except Exception as e:
                    print(f"Error updating weather forecast: {e}")
        
        # Continue processing the request
        response = self.get_response(request)
        return response
