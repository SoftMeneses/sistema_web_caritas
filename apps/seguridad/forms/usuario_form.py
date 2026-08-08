from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.seguridad.models import Usuario


class UsuarioForm(BaseStyledModelForm):
    """
    Formulario para la creación y edición de usuarios.
    """

    password1 = forms.CharField(

        label="Contraseña",

        required=True,

        strip=False,

        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingrese una contraseña",
            }
        ),

        validators=[validate_password],

    )

    password2 = forms.CharField(

        label="Confirmar contraseña",

        required=True,

        strip=False,

        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirme la contraseña",
            }
        ),

    )

    class Meta:

        model = Usuario

        fields = [

            "first_name",

            "last_name",

            "username",

            "email",

            "cedula",

            "telefono",

            "rol",

            "is_active",

        ]

        error_messages = {

            "username": {

                "unique": "Ya existe un usuario registrado con ese nombre de usuario.",
                
            },

        }

        widgets = {

            "first_name": forms.TextInput(

                attrs={
                    "placeholder": "Ingrese el nombre",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el apellido",
                }
            ),

            "username": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre de usuario",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "correo@ejemplo.com",
                }
            ),

            "cedula": forms.TextInput(
                attrs={
                    "placeholder": "Ej: V-12345678",
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "placeholder": "Ej: 0414-1234567",
                }
            ),
        }


    def __init__(self, *args, **kwargs):
    
            super().__init__(*args, **kwargs)
    
            if self.instance.pk:
    
                self._remove_fields(
    
                    "password1",
    
                    "password2",
                )

            self.fields["rol"].empty_label = "Seleccione un rol"


    def clean_email(self):
        """
        Valida el correo electrónico.

        - Elimina espacios al inicio y al final.
        - Convierte el correo a minúsculas.
        - Impide correos duplicados.
        """

        email = self.cleaned_data["email"].strip().lower()

        queryset = Usuario.objects.filter(

            email__iexact=email,

        )

        if self.instance.pk:

            queryset = queryset.exclude(

                pk=self.instance.pk,

            )

        if queryset.exists():

            raise ValidationError(

                "Ya existe un usuario registrado con ese correo electrónico."

            )

        return email


    def clean_cedula(self):
        """
        Valida la cédula del usuario.

        - Elimina espacios.
        - Impide cédulas duplicadas.
        """

        cedula = self.cleaned_data["cedula"].strip().upper()

        queryset = Usuario.objects.filter(

            cedula__iexact=cedula,

        )

        if self.instance.pk:

            queryset = queryset.exclude(

                pk=self.instance.pk,

            )

        if queryset.exists():

            raise ValidationError(

                "Ya existe un usuario registrado con esa cédula."

            )

        return cedula


    def clean(self):
        """
        Valida la contraseña durante la creación del usuario.
        """

        cleaned_data = super().clean()

        if not self.instance.pk:

            password1 = cleaned_data.get("password1")

            password2 = cleaned_data.get("password2")

            if not password1:

                self.add_error(

                    "password1",

                    "Debe ingresar una contraseña.",

                )

            if not password2:

                self.add_error(

                    "password2",

                    "Debe confirmar la contraseña.",

                )

            if (

                password1

                and

                password2

                and

                password1 != password2

            ):

                self.add_error(

                    "password2",

                    "Las contraseñas no coinciden.",

                )

        return cleaned_data


    def save(self, commit=True):
        """
        Guarda el usuario.
    
        Durante la creación genera el hash seguro de la contraseña.
        """
    
        usuario = super().save(commit=False)
    
        if not self.instance.pk:
        
            usuario.set_password(
            
                self.cleaned_data["password1"]
    
            )
    
        if commit:
        
            usuario.save()
    
        return usuario