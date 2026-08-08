from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.core.forms.base_form import BaseStyledModelForm
from apps.core.models import Programa

class ProgramaForm(BaseStyledModelForm):
    """
    Formulario para la creación y edición de programas.
    """

    class Meta:

        model = Programa

        fields = [

            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "usuario_responsable",
            "estado",

        ]

        widgets = {

            "nombre": forms.TextInput(attrs={"placeholder": "Ingrese el nombre del programa"}),

            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),

            "fecha_fin": forms.DateInput(attrs={"type": "date"}),

            "descripcion": forms.Textarea(attrs={"rows": 4}),

        }

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields["usuario_responsable"].empty_label = "Seleccione un responsable"
                

    def clean_nombre(self):
        """
        Valida el nombre del programa.

        - Elimina espacios al inicio y al final.
        - Impide nombres duplicados sin distinguir mayúsculas/minúsculas.
        """

        nombre = self.cleaned_data["nombre"].strip()

        queryset = Programa.objects.filter(
            nombre__iexact=nombre
        )

        # Si estamos editando, excluir el propio registro
        if self.instance.pk:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise ValidationError(
                "Ya existe un programa registrado con ese nombre."
            )

        return nombre


    def clean(self):
        """
        Valida la coherencia entre las fechas del programa.
        """

        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if (
            fecha_inicio
            and fecha_fin
            and fecha_fin < fecha_inicio
        ):

            self.add_error(

                "fecha_fin",

                "La fecha de finalización no puede ser anterior a la fecha de inicio."

            )

        return cleaned_data


    def clean_descripcion(self):

        descripcion = self.cleaned_data.get("descripcion")

        if descripcion:

            descripcion = descripcion.strip()

        return descripcion