from rest_framework.routers import DefaultRouter

from .views import (
    ActividadViewSet,
    BeneficiarioViewSet,
    ProgramaViewSet,
)


router = DefaultRouter()

router.register("beneficiarios", BeneficiarioViewSet, basename="beneficiario")

router.register("programas", ProgramaViewSet, basename="programa")

router.register("actividades", ActividadViewSet, basename="actividad")

urlpatterns = router.urls