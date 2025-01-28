from django.shortcuts import render

def landing_page(request): 
	return render(request, 'authenticate/landing_page.html')

# views.py
from django.shortcuts import render, redirect
from .forms import UserDetailsForm
from .models import UserProfile

from django.shortcuts import render, redirect
from .forms import UserDetailsForm
from .models import UserProfile

def user_details(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page
    else:
        form = UserDetailsForm(instance=profile, user=user)
    
    return render(request, 'authenticate/user_details.html', {'form': form})

