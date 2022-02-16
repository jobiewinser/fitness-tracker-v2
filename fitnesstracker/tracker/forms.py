from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

class UserLoginForm(AuthenticationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        # fields = ['email']
