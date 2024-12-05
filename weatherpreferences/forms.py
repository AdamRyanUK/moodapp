from django import forms
from .models import WeatherPreferences
from .models import HealthConditions
from .models import WeatherFeedback

class HealthConditionsForm(forms.ModelForm):
    class Meta:
        model = HealthConditions
        fields = ['sad', 'joint_pain_arthritis']
        widgets = {
            'sad': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'joint_pain_arthritis': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }

class WeatherPreferencesForm(forms.ModelForm):
    class Meta:
        model = WeatherPreferences
        fields = [
            'ideal_temp_max',
            'ideal_temp_min',
            'rain_lover',
            'snow_lover',
            'sun_lover',
            'wind_hater',
        ]
        widgets = {
            'ideal_temp_max': forms.HiddenInput(),
            'ideal_temp_min': forms.HiddenInput(),
        }

class WeatherFeedbackForm(forms.ModelForm):
    class Meta:
        model = WeatherFeedback
        fields = ['rating', 'city', 'latitude', 'longitude']
        widgets = {
            'rating': forms.Select(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Neutral'), (4, 'Good'), (5, 'Very Good')]),
            'city': forms.TextInput(attrs={'id': 'hometown'}),
            'latitude': forms.HiddenInput(attrs={'id': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude'}),
        }



