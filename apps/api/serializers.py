from rest_framework import serializers

from apps.core.models import (
    Actividad,
    ActividadUsuario,
    Auditoria,
    Beneficiario,
    DetalleActividadInsumo,
    Insumo,
    MovimientoInsumo, 
    Programa, 
    ProgramaBeneficiario,
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

    usuario_responsable_nombre = serializers.SerializerMethodField()

    cantidad_usuarios = serializers.IntegerField(
        read_only=True
    )

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
            "usuario_responsable_nombre",
            "cantidad_usuarios",
        )
        read_only_fields = (
            "id_programa",
            "usuario_responsable",
            "usuario_responsable_nombre",
            "cantidad_usuarios",
        )

    def get_usuario_responsable_nombre(self, obj):
        if obj.usuario_responsable:
            return str(obj.usuario_responsable)

        return None


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


class DetalleActividadInsumoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleActividadInsumo

        fields = (
            "id",
            "insumo",
            "cantidad_usada",
        )

        read_only_fields = (
            "id",
            "insumo",
            "cantidad_usada",
        )


class ProgramaBeneficiarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramaBeneficiario

        fields = (
            "id",
            "fecha_asignacion",
            "programa",
            "beneficiario",
            "estado",
        )

        read_only_fields = (
            "id",
            "fecha_asignacion",
            "programa",
            "beneficiario",
            "estado",
        )


class AuditoriaSerializer(serializers.ModelSerializer):
    usuario_responsable_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Auditoria
        fields = (
            "id_auditoria",
            "tabla_afectada",
            "operacion",
            "accion",
            "id_registro",
            "descripcion",
            "fecha_auditoria",
            "usuario_responsable",
            "usuario_responsable_nombre",
        )

        read_only_fields = fields

    def get_usuario_responsable_nombre(self, obj):
        if obj.usuario_responsable:
            return str(obj.usuario_responsable)

        return None