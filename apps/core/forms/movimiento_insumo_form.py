from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Insumo, MovimientoInsumo
from apps.core.models.choices import TipoMovimiento


class MovimientoInsumoForm(BaseStyledModelForm):
    """
    Formulario para el registro de movimientos de inventario.

    El stock_actual no se modifica desde el formulario.
    Su actualización corresponde a los triggers SQL de la base de datos.
    """

    class Meta:

        model = MovimientoInsumo

        fields = [
            "tipo_movimiento",
            "insumo",
            "cantidad",
            "observacion",
        ]

        error_messages = {

            "tipo_movimiento": {
                "required":
                    "Debe seleccionar el tipo de movimiento.",
            },

            "insumo": {
                "required":
                    "Debe seleccionar un insumo.",
            },

            "cantidad": {
                "required":
                    "La cantidad es obligatoria.",
            },

        }

        widgets = {

            "cantidad": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Ingrese la cantidad",
                }
            ),

            "observacion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese una observación",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["insumo"].queryset = (
            Insumo.objects
            .filter(
                estado=True
            )
            .order_by(
                "nombre"
            )
        )

        self.fields["insumo"].empty_label = (
            "Seleccione un insumo"
        )

    def clean_cantidad(self):

        cantidad = self.cleaned_data["cantidad"]

        if cantidad <= 0:

            raise ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad

    def clean(self):

        cleaned_data = super().clean()

        insumo = cleaned_data.get("insumo")

        tipo_movimiento = cleaned_data.get(
            "tipo_movimiento"
        )

        if insumo and not insumo.estado:

            self.add_error(
                "insumo",
                "No se pueden registrar movimientos "
                "para un insumo inactivo.",
            )

        if (
            insumo
            and tipo_movimiento == TipoMovimiento.SALIDA
        ):

            cantidad = cleaned_data.get("cantidad")

            if (
                cantidad is not None
                and cantidad > insumo.stock_actual
            ):

                self.add_error(
                    "cantidad",
                    "Stock insuficiente para realizar esta salida.",
                )

        return cleaned_data