from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import (
    Actividad,
    DetalleActividadInsumo,
    Insumo,
)


class DetalleActividadInsumoForm(BaseStyledModelForm):

    """
    Formulario para registrar el consumo de un insumo
    dentro de una actividad.
    """

    class Meta:

        model = DetalleActividadInsumo

        fields = [
            "insumo",
            "cantidad_usada",
        ]

        error_messages = {

            "insumo": {
                "required":
                    "Debe seleccionar un insumo.",
            },

            "cantidad_usada": {
                "required":
                    "La cantidad utilizada es obligatoria.",
            },

        }

        widgets = {

            "cantidad_usada": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Ingrese la cantidad utilizada",
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

        self.fields["insumo"].queryset = (
            Insumo.objects
            .filter(
                estado=True,
            )
            .order_by(
                "nombre",
            )
        )

        self.fields["insumo"].empty_label = (
            "Seleccione un insumo"
        )

    def clean_cantidad_usada(self):

        cantidad = self.cleaned_data[
            "cantidad_usada"
        ]

        if cantidad <= 0:

            raise ValidationError(
                "La cantidad utilizada debe ser mayor que cero."
            )

        return cantidad

    def clean(self):

        cleaned_data = super().clean()

        actividad = self.actividad

        insumo = cleaned_data.get(
            "insumo"
        )

        cantidad = cleaned_data.get(
            "cantidad_usada"
        )

        if not actividad:

            raise ValidationError(
                "Debe especificarse una actividad."
            )

        if not actividad.estado:

            self.add_error(
                None,
                "No se puede registrar consumo "
                "para una actividad inactiva.",
            )

        if not actividad.programa.estado:

            self.add_error(
                None,
                "No se puede registrar consumo "
                "porque la actividad pertenece "
                "a un programa inactivo.",
            )

        if insumo:

            if not insumo.estado:

                self.add_error(
                    "insumo",
                    "No se puede registrar consumo "
                    "para un insumo inactivo.",
                )

        if (
            actividad
            and insumo
        ):

            existe = (
                DetalleActividadInsumo.objects
                .filter(
                    actividad=actividad,
                    insumo=insumo,
                )
                .exists()
            )

            if existe:

                self.add_error(
                    "insumo",
                    "El insumo ya está registrado "
                    "en esta actividad.",
                )

        if (
            insumo
            and cantidad is not None
            and cantidad > insumo.stock_actual
        ):

            self.add_error(
                "cantidad_usada",
                "Stock insuficiente para registrar "
                "este consumo.",
            )

        return cleaned_data