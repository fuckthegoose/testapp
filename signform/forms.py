from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import UserCreationForm


class UserCreationFormWithSubscribe(UserCreationForm):
    subscribe_news = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        field_classes = {'username': UsernameField}
