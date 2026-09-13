from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from apps.core.models import (
    Actividad,
    Insumo,
)

from apps.core.services import (
    obtener_actividades_queryset,
    obtener_usuarios_actividad,
    obtener_beneficiarios_queryset,
    obtener_insumos_queryset,
    obtener_movimientos_insumo,
    obtener_programas_queryset,
)

from .serializers import (
    ActividadSerializer,
    ActividadUsuarioSerializer,
    BeneficiarioSerializer,
    InsumoSerializer,
    MovimientoInsumoSerializer,
    ProgramaSerializer,
)

from .serializers import BeneficiarioSerializer


class BeneficiarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BeneficiarioSerializer

    def get_queryset(self):
        return obtener_beneficiarios_queryset(self.request)


class ProgramaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgramaSerializer

    def get_queryset(self):
        return obtener_programas_queryset(self.request)


class ActividadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActividadSerializer

    def get_queryset(self):
        return obtener_actividades_queryset(self.request)


class InsumoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InsumoSerializer

    def get_queryset(self):
        return obtener_insumos_queryset(self.request)


class MovimientoInsumoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MovimientoInsumoSerializer

    def get_queryset(self):
        insumo = get_object_or_404(
            Insumo,
            pk=self.kwargs["insumo_id"],
        )

        return (
            obtener_movimientos_insumo(insumo)
            .select_related("insumo")
        )


class ActividadUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActividadUsuarioSerializer

    def get_queryset(self):
        actividad = get_object_or_404(
            Actividad,
            pk=self.kwargs["actividad_id"],
        )

        return obtener_usuarios_actividad(actividad)