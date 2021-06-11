from django.shortcuts import render
from .database import check_creditentials, return_users

def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    elif request.method == 'POST':
        return_users()
        