from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Actividad, Programa


class ActividadForm(BaseStyledModelForm):
    """
    Formulario para la creación y edición de actividades.
    """

    class Meta:

        model = Actividad

        fields = [

            "nombre",
            "descripcion",
            "fecha_actividad",
            "programa",
            "estado",

        ]

        error_messages = {

            "nombre": {

                "required": "El nombre de la actividad es obligatorio."
            },

            "programa": {

                "required": "Debe seleccionar un programa."
            },

            "fecha_actividad": {

                "required": "Debe seleccionar la fecha y hora de actividad."
            },
        }

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre de la actividad"
                }
            ),

            "fecha_actividad": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

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

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip()
    
        if not nombre:
        
            raise ValidationError(
                "El nombre de la actividad es obligatorio."
            )
    
        if not any(caracter.isalnum() for caracter in nombre):
        
            raise ValidationError(
                "El nombre de la actividad debe contener "
                "al menos una letra o número."
            )
    
        return nombre

    def clean_descripcion(self):

        descripcion = self.cleaned_data.get("descripcion")

        if descripcion:

            descripcion = descripcion.strip()

        return descripcion

    def clean(self):

        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")

        programa = cleaned_data.get("programa")

        fecha_actividad = cleaned_data.get(
            "fecha_actividad"
        )

        # --------------------------------------------------
        # Validar programa
        # --------------------------------------------------

        if programa and not programa.estado:

            self.add_error(

                "programa",

                "No se pueden crear o modificar actividades "
                "pertenecientes a un programa inactivo."

            )

        # --------------------------------------------------
        # Validar nombre dentro del programa
        # --------------------------------------------------

        if nombre and programa:

            queryset = Actividad.objects.filter(

                programa=programa,

                nombre__iexact=nombre,

            )

            if self.instance.pk:

                queryset = queryset.exclude(

                    pk=self.instance.pk

                )

            if queryset.exists():

                self.add_error(

                    "nombre",

                    "Ya existe una actividad registrada "
                    "con ese nombre en el programa seleccionado."

                )

        # --------------------------------------------------
        # Validar fecha dentro del período del programa
        # --------------------------------------------------

        if fecha_actividad and programa:

            if fecha_actividad.date() < programa.fecha_inicio:

                self.add_error(

                    "fecha_actividad",

                    "La fecha de la actividad no puede ser anterior "
                    "a la fecha de inicio del programa."

                )

            if (
                programa.fecha_fin
                and fecha_actividad.date() > programa.fecha_fin
            ):

                self.add_error(

                    "fecha_actividad",

                    "La fecha de la actividad no puede ser posterior "
                    "a la fecha de finalización del programa."

                )

        return cleaned_data