from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-caritas",
                "placeholder": "Ingrese su usuario",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-caritas",
                "placeholder": "Ingrese su contraseña",
                "autocomplete": "current-password",
            }
        ),
    )