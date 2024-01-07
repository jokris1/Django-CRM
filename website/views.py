from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # login/logout
from django.contrib import messages # when user logs in/out



def home(request): # request of page, which is sent back into backend, pass into view and returning page
    # POST FORM LOGIC
    if request.method == 'POST': # if posting form, get form data
        username = request.POST['username'] # since form has name='username'
        password = request.POST['password']

        # Authenticate: check if real user and login credentials are correct
        user = authenticate(request, username=username, password=password)
        if user is not None: # if correct
            login(request, user)
            messages.success(request, "You have been logged in!") # add to base.html file
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, please try again...")
            return redirect('home')
    
    return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    return render(request, 'register.html', {})
