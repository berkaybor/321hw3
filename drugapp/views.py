from django.shortcuts import render

def home(request):
    return render(request, 'drugapp/home.html')