from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from apps.core.services import obtener_paginas_visibles
from apps.seguridad.models import Usuario


# ==========================================
# Listado de usuarios
# ==========================================

def obtener_usuarios(request):
    """
    Obtiene el listado de usuarios aplicando:

    - búsqueda
    - filtro por estado
    - ordenamiento
    - paginación

    Retorna el contexto requerido por la vista lista.html.
    """

    params = request.GET.copy()

    params.pop(

        "page",

        None,

    )

    status = request.GET.get(

        "status",

        "activo",

    )

    queryset = (

        Usuario.objects

        .select_related(

            "rol",

        )

    )

    if status == "activo":

        queryset = queryset.filter(

            is_active=True,

        )

    elif status == "inactivo":

        queryset = queryset.filter(

            is_active=False,

        )

    queryset = queryset.order_by(

        "first_name",

        "last_name",

    )

    q = request.GET.get(

        "q",

        "",

    ).strip()

    if q:

        queryset = queryset.filter(

            Q(first_name__icontains=q)

            |

            Q(last_name__icontains=q)

            |

            Q(username__icontains=q)

            |

            Q(email__icontains=q)

            |

            Q(cedula__icontains=q)

            |

            Q(rol__nombre__icontains=q)

        )

    paginator = Paginator(

        queryset,

        10,

    )

    page_number = request.GET.get(

        "page",

    )

    page_obj = paginator.get_page(

        page_number,

    )

    return {

        "usuarios": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "status_value": status,

        "visible_pages": obtener_paginas_visibles(page_obj),

        "query_string": params.urlencode(),

    }


# ==========================================
# Crear usuario
# ==========================================

@transaction.atomic
def crear_usuario(formulario):
    """
    Guarda un nuevo usuario en la base de datos.

    Parámetros:
        formulario (UsuarioForm): formulario validado.

    Retorna:
        Usuario: instancia creada.
    """

    usuario = formulario.save()

    return usuario


# ==========================================
# Obtener usuario
# ==========================================

def obtener_usuario(pk):
    """
    Obtiene un usuario por su identificador.
    """

    return get_object_or_404(

        Usuario.objects.select_related(

            "rol",

        ),

        pk=pk,

    )


# ==========================================
# Actualizar usuario
# ==========================================

@transaction.atomic
def actualizar_usuario(formulario, usuario_actual):
    """
    Actualiza un usuario existente.

    Reglas:
    - Un usuario no puede desactivarse a sí mismo.
    - Un usuario no puede modificar su propio rol.
    """

    usuario = formulario.instance

    if usuario.pk == usuario_actual.pk:

        if formulario.cleaned_data.get("is_active") is False:

            raise ValueError(
                "No puede desactivar su propio usuario."
            )

        rol_nuevo = formulario.cleaned_data.get("rol")

        if rol_nuevo and rol_nuevo.pk != usuario_actual.rol_id:

            raise ValueError(
                "No puede modificar su propio rol."
            )

    usuario = formulario.save()

    return usuario


# ==========================================
# Desactivar usuario
# ==========================================

@transaction.atomic
def desactivar_usuario(usuario, usuario_actual):
    """
    Realiza la desactivación lógica del usuario.
    """

    if usuario.pk == usuario_actual.pk:

        raise ValueError(

            "No puede desactivar su propio usuario."

        )

    if usuario.is_superuser:

        raise ValueError(

            "No está permitido desactivar el superusuario del sistema."

        )

    if not usuario.is_active:

        raise ValueError(

            "El usuario ya se encuentra desactivado."

        )

    usuario.is_active = False

    usuario.save(

        update_fields=[

            "is_active",

        ]

    )

    return usuario