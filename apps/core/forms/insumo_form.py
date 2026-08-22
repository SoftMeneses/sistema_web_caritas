from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Insumo


class InsumoForm(BaseStyledModelForm):
    """
    Formulario para la creación y edición de insumos.

    El stock_actual no se administra desde este formulario.
    Su modificación corresponde exclusivamente al registro
    de movimientos de inventario.
    """

    class Meta:

        model = Insumo

        fields = [
            "nombre",
            "descripcion",
            "unidad_medida",
            "estado",
        ]

        error_messages = {

            "nombre": {

                "required": "El nombre del insumo es obligatorio.",

            },

        }

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del insumo",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Ingrese una descripción del insumo",
                }
            ),

        }

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:

            raise ValidationError(
                "El nombre del insumo es obligatorio."
            )

        queryset = Insumo.objects.filter(
            nombre__iexact=nombre,
        )

        if self.instance.pk:

            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():

            raise ValidationError(
                "Ya existe un insumo registrado con ese nombre."
            )

        return nombre

    def clean_descripcion(self):

        descripcion = self.cleaned_data.get("descripcion")

        if descripcion:

            descripcion = descripcion.strip()

        return descripcion