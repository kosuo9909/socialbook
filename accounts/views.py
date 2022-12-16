from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm


class SignUp(CreateView, SuccessMessageMixin):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    success_message = "Your profile was created successfully."

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class SignIn(LoginView):
    template_name = 'signin.html'
    success_url = reverse_lazy('index')
    next_page = reverse_lazy('index')


class SignOut(LogoutView):
    next_page = reverse_lazy('index')
