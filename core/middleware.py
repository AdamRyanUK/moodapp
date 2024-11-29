from .utils import save_location_history, get_nearest_town  # Assuming the function is in utils.py
from django.utils.timezone import now

class SaveLocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if location has been saved in this session
        if request.user.is_authenticated and not request.session.get('location_saved', False):
            # Get the user's profile and location data
            user_profile = request.user.userprofile
            latitude = user_profile.latitude if user_profile.latitude else None
            longitude = user_profile.longitude if user_profile.longitude else None
            
            if latitude and longitude:
                city = get_nearest_town(latitude, longitude)  # Assuming this is a function you defined
                if city:
                    save_location_history(request.user, latitude, longitude, city)  # Save the location
                    request.session['location_saved'] = True  # Set the session flag

        # Call the next middleware or view
        response = self.get_response(request)
        return response
