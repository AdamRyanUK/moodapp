from django import forms
from .models import JournalEntry, UserActions, WeatherFeedback, HealthConditions, WeatherPreferences

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

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['journal_entry']
        
class UserActionsForm(forms.ModelForm):
    class Meta:
        model = UserActions
        fields = ['exercised', 'meditated', 'socialized', 'ate_healthily', 'slept_well']
        






