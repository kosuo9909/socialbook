from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm


class SignUp(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(self.request, self.object)
        return response


class SignIn(LoginView):
    template_name = 'signin.html'
    success_url = reverse_lazy('index')
    next_page = reverse_lazy('index')


class SignOut(LogoutView):
    next_page = reverse_lazy('index')
