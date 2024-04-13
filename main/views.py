from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'main/index.html')


def login(request):
    return HttpResponse("Strona logowania")


def register(request):
    return HttpResponse("Strona rejestracji")
