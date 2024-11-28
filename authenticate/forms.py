from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class EditProfileForm(UserChangeForm):
	password = forms.CharField(label="",  widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    home_town = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Home Town'}),
    )

    # Add other UserProfile fields
    preferred_temperature_min = forms.FloatField(
        initial=15.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Min Temperature'}),
    )
    preferred_temperature_max = forms.FloatField(
        initial=25.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Max Temperature'}),
    )
    likes_rain = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    sun_worshipper = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'home_town',
            'preferred_temperature_min',
            'preferred_temperature_max',
            'likes_rain',
            'sun_worshipper',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Style the User fields
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

        self.fields['home_town'].widget.attrs['class'] = 'form-control'
        self.fields['home_town'].widget.attrs['placeholder'] = 'Enter Home Location'
        self.fields['home_town'].label = ''
        self.fields['home_town'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=commit)

        if commit:
            # Create a related UserProfile only if it doesn't already exist
            UserProfile.objects.get_or_create(
                user=user, 
                defaults={
                    'home_town': self.cleaned_data.get('home_town'),
                    'preferred_temperature_min': self.cleaned_data.get('preferred_temperature_min'),
                    'preferred_temperature_max': self.cleaned_data.get('preferred_temperature_max'),
                    'likes_rain': self.cleaned_data.get('likes_rain'),
                    'sun_worshipper': self.cleaned_data.get('sun_worshipper'),
                }
            )

        return user
