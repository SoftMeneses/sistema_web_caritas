from rest_framework.routers import DefaultRouter

from .views import BeneficiarioViewSet


router = DefaultRouter()
router.register("beneficiarios", BeneficiarioViewSet, basename="beneficiario")

urlpatterns = router.urls