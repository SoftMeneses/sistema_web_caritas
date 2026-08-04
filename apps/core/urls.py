from django.urls import path

from .views import (

    dashboard,

    programa_lista,

    programa_crear,

    programa_detalle,

)

app_name = "core"

urlpatterns = [

    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),

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

]