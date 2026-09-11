from rest_framework import serializers

from apps.core.models import Beneficiario


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