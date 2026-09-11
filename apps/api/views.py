from rest_framework import viewsets

from apps.core.services import (
    obtener_beneficiario,
    obtener_beneficiarios_queryset,
)

from .serializers import BeneficiarioSerializer


class BeneficiarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BeneficiarioSerializer

    def get_queryset(self):
        return obtener_beneficiarios_queryset(self.request)