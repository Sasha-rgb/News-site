from django import forms
from newsapp.models import Questions


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(min_length=10, max_length=699)

    class Meta:
        model = Questions
        fields = ('name', 'email', 'message')