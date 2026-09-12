from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ActividadViewSet,
    BeneficiarioViewSet,
    InsumoViewSet,
    MovimientoInsumoViewSet,
    ProgramaViewSet,
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
]