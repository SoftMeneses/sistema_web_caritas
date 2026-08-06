from django.urls import path

from .views import (

    dashboard,
    programa_lista,
    programa_crear,
    programa_detalle,
    programa_editar,
    programa_desactivar,

)

app_name = "core"

urlpatterns = [

    # ==========================================================================
    # Dashboard
    # ==========================================================================

    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),

    # ==========================================================================
    # Programas
    # ==========================================================================

    path(
        "programas/",
        programa_lista,
        name="programa_lista",
    ),

    path(
        "programas/nuevo/",
        programa_crear,
        name="programa_crear",
    ),

    path(
        "programas/<int:pk>/",
        programa_detalle,
        name="programa_detalle",
    ),

    path(
        "programas/<int:pk>/editar/",
        programa_editar,
        name="programa_editar",
    ),

    path(
        "programas/<int:pk>/desactivar/",
        programa_desactivar,
        name="programa_desactivar",
    ),

]