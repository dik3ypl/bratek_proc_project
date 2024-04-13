from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)

    if user is None:
        user = User.objects.filter(email=username).first()
        if user:
            user = authenticate(request, username=user.username, password=password)
        else:
            return HttpResponse("Nieprawidłowy login lub hasło.")

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Konto nie jest aktywne.")

    return HttpResponse("Nieprawidłowy login lub hasło.")


def logout_user(request):
    logout(request)
    return redirect('home')
