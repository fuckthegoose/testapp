from django import forms
from django.contrib.auth.models import User


class LogInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    subscribe_news = forms.BooleanField(required=False)

    def clean_password(self):
        if self.data['password'] != self.data['confirm_password']:
            self.add_error('confirm_password', 'Passwords are not the same.')
            raise forms.ValidationError('Passwords are not the same.')

        return self.data['password']

    def clean_email(self):
        email = self.cleaned_data['email']

        is_user_exists = User.objects.filter(email=email).exists()

        if not is_user_exists:
            return email

        raise forms.ValidationError('Email is already in use.')
