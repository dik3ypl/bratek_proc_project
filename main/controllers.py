import tempfile
import importlib.util
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.email = request.POST['email']
        user.is_active = False
        user.save()

        # current_site = get_current_site(request)
        # subject = 'Activate Your Account'
        # message = render_to_string('main/login.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': default_token_generator.make_token(user),
        # })
        # user.email_user(subject, message)
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
        user_code = request.POST.get("code", "")
        args = request.POST.get("args", "")
        expected = request.POST.get("expected", "")
        function_name = request.POST.get("function", "").strip()

        args_list = [eval(arg.strip()) for arg in args.split(',')] if args else []
        expected_list = [eval(exp.strip()) for exp in expected.split(',')] if expected else []

        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as script_file:
            script_file.write(user_code)
            script_path = script_file.name

        spec = importlib.util.spec_from_file_location("user_module", script_path)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        try:
            user_function = getattr(user_module, function_name)
            result = user_function(*args_list)
            output = f"Result of {function_name}: {result}"
            if result in expected_list:
                output += " — Result is as expected."
            else:
                output += " — Result differs from expected."
        except Exception as e:
            output = f"Error while executing user function: {str(e)}"

    return render(request, 'main/playground.html', {"output": output})