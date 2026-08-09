from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from apps.seguridad.services.permission_service import (
    es_administrador,
)


def administrador_required(view_func):
    """
    Restringe el acceso a usuarios con rol Administrador.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not es_administrador(request.user):

            messages.error(
                request,
                "No tiene permisos para acceder a este módulo.",
            )

            return redirect("core:dashboard")

        return view_func(
            request,
            *args,
            **kwargs,
        )

    return wrapper