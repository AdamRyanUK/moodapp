from django import forms

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField()
