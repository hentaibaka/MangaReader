from .forms import *
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView


class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LogInView(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'registration/login.html'
