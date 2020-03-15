from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, LogInForm
from .models import Subscribers


class NotLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('signform:index'))
        return super().dispatch(request, *args, **kwargs)


class SignUpView( View):
    template_name = 'signform/forms/signup.html'

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            self.create_user(form.cleaned_data)

            return redirect(reverse('signform:login'))

        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def create_user(self, data):
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password'],
            **{
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'is_active': True
            }
        )

        if data.get('subscribe_news', False):
            Subscribers.objects.create(user=user)

        return user


class LoginView(NotLoginRequiredMixin, View):
    errors = []
    template_name = 'signform/forms/login.html'

    def get(self, request):
        form = LogInForm()
        return render(request, self.template_name, {'form': form, 'errors': self.errors})

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

            if user is None:
                self.errors.append('Invalid credentials')
            else:
                login(request, user)
                return redirect(reverse('signform:index'))
        return render(request, self.template_name, {'form': form, 'errors': self.errors})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect(reverse('signform:login'))


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'signform/main.html', {'user': request.user})
