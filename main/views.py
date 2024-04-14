from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from main import controllers


def home(request):
    return render(request, 'main/index.html', {
        'user': request.user
    })


def playground(request):
    return controllers.playground(request)


def login(request):
    if request.method == "POST":
        return controllers.login_user(request)

    return render(request, 'main/login.html')


@require_http_methods(["POST"])
def logout(request):
    return controllers.logout_user(request)


def register(request):
    return HttpResponse("Strona rejestracji")
