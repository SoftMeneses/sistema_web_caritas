from django.urls import path

from .views import (

    dashboard,

    programa_lista,
    programa_crear,
    programa_detalle,
    programa_editar,
    programa_desactivar,

    actividad_lista,
    actividad_crear,
    actividad_detalle,
    actividad_editar,
    actividad_desactivar,

    beneficiario_lista,
    beneficiario_crear,
    beneficiario_detalle,
    beneficiario_editar,
    beneficiario_desactivar,

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


    # ==============================================================================
    # Actividades
    # ==============================================================================
    
    path(
        "actividades/",
        actividad_lista,
        name="actividad_lista",
    ),
    
    path(
        "actividades/nuevo/",
        actividad_crear,
        name="actividad_crear",
    ),
    
    path(
        "actividades/<int:pk>/",
        actividad_detalle,
        name="actividad_detalle",
    ),
    
    path(
        "actividades/<int:pk>/editar/",
        actividad_editar,
        name="actividad_editar",
    ),
    
    path(
        "actividades/<int:pk>/desactivar/",
        actividad_desactivar,
        name="actividad_desactivar",
    ),


    # ==============================================================================
    # Beneficiarios
    # ==============================================================================
    
    path(
        "beneficiarios/",
        beneficiario_lista,
        name="beneficiario_lista",
    ),
    
    path(
        "beneficiarios/nuevo/",
        beneficiario_crear,
        name="beneficiario_crear",
    ),
    
    path(
        "beneficiarios/<int:pk>/",
        beneficiario_detalle,
        name="beneficiario_detalle",
    ),
    
    path(
        "beneficiarios/<int:pk>/editar/",
        beneficiario_editar,
        name="beneficiario_editar",
    ),
    
    path(
        "beneficiarios/<int:pk>/desactivar/",
        beneficiario_desactivar,
        name="beneficiario_desactivar",
    ),

]