import tempfile
import importlib.util
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from mail.sender import send_activation_email


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
