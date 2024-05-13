from django import forms
from ..models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'join_code', 'join_code_for_instructor', 'image']
