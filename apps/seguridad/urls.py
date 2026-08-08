from django.urls import path
from .views import(
    login_view, 
    logout_view,
    usuario_lista,
    usuario_crear,
    usuario_detalle,
    usuario_editar,
    usuario_desactivar,
)

app_name = 'seguridad'

urlpatterns = [

    # ==========================================================================
    # Autenticación
    # ==========================================================================
    
    path('', login_view, name='login'),

    path('logout/', logout_view, name='logout'),

    # ==========================================================================
    # Usuarios
    # ==========================================================================

    path(
        "usuarios/",
        usuario_lista,
        name="usuario_lista",
    ),

    path(
        "usuarios/nuevo/",
        usuario_crear,
        name="usuario_crear",
    ),

    path(
        "usuarios/<int:pk>/",
        usuario_detalle,
        name="usuario_detalle",
    ),

    path(
        "usuarios/<int:pk>/editar/",
        usuario_editar,
        name="usuario_editar",
    ),

    path(
        "usuarios/<int:pk>/desactivar/",
        usuario_desactivar,
        name="usuario_desactivar",
    ),
]