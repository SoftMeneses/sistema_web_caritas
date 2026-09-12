from rest_framework.routers import DefaultRouter

from .views import (
    BeneficiarioViewSet,
    ProgramaViewSet,
)


router = DefaultRouter()

router.register("beneficiarios", BeneficiarioViewSet, basename="beneficiario")

router.register("programas", ProgramaViewSet, basename="programa")

urlpatterns = router.urls