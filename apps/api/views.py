from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.forms import ProgramaBeneficiarioForm

from apps.core.models import (
    Actividad,
    Auditoria,
    Beneficiario,
    DetalleActividadInsumo,
    Insumo,
    Programa,
    ProgramaBeneficiario,
)

from apps.core.services import (
    asignar_beneficiario,
    desasignar_beneficiario,
    obtener_actividades_queryset,
    obtener_usuarios_actividad,
    obtener_beneficiarios_programa,
    obtener_beneficiarios_queryset,
    obtener_insumos_queryset,
    obtener_movimientos_insumo,
    obtener_programas_beneficiario,
    obtener_programas_queryset,
)

from .serializers import (
    ActividadSerializer,
    AuditoriaSerializer,
    ActividadUsuarioSerializer,
    BeneficiarioSerializer,
    DetalleActividadInsumoSerializer,
    InsumoSerializer,
    MovimientoInsumoSerializer,
    ProgramaSerializer,
    ProgramaBeneficiarioSerializer,
)


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


class ActividadInsumosAPIView(APIView):

    def get(self, request, id_actividad):

        actividad = get_object_or_404(
            Actividad,
            pk=id_actividad
        )

        detalles = (
            DetalleActividadInsumo.objects
            .filter(actividad=actividad)
            .select_related("insumo")
            .order_by("insumo__nombre")
        )

        serializer = DetalleActividadInsumoSerializer(
            detalles,
            many=True
        )

        return Response(serializer.data)


class ProgramaBeneficiariosAPIView(APIView):
    """
    Lista los beneficiarios asignados a un programa.
    """

    def get(self, request, id_programa):
        try:
            programa = Programa.objects.get(
                id_programa=id_programa
            )
        except Programa.DoesNotExist:
            return Response(
                {
                    "detail": "El programa no existe."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        asignaciones = obtener_beneficiarios_programa(
            programa
        )

        serializer = ProgramaBeneficiarioSerializer(
            asignaciones,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class BeneficiarioProgramasAPIView(APIView):
    """
    Consulta y administra los programas asignados
    a un beneficiario.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id_beneficiario):
        beneficiario = get_object_or_404(
            Beneficiario,
            pk=id_beneficiario,
        )

        asignaciones = obtener_programas_beneficiario(
            beneficiario
        )

        serializer = ProgramaBeneficiarioSerializer(
            asignaciones,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, id_beneficiario):
        beneficiario = get_object_or_404(
            Beneficiario,
            pk=id_beneficiario,
        )

        formulario = ProgramaBeneficiarioForm(
            request.data,
            beneficiario=beneficiario,
        )

        if not formulario.is_valid():
            return Response(
                {"errors": formulario.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            asignacion = asignar_beneficiario(
                formulario=formulario,
                beneficiario=beneficiario,
                usuario_actual=request.user,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProgramaBeneficiarioSerializer(
            asignacion,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditoriaSerializer

    def get_queryset(self):
        return (
            Auditoria.objects
            .select_related("usuario_responsable")
            .order_by("-fecha_auditoria")
        )