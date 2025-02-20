from django import forms
from .models import Profile, Location

class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'lat', 'lon']
        widgets = {
            'hometown': forms.HiddenInput(),
            'lat': forms.HiddenInput(),
            'lon': forms.HiddenInput(),
        }



