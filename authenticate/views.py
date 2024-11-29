from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages 
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, EditProfileForm
from django.shortcuts import render
from .models import UserProfile


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged In!'))
			return redirect('home')

		else:
			messages.success(request, ('Error Logging In - Please Try Again...'))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out...'))
	return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            hometown = form.cleaned_data.get('hometown')
            # Use get_or_create to avoid duplicate UserProfile creation
            user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'hometown': hometown})
            if not created:
                user_profile.hometown = hometown
                user_profile.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You Have Registered...'))
            return redirect('register_weather_preferences')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile...'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Edited Your Password...'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)


