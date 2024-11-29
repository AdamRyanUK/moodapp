from django import forms
from .models import WeatherPreferences

from django import forms
from .models import HealthConditions

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


