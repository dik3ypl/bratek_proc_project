from django import forms


class PlaygroundForm(forms.Form):
    function = forms.CharField(label='Function Name', max_length=100, required=True)
    code = forms.CharField(label='Function Code', widget=forms.Textarea, required=True)
    args = forms.CharField(label='Arguments', required=False)
    expected = forms.CharField(label='Expected Output', required=False)
