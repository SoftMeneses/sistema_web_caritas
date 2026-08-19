from django import forms

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import (
    Programa,
    ProgramaBeneficiario,
)


class ProgramaBeneficiarioForm(BaseStyledModelForm):
    """
    Formulario para asignar un programa a un beneficiario.
    """

    class Meta:

        model = ProgramaBeneficiario

        fields = [
            "programa",
        ]

    def __init__(
        self,
        *args,
        beneficiario=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs,
        )

        self.beneficiario = beneficiario

        self.fields["programa"].queryset = (
            Programa.objects
            .filter(
                estado=True
            )
            .order_by(
                "nombre"
            )
        )

        self.fields["programa"].empty_label = (
            "Seleccione un programa"
        )

    def clean(self):

        cleaned_data = super().clean()

        programa = cleaned_data.get(
            "programa"
        )

        beneficiario = self.beneficiario

        if programa and not programa.estado:

            self.add_error(

                "programa",

                "No se pueden realizar asignaciones "
                "a un programa inactivo."

            )

        if beneficiario and not beneficiario.estado:

            raise forms.ValidationError(

                "No se puede asignar un programa "
                "a un beneficiario inactivo."

            )

        if programa and beneficiario:

            asignacion = (
                ProgramaBeneficiario.objects
                .filter(
                    programa=programa,
                    beneficiario=beneficiario,
                )
                .first()
            )

            if asignacion and asignacion.estado:

                self.add_error(

                    "programa",

                    "El beneficiario ya está asignado "
                    "a este programa."

                )

        return cleaned_data