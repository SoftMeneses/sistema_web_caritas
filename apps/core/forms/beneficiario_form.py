from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Beneficiario


class BeneficiarioForm(BaseStyledModelForm):
    """
    Formulario para la creación y edición de beneficiarios.
    """

    class Meta:

        model = Beneficiario

        fields = [

            "cedula",
            "nombre",
            "apellido",
            "telefono",
            "direccion",
            "estado",

        ]

        error_messages = {

            "cedula": {

                "required":
                    "La cédula del beneficiario es obligatoria.",

            },

            "nombre": {

                "required":
                    "El nombre del beneficiario es obligatorio.",

            },

            "apellido": {

                "required":
                    "El apellido del beneficiario es obligatorio.",

            },

        }

        widgets = {

            "cedula": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la cédula"
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre"
                }
            ),

            "apellido": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el apellido"
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el teléfono"
                }
            ),

            "direccion": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ingrese la dirección"
                }
            ),

        }

    def clean_cedula(self):

        cedula = self.cleaned_data["cedula"].strip()

        if not cedula:

            raise ValidationError(
                "La cédula del beneficiario es obligatoria."
            )

        if not any(
            caracter.isalnum()
            for caracter in cedula
        ):

            raise ValidationError(
                "La cédula debe contener al menos una letra o número."
            )

        queryset = Beneficiario.objects.filter(
            cedula__iexact=cedula
        )

        if self.instance.pk:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise ValidationError(
                "Ya existe un beneficiario registrado con esa cédula."
            )

        return cedula

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:

            raise ValidationError(
                "El nombre del beneficiario es obligatorio."
            )

        if not any(
            caracter.isalnum()
            for caracter in nombre
        ):

            raise ValidationError(
                "El nombre del beneficiario debe contener "
                "al menos una letra o número."
            )

        return nombre

    def clean_apellido(self):

        apellido = self.cleaned_data["apellido"].strip()

        if not apellido:

            raise ValidationError(
                "El apellido del beneficiario es obligatorio."
            )

        if not any(
            caracter.isalnum()
            for caracter in apellido
        ):

            raise ValidationError(
                "El apellido del beneficiario debe contener "
                "al menos una letra o número."
            )

        return apellido

    def clean_telefono(self):

        telefono = self.cleaned_data.get("telefono")

        if telefono:

            telefono = telefono.strip()

        return telefono

    def clean_direccion(self):

        direccion = self.cleaned_data.get("direccion")

        if direccion:

            direccion = direccion.strip()

        return direccion