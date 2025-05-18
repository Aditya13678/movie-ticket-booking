from django import forms
from .models import user
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class register(UserCreationForm):
    class Meta:
        model=user
        fields=['username','email','phone','password1','password2']


class loginform(AuthenticationForm):
    class Meta:
        model=user
        fields=['username','password']
        widgets={
            'username':forms.TextInput(attrs={'placeholder':'username'}),
            'password':forms.PasswordInput(attrs={'placeholder':'password'})
        }