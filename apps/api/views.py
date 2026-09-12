from rest_framework import viewsets

from apps.core.services import (
    obtener_actividades_queryset,
    obtener_beneficiarios_queryset,
    obtener_programas_queryset,
)

from .serializers import (
    ActividadSerializer,
    BeneficiarioSerializer,
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