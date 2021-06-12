from django.shortcuts import render
from .database import check_credentials, return_users, check_credentials_db_manager, add_user_to_db
import hashlib
from .forms import UserLoginForm, DBManagerLoginForm, UserAddForm

def login(request):
    if request.method == 'GET':

        context = {'form': UserLoginForm()}
        return render(request, 'users/login.html', context)

    elif request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            sha256password = hashlib.sha256(f['password'].encode('utf-8')).hexdigest()
            if check_credentials(f['name'], f['institution'], sha256password):
                
                request.session['user_logged_in'] = True
                request.session['database_manager_logged_in'] = False
                return render(request, 'drugapp/home.html')
                

        return render(request, 'users/login.html', {'msg': 'Invalid credentials', 'form': UserLoginForm()})

def login_db_manager(request):
    if request.method == 'GET':

        context = {'form': DBManagerLoginForm()}
        return render(request, 'users/login.html', context)

    elif request.method == 'POST':

        form = DBManagerLoginForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            sha256password = hashlib.sha256(f['password'].encode('utf-8')).hexdigest()
            if check_credentials_db_manager(f['username'], sha256password):
                
                request.session['database_manager_logged_in'] = True
                request.session['user_logged_in'] = False
                return render(request, 'drugapp/home.html')
                

        return render(request, 'users/login.html', {'msg': 'Invalid credenials', 'form': DBManagerLoginForm()})
        
def logout(request):
    if request.method == 'GET':
        request.session['user_logged_in'] = False
        request.session['database_manager_logged_in'] = False

        return render(request, 'drugapp/home.html')

def add_user(request):
    if request.method == 'GET':

        context = {'form': UserAddForm()}
        return render(request, 'users/add_user.html', context)

    elif request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            sha256password = hashlib.sha256(f['password'].encode('utf-8')).hexdigest()
            msg = add_user_to_db(f['name'], f['institution'], sha256password)
                
        if msg:
            return render(request, 'users/add_user.html', {'msg': msg, 'form': UserAddForm()})  

        return render(request, 'users/add_user.html', {'msg': 'User created', 'form': UserAddForm()})
