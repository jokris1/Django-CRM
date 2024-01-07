from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # login/logout
from django.contrib import messages # when user logs in/out
from .forms import SignUpForm, AddRecordForm # import form
from .models import Record



def home(request): # request of page, which is sent back into backend, pass into view and returning page
    records = Record.objects.all() # get all records, show in GET logic
    
    
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
    
    return render(request, 'home.html', {'records':records}) # display all records

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST': # when form is posted
        form = SignUpForm(request.POST)
        if form.is_valid(): # django checks this automatically
            form.save()

            # authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] # forms.py
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
        
    else: # if not posting form, they are visiting same form page
        form = SignUpForm()
        return render(request, 'register.html', {'form':form}) # pass form into web
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk): # pk in urls
    # allow visibility only if logged in
    if request.user.is_authenticated:
        # look up single record
        customer_record = Record.objects.get(id=pk) # pk is nr passed in at get request

        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')

def delete_record(request, pk):
    # only allow if logged in
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None) # If not posting, go to web page
    if request.user.is_authenticated:
        # allow post if logged in
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
       # else show form on page (GET-request)
        return render(request, 'add_record.html', {'form':form})
    # if not authenticated
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        # allow update if logged in
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record) # instance will populate form with previous data

        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')