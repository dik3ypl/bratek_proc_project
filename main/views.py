from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from main import controllers


def home(request):
    return render(request, 'main/index.html', {
        'user': request.user
    })


def playground(request):
    return controllers.playground(request)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        return controllers.register(request)

    return render(request, 'main/register.html', {'form': form})


def login(request):
    if request.method == "POST":
        return controllers.login_user(request)

    return render(request, 'main/login.html')


def activate(request, uidb64, token):
    return controllers.activate(request, uidb64, token)


@require_http_methods(["POST"])
def logout(request):
    return controllers.logout_user(request)
