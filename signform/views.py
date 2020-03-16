from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserCreationFormWithSubscribe
from .models import Subscribers


class NotLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('signform:index'))
        return super().dispatch(request, *args, **kwargs)


class SignUpView(NotLoginRequiredMixin, View):
    template_name = 'signform/forms/signup.html'

    def post(self, request):
        form = UserCreationFormWithSubscribe(data=request.POST)
        if form.is_valid():
            user = form.save()

            if form.cleaned_data.get('subscribe_news', False):
                Subscribers.objects.create(user=user)

            return redirect(reverse('signform:login'))

        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = UserCreationFormWithSubscribe()
        return render(request, self.template_name, {'form': form})


class LoginView(NotLoginRequiredMixin, View):
    template_name = 'signform/forms/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('signform:index'))
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect(reverse('signform:login'))


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'signform/main.html', {'user': request.user})
