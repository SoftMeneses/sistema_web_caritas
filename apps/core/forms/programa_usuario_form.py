from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Programa, ProgramaUsuario
from apps.seguridad.models import Usuario


class ProgramaUsuarioForm(BaseStyledModelForm):
    """
    Formulario para asignar un usuario a un programa.
    """

    class Meta:

        model = ProgramaUsuario

        fields = [
            "usuario",
            "rol_en_programa",
        ]

        error_messages = {

            "usuario": {
                "required": "Debe seleccionar un usuario."
            },

            "rol_en_programa": {
                "required": "Debe indicar el rol del usuario en el programa."
            },

        }

        widgets = {

            "rol_en_programa": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el rol del usuario en el programa"
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        self.programa = kwargs.pop(
            "programa",
            None,
        )

        super().__init__(*args, **kwargs)

        self.fields["usuario"].queryset = (
            Usuario.objects
            .filter(
                is_active=True
            )
            .select_related(
                "rol"
            )
            .order_by(
                "first_name",
                "last_name",
            )
        )

        self.fields["usuario"].empty_label = (
            "Seleccione un usuario"
        )

    def clean_rol_en_programa(self):

        rol = self.cleaned_data["rol_en_programa"].strip()

        if not rol:

            raise ValidationError(
                "El rol del usuario en el programa es obligatorio."
            )

        return rol

    def clean(self):

        cleaned_data = super().clean()

        usuario = cleaned_data.get("usuario")

        if self.programa and not self.programa.estado:

            raise ValidationError(
                "No se pueden asignar usuarios a un programa inactivo."
            )

        if usuario and not usuario.is_active:

            self.add_error(
                "usuario",
                "No se puede asignar un usuario inactivo."
            )

        if self.programa and usuario:

            queryset = ProgramaUsuario.objects.filter(
                programa=self.programa,
                usuario=usuario,
            )

            if self.instance.pk:

                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():

                self.add_error(
                    "usuario",
                    "El usuario ya está asignado a este programa."
                )

        return cleaned_data