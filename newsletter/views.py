from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from .mailchimp_utils import add_subscriber

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            response = add_subscriber(email)
            if response:
                return redirect("success_page")  # Define a success page in your app
    else:
        form = NewsletterSignupForm()
    return render(request, "newsletter_signup.html", {"form": form})
