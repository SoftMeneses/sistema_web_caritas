from django.urls import path

from .views import (

    dashboard,

    programa_lista,
    programa_pdf_lista,
    programa_crear,
    programa_usuario_crear,
    programa_usuario_desasignar,
    programa_detalle,
    programa_pdf,
    programa_editar,
    programa_desactivar,

    actividad_lista,
    actividad_pdf_lista,
    actividad_crear,
    actividad_usuario_crear,
    actividad_usuario_desasignar,
    actividad_detalle,
    actividad_pdf,
    actividad_editar,
    actividad_desactivar,
    consumo_insumo_crear,

    beneficiario_lista,
    beneficiario_pdf_lista,
    beneficiario_crear,
    beneficiario_detalle,
    beneficiario_editar,
    beneficiario_desactivar,
    beneficiario_pdf,

    beneficiario_asignar_programa,
    beneficiario_desasignar_programa,

    insumo_lista,
    insumo_crear,
    insumo_detalle,
    insumo_editar,
    insumo_desactivar,

    movimiento_insumo_crear,

    auditoria_lista,
    auditoria_detalle,

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
        "programas/pdf/",
        programa_pdf_lista,
        name="programa_pdf_lista",
    ),

    path(
        "programas/nuevo/",
        programa_crear,
        name="programa_crear",
    ),

    path(
        "programas/<int:pk>/usuarios/nuevo/",
        programa_usuario_crear,
        name="programa_usuario_crear",
    ),

    path(
        "programa-usuarios/<int:pk>/desasignar/",
        programa_usuario_desasignar,
        name="programa_usuario_desasignar",
    ),

    path(
        "programas/<int:pk>/",
        programa_detalle,
        name="programa_detalle",
    ),

    path(
        "programas/<int:pk>/pdf/",
        programa_pdf,
        name="programa_pdf",
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
        "actividades/pdf/",
        actividad_pdf_lista,
        name="actividad_pdf_lista",
    ),
    
    path(
        "actividades/nuevo/",
        actividad_crear,
        name="actividad_crear",
    ),

    path(
            "actividades/<int:pk>/usuarios/nuevo/",
            actividad_usuario_crear,
            name="actividad_usuario_crear",
        ),

    path(
        "actividad-usuarios/<int:pk>/desasignar/",
        actividad_usuario_desasignar,
        name="actividad_usuario_desasignar",
    ),
    
    path(
        "actividades/<int:pk>/",
        actividad_detalle,
        name="actividad_detalle",
    ),

    path(
        "actividades/<int:pk>/pdf/",
        actividad_pdf,
        name="actividad_pdf_detalle",
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

    path(
        "actividades/<int:pk>/insumos/nuevo/",
        consumo_insumo_crear,
        name="consumo_insumo_crear",
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
        "beneficiarios/pdf/",
        beneficiario_pdf_lista,
        name="beneficiario_pdf_lista",
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
        "beneficiarios/<int:pk>/pdf/",
        beneficiario_pdf,
        name="beneficiario_pdf",
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

    path(
        "beneficiarios/<int:pk>/programas/asignar/",
        beneficiario_asignar_programa,
        name="beneficiario_asignar_programa",
    ),
    
    path(
        "beneficiarios/<int:pk>/programas/<int:asignacion_pk>/desasignar/",
        beneficiario_desasignar_programa,
        name="beneficiario_desasignar_programa",
    ),


    # ==============================================================================
    # Insumos
    # ==============================================================================

    path(
        "insumos/",
        insumo_lista,
        name="insumo_lista",
    ),
    
    path(
        "insumos/nuevo/",
        insumo_crear,
        name="insumo_crear",
    ),
    
    path(
        "insumos/<int:pk>/",
        insumo_detalle,
        name="insumo_detalle",
    ),
    
    path(
        "insumos/<int:pk>/editar/",
        insumo_editar,
        name="insumo_editar",
    ),
    
    path(
        "insumos/<int:pk>/desactivar/",
        insumo_desactivar,
        name="insumo_desactivar",
    ),

    path(
        "insumos/movimiento/nuevo/",
        movimiento_insumo_crear,
        name="movimiento_insumo_crear",
    ),


    # ==========================================================================
    # Administración - Auditoría
    # ==========================================================================

    path(
        "auditoria/",
        auditoria_lista,
        name="auditoria_lista",
    ),

    path(
        "auditoria/<int:pk>/",
        auditoria_detalle,
        name="auditoria_detalle",
    ),

]