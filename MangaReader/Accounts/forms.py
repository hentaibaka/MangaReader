from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    username = forms.SlugField(required=True)

class MyAuthenticationForm(AuthenticationForm):
    pass