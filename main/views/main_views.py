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
