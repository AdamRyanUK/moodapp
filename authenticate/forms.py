# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# forms.py
class UserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['hometown', 'latitude', 'longitude']
        widgets = {
            'hometown': forms.TextInput(attrs={'class': 'form-control', 'id': 'search-location'}),
            'latitude': forms.HiddenInput(attrs={'id': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        profile = super(UserDetailsForm, self).save(commit=False)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile
