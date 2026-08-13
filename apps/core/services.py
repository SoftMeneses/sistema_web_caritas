from datetime import datetime

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from urllib.parse import urlencode

from apps.core.audit_service import registrar_auditoria
from apps.core.models import (
     Actividad, 
     Beneficiario,
     Programa,
)
from apps.core.models.choices import (
    OperacionAuditoria,
    AccionAuditoria,
)


def obtener_dashboard():

    return {

        "usuario": "",

        "fecha": datetime.now(),

        "programas": 0,

        "actividades": 0,

        "beneficiarios": 0,

        "inventario": 0,

    }


# ==============================================================================
# Programas
# ==============================================================================

def obtener_programas(request):

    """
    Obtiene el listado de programas aplicando:

    - filtro por estado
    - búsqueda
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

        Programa.objects

        .select_related("usuario_responsable")

    )

    if status == "activo":

        queryset = queryset.filter(

            estado=True,

        )

    elif status == "inactivo":

        queryset = queryset.filter(

            estado=False,

        )

    elif status == "todos":

        pass

    q = request.GET.get(

        "q",

        "",

    ).strip()

    if q:

        queryset = queryset.filter(

            Q(nombre__icontains=q)

            |

            Q(descripcion__icontains=q)

            |

            Q(usuario_responsable__first_name__icontains=q)

            |

            Q(usuario_responsable__last_name__icontains=q)

            |

            Q(usuario_responsable__username__icontains=q)

        )

    queryset = queryset.order_by(
    
        "nombre",
    
    )

    paginator = Paginator(

        queryset,

        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return {

        "programas": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "status_value": status,

        "visible_pages": obtener_paginas_visibles(page_obj),

        "query_string": params.urlencode(),

    }


def obtener_paginas_visibles(page_obj):

    """
    Calcula las páginas que serán mostradas en el componente
    de paginación.

    Se utiliza una ventana de cinco páginas alrededor de
    la página actual.
    """

    pagina_actual = page_obj.number

    total_paginas = page_obj.paginator.num_pages

    inicio = max(

        pagina_actual - 2,

        1,

    )

    fin = min(

        pagina_actual + 2,

        total_paginas,

    )

    return range(

        inicio,

        fin + 1,

    )


@transaction.atomic
def crear_programa(formulario, usuario_actual):
    """
    Guarda un nuevo programa y registra la acción realizada por el usuario.
    """

    programa = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programas",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_PROGRAMA,

        id_registro=programa.pk,

        descripcion=(
            f'Programa "{programa.nombre}" creado.'
        ),

    )

    return programa


def obtener_programa(pk):
    """
    Obtiene un programa por su identificador.
    """

    return get_object_or_404(

        Programa.objects.select_related(

            "usuario_responsable"

        ),

        pk=pk,

    )


@transaction.atomic
def actualizar_programa(formulario, usuario_actual):
    """"
    Actualiza un programa existente y registra la acción realizada por el usuario.
    """

    programa = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programas",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.EDITAR_PROGRAMA,

        id_registro=programa.pk,

        descripcion=(f'Programa "{programa.nombre}" actualizado.'),

    )

    return programa


@transaction.atomic
def desactivar_programa(programa, usuario_actual):
    """
    Realiza la desactivación lógica del programa y registra la accion realizada por el usuario.
    """

    programa.estado = False

    programa.save(

        update_fields=[
            
            "estado",
        ]
    )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programas",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.DESACTIVAR_PROGRAMA,

        id_registro=programa.pk,

        descripcion=(f'Programa "{programa.nombre}" desactivado.'),

    )

    return programa


# ==============================================================================
# Actividades
# ==============================================================================

def obtener_actividades(request):
    """
    Obtiene el listado de actividades aplicando:

    - filtro por estado
    - búsqueda
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
        Actividad.objects
        .select_related(
            "programa",
            "usuario_creador",
        )
    )

    if status == "activo":

        queryset = queryset.filter(
            estado=True,
        )

    elif status == "inactivo":

        queryset = queryset.filter(
            estado=False,
        )

    elif status == "todos":

        pass

    q = request.GET.get(
        "q",
        "",
    ).strip()

    if q:

        queryset = queryset.filter(

            Q(nombre__icontains=q)

            |

            Q(descripcion__icontains=q)

            |

            Q(programa__nombre__icontains=q)

            |

            Q(usuario_creador__first_name__icontains=q)

            |

            Q(usuario_creador__last_name__icontains=q)

            |

            Q(usuario_creador__username__icontains=q)

        )

    queryset = queryset.order_by(
        "-fecha_actividad",
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

        "actividades": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "status_value": status,

        "visible_pages": obtener_paginas_visibles(
            page_obj
        ),

        "query_string": params.urlencode(),

    }


