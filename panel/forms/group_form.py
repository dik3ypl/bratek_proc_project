from django import forms
from ..models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'join_code', 'join_code_for_instructor', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['join_code'].required = False
        self.fields['join_code_for_instructor'].required = False
