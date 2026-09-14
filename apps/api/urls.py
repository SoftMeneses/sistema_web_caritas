from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    ActividadViewSet,
    ActividadInsumosAPIView,
    ActividadUsuarioViewSet,
    BeneficiarioProgramasAPIView,
    BeneficiarioViewSet,
    InsumoViewSet,
    MovimientoInsumoViewSet,
    ProgramaViewSet,
    ProgramaBeneficiariosAPIView,
)


router = DefaultRouter()

router.register("beneficiarios", BeneficiarioViewSet, basename="beneficiario")

router.register("programas", ProgramaViewSet, basename="programa")

router.register("actividades", ActividadViewSet, basename="actividad")

router.register("insumos", InsumoViewSet, basename="insumo")

urlpatterns = router.urls + [
    path(
        "insumos/<int:insumo_id>/movimientos/",
        MovimientoInsumoViewSet.as_view({"get": "list"}),
        name="insumo-movimientos",
    ),
    path(
        "actividades/<int:actividad_id>/usuarios/",
        ActividadUsuarioViewSet.as_view({"get": "list"}),
        name="actividad-usuarios",
    ),
    path(
        "actividades/<int:id_actividad>/insumos/",
        ActividadInsumosAPIView.as_view(),
        name="actividad-insumos",
    ),
    path(
        "programas/<int:id_programa>/beneficiarios/",
        ProgramaBeneficiariosAPIView.as_view(),
        name="programa-beneficiarios",
    ),
    path(
        "beneficiarios/<int:id_beneficiario>/programas/",
        BeneficiarioProgramasAPIView.as_view(),
        name="beneficiario-programas",
    ),
]