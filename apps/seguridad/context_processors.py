from apps.seguridad.services.permission_service import (
    es_administrador,
)


def permisos_usuario(request):
    """
    Expone información de autorización del usuario
    para las plantillas del sistema.
    """

    return {
        "es_administrador": es_administrador(
            request.user
        )
    }