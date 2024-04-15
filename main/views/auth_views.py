from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ..controllers import auth_controller


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        return auth_controller.register(request)

    return render(request, 'auth/register.html', {'form': form})


def login(request):
    if request.method == "POST":
        return auth_controller.login_user(request)

    return render(request, 'auth/login.html')


def activate(request, uidb64, token):
    return auth_controller.activate(request, uidb64, token)


@require_http_methods(["POST"])
def logout(request):
    logout(request)
    return redirect('home')
