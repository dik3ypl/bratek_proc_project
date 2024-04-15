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


def playground(form):
    if not form.is_valid():
        return HttpResponse("Error.")

    user_code = form.cleaned_data['code']
    args = form.cleaned_data['args']
    expected = form.cleaned_data['expected']
    function = form.cleaned_data['function']

    args_list = [eval(arg.strip()) for arg in args.split(',')] if args else []
    expected_list = [eval(exp.strip()) for exp in expected.split(',')] if expected else []

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as script_file:
        script_file.write(user_code)
        script_path = script_file.name

    spec = importlib.util.spec_from_file_location("user_module", script_path)
    user_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_module)

    try:
        user_function = getattr(user_module, function)
        result = user_function(*args_list)
        output = f"Result of {function}: {result}"
        if result in expected_list:
            output += " — Result is as expected."
        else:
            output += " — Result differs from expected."
    except Exception as e:
        output = f"Error while executing user function: {str(e)}"

    return output
