from django.http import HttpResponse
from django.shortcuts import render, redirect

from main import controllers


def home(request):
    return render(request, 'main/index.html', {
        'user': request.user
    })


def login(request):
    if request.method == "POST":
        return controllers.login_user(request)

    return render(request, 'main/login.html')


def logout(request):
    if request.method == "POST":
        controllers.logout_user(request)

    return redirect('home')


def register(request):
    return HttpResponse("Strona rejestracji")
