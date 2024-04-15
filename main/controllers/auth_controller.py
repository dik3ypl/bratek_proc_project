from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode

from mail.sender import send_activation_email


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.email = request.POST['email']
        user.is_active = False
        user.save()

        send_activation_email(request, user)

        return HttpResponse('Please confirm your email address to complete the registration.')


def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)

    if user is None:
        user = User.objects.filter(email=username).first()
        if user:
            user = authenticate(request, username=user.username, password=password)
        else:
            return HttpResponse("Invalid credentials.")

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Inactive account.")

    return HttpResponse("Invalid credentials.")


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
