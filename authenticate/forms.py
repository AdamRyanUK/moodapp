from django import forms
from .models import Profile

class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'lat', 'lon']
        widgets = {
            'hometown': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'select your hometown'}),
            'lat': forms.TextInput(attrs={'class': 'form-control'}),
            'lon': forms.TextInput(attrs={'class': 'form-control'}),
        }

