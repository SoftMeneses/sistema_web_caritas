from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import (
    Actividad,
    ActividadUsuario,
)
from apps.seguridad.models import Usuario


class ActividadUsuarioForm(BaseStyledModelForm):

    """
    Formulario para asignar un usuario a una actividad.
    """

    class Meta:

        model = ActividadUsuario

        fields = [
            "usuario",
            "rol_en_actividad",
        ]

        error_messages = {

            "usuario": {
                "required":
                    "Debe seleccionar un usuario.",
            },

            "rol_en_actividad": {
                "required":
                    "El rol en la actividad es obligatorio.",
            },

        }

        widgets = {

            "rol_en_actividad": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el rol en la actividad",
                    "maxlength": "50",
                    "autocomplete": "off",
                }
            ),

        }

    def __init__(
        self,
        *args,
        actividad=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.actividad = actividad

        self.fields["usuario"].queryset = (
            Usuario.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "first_name",
                "last_name",
            )
        )

        self.fields["usuario"].empty_label = (
            "Seleccione un usuario"
        )

    def clean_rol_en_actividad(self):

        rol = self.cleaned_data[
            "rol_en_actividad"
        ].strip()

        if not rol:

            raise ValidationError(
                "El rol en la actividad es obligatorio."
            )

        if not any(
            caracter.isalnum()
            for caracter in rol
        ):

            raise ValidationError(
                "El rol en la actividad debe contener "
                "al menos una letra o número."
            )

        return rol

    def clean(self):

        cleaned_data = super().clean()

        actividad = self.actividad

        usuario = cleaned_data.get(
            "usuario"
        )

        if not actividad:

            raise ValidationError(
                "Debe especificarse una actividad."
            )

        if not actividad.estado:

            self.add_error(
                None,
                "No se puede asignar un usuario "
                "a una actividad inactiva.",
            )

        if not actividad.programa.estado:

            self.add_error(
                None,
                "No se puede asignar un usuario "
                "porque la actividad pertenece "
                "a un programa inactivo.",
            )

        if usuario:

            if not usuario.is_active:

                self.add_error(
                    "usuario",
                    "No se puede asignar un usuario inactivo.",
                )

        if (
            actividad
            and usuario
        ):

            existe = (
                ActividadUsuario.objects
                .filter(
                    actividad=actividad,
                    usuario=usuario,
                )
                .exists()
            )

            if existe:

                self.add_error(
                    "usuario",
                    "El usuario ya está asignado "
                    "a esta actividad.",
                )

        return cleaned_data