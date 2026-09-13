from rest_framework import serializers

from apps.core.models import (
    Actividad,
    ActividadUsuario,
    Beneficiario,
    Insumo,
    MovimientoInsumo, 
    Programa, 
)    


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


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = (
            "id_insumo",
            "nombre",
            "descripcion",
            "stock_actual",
            "unidad_medida",
            "estado",
        )
        read_only_fields = (
            "id_insumo",
            "stock_actual",
        )


class MovimientoInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInsumo
        fields = (
            "id_movimiento",
            "tipo_movimiento",
            "cantidad",
            "fecha_movimiento",
            "observacion",
            "insumo",
            "usuario_responsable",
        )
        read_only_fields = (
            "id_movimiento",
            "fecha_movimiento",
            "usuario_responsable",
        )


class ActividadUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadUsuario
        fields = (
            "id_actividad_usuario",
            "actividad",
            "usuario",
        )
        read_only_fields = (
            "id_actividad_usuario",
            "actividad",
            "usuario",
        )