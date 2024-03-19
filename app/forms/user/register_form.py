from django.contrib.auth.forms import UserCreationForm

from app.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'role', 'password')
