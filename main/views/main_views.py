from django.shortcuts import render, redirect
from main.controllers import main_controller
from main.forms.playground_form import PlaygroundForm


def home(request):
    return render(request, 'main/index.html', {
        'user': request.user
    })


def playground(request):
    if request.method == 'POST':
        output = main_controller.playground(PlaygroundForm(request.POST or None))
        return render(request, 'main/playground.html', {"output": output})

    return render(request, 'main/playground.html', {"output": None})
