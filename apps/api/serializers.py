from rest_framework import serializers

from apps.core.models import Beneficiario, Programa, Actividad


class BeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiario
        fields = (
            "id_beneficiario",
            "cedula",
            "nombre",
            "apellido",
            "telefono",
            "direccion",
            "fecha_registro",
            "estado",
        )
        read_only_fields = (
            "id_beneficiario",
            "fecha_registro",
        )


class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = (
            "id_programa",
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "usuario_responsable",
        )
        read_only_fields = (
            "id_programa",
            "usuario_responsable",
        )


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = (
            "id_actividad",
            "nombre",
            "descripcion",
            "fecha_actividad",
            "estado",
            "programa",
            "usuario_creador",
        )
        read_only_fields = (
            "id_actividad",
            "usuario_creador",
        )