import tempfile
import importlib.util
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render


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


def playground(request):
    output = None
    if request.method == "POST":
        code = request.POST.get("code", "")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as script_file:
            script_file.write(code)
            script_path = script_file.name

        spec = importlib.util.spec_from_file_location("user_module", script_path)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        data = [1, 2, 3]
        try:
            result = user_module.user_function(data)
            output = f"Result of user_function: {result}"
        except Exception as e:
            output = f"Error while executing user function: {str(e)}"

    return render(request, 'main/playground.html', {"output": output})