@transaction.atomic
def crear_actividad(formulario, usuario_actual):
    """
    Guarda una nueva actividad y registra la acción
    realizada por el usuario.
    """

    actividad = formulario.save(
        commit=False
    )

    actividad.usuario_creador = usuario_actual

    actividad.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="actividades",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_ACTIVIDAD,

        id_registro=actividad.pk,

        descripcion=(
            f'Actividad "{actividad.nombre}" creada.'
        ),

    )

    return actividad


def obtener_actividad(pk):
    """
    Obtiene una actividad por su identificador.
    """

    return get_object_or_404(

        Actividad.objects.select_related(

            "programa",

            "usuario_creador",

        ),

        pk=pk,

    )


@transaction.atomic
def actualizar_actividad(formulario, usuario_actual):
    """
    Actualiza una actividad existente y registra la acción
    realizada por el usuario.
    """

    actividad = formulario.instance

    if not actividad.programa.estado:

        raise ValueError(

            "No puede modificar esta actividad porque "
            "pertenece a un programa inactivo."

        )

    actividad = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="actividades",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.EDITAR_ACTIVIDAD,

        id_registro=actividad.pk,

        descripcion=(
            f'Actividad "{actividad.nombre}" actualizada.'
        ),

    )

    return actividad


@transaction.atomic
def desactivar_actividad(actividad, usuario_actual):
    """
    Realiza la desactivación lógica de una actividad
    y registra la acción realizada por el usuario.
    """

    if not actividad.programa.estado:

        raise ValueError(

            "No puede desactivar esta actividad porque "
            "pertenece a un programa inactivo."

        )

    if not actividad.estado:

        raise ValueError(

            "La actividad ya se encuentra desactivada."

        )

    actividad.estado = False

    actividad.save(

        update_fields=[
            "estado",
        ]

    )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="actividades",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.DESACTIVAR_ACTIVIDAD,

        id_registro=actividad.pk,

        descripcion=(
            f'Actividad "{actividad.nombre}" desactivada.'
        ),

    )

    return actividad


# ==============================================================================
# Beneficiarios
# ==============================================================================

def obtener_beneficiarios(request):
    """
    Obtiene el listado de beneficiarios aplicando:

    - filtro por estado
    - búsqueda
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

    queryset = Beneficiario.objects.all()

    if status == "activo":

        queryset = queryset.filter(
            estado=True,
        )

    elif status == "inactivo":

        queryset = queryset.filter(
            estado=False,
        )

    elif status == "todos":

        pass

    q = request.GET.get(
        "q",
        "",
    ).strip()

    if q:

        queryset = queryset.filter(

            Q(cedula__icontains=q)

            |

            Q(nombre__icontains=q)

            |

            Q(apellido__icontains=q)

            |

            Q(telefono__icontains=q)

            |

            Q(direccion__icontains=q)

        )

    queryset = queryset.order_by(
        "apellido",
        "nombre",
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

        "beneficiarios": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "status_value": status,

        "visible_pages": obtener_paginas_visibles(
            page_obj
        ),

        "query_string": params.urlencode(),

    }


@transaction.atomic
def crear_beneficiario(formulario, usuario_actual):
    """
    Guarda un nuevo beneficiario y registra la acción
    realizada por el usuario.
    """

    beneficiario = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="beneficiarios",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_BENEFICIARIO,

        id_registro=beneficiario.pk,

        descripcion=(
            f'Beneficiario "{beneficiario.nombre} '
            f'{beneficiario.apellido}" creado.'
        ),

    )

    return beneficiario


def obtener_beneficiario(pk):
    """
    Obtiene un beneficiario por su identificador.
    """

    return get_object_or_404(

        Beneficiario,

        pk=pk,

    )


@transaction.atomic
def actualizar_beneficiario(formulario, usuario_actual):
    """
    Actualiza un beneficiario existente y registra
    la acción realizada por el usuario.
    """

    beneficiario = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="beneficiarios",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.EDITAR_BENEFICIARIO,

        id_registro=beneficiario.pk,

        descripcion=(
            f'Beneficiario "{beneficiario.nombre} '
            f'{beneficiario.apellido}" actualizado.'
        ),

    )

    return beneficiario


@transaction.atomic
def desactivar_beneficiario(
    beneficiario,
    usuario_actual,
):
    """
    Realiza la desactivación lógica de un beneficiario
    y registra la acción realizada por el usuario.
    """

    if not beneficiario.estado:

        raise ValueError(

            "El beneficiario ya se encuentra desactivado."

        )

    beneficiario.estado = False

    beneficiario.save(

        update_fields=[
            "estado",
        ]

    )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="beneficiarios",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.DESACTIVAR_BENEFICIARIO,

        id_registro=beneficiario.pk,

        descripcion=(
            f'Beneficiario "{beneficiario.nombre} '
            f'{beneficiario.apellido}" desactivado.'
        ),

    )

    return beneficiario