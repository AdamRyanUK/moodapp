from django.shortcuts import render

def landing_page(request): 
	return render(request, 'authenticate/landing_page.html')

def check_email(request): 
	return render(request, 'authenticate/check_email.html')

def user_register(request): 
	return render(request, 'account/signup.html')

def user_login(request):
	return render(request, 'account/login.html')