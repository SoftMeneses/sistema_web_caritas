from datetime import datetime

from django.core.exceptions import ValidationError
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
     ProgramaBeneficiario,
     ProgramaUsuario,
     Insumo,
     MovimientoInsumo,
     DetalleActividadInsumo,
     ActividadUsuario,
     Auditoria,
)

from apps.core.models.choices import (
    OperacionAuditoria,
    AccionAuditoria,
    TipoMovimiento,
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


def obtener_auditorias(request):

    """
    Obtiene el listado paginado de auditorías aplicando:

    - búsqueda
    - filtro por operación
    - filtro por acción
    - filtro por tabla afectada
    - ordenamiento
    - paginación

    Retorna el contexto requerido por la vista de auditoría.
    """

    acciones_auditoria = AccionAuditoria.choices

    params = request.GET.copy()

    params.pop(
        "page",
        None,
    )

    queryset = (
        Auditoria.objects
        .select_related(
            "usuario_responsable",
        )
    )

    q = request.GET.get(
        "q",
        "",
    ).strip()

    if q:

        queryset = queryset.filter(

            Q(tabla_afectada__icontains=q)

            |

            Q(descripcion__icontains=q)

            |

            Q(usuario_responsable__first_name__icontains=q)

            |

            Q(usuario_responsable__last_name__icontains=q)

            |

            Q(usuario_responsable__username__icontains=q)

        )

    operacion = request.GET.get(
        "operacion",
        "",
    )

    if operacion:

        queryset = queryset.filter(
            operacion=operacion,
        )

    accion = request.GET.get(
        "accion",
        "",
    )

    if accion:

        queryset = queryset.filter(
            accion=accion,
        )

    tabla = request.GET.get(
        "tabla",
        "",
    ).strip()

    if tabla:

        queryset = queryset.filter(
            tabla_afectada__icontains=tabla,
        )

    queryset = queryset.order_by(
        "-fecha_auditoria",
    )

    paginator = Paginator(
        queryset,
        20,
    )

    page_number = request.GET.get(
        "page",
    )

    page_obj = paginator.get_page(
        page_number,
    )

    return {

        "auditorias": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "operacion_value": operacion,

        "accion_value": accion,

        "tabla_value": tabla,

        "acciones_auditoria": AccionAuditoria.choices,

        "visible_pages": obtener_paginas_visibles(
            page_obj,
        ),

        "query_string": params.urlencode(),

    }


def obtener_auditoria(pk):
    """
    Obtiene un registro de auditoría por su identificador.
    """

    return get_object_or_404(
        Auditoria.objects.select_related(
            "usuario_responsable",
        ),
        id_auditoria=pk,
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


def obtener_usuarios_programa(programa):
    """
    Obtiene los usuarios asignados a un programa.
    """

    return (
        ProgramaUsuario.objects
        .filter(
            programa=programa
        )
        .select_related(
            "usuario",
            "usuario__rol",
        )
        .order_by(
            "-fecha_asignacion",
        )
    )


def obtener_asignacion_usuario_programa(pk):
    """
    Obtiene una asignación de usuario a programa.
    """

    return get_object_or_404(

        ProgramaUsuario.objects.select_related(

            "programa",
            "usuario",
            "usuario__rol",

        ),

        pk=pk,

    )


@transaction.atomic
def asignar_usuario_programa(
    formulario,
    programa,
    usuario_actual,
):
    """
    Asigna un usuario a un programa y registra
    la operación realizada en auditoría.
    """

    if not programa.estado:

        raise ValidationError(
            "No se pueden asignar usuarios "
            "a un programa inactivo."
        )

    asignacion = formulario.save(
        commit=False
    )

    asignacion.programa = programa

    asignacion.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programa_usuario",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_ASIGNACION_USUARIO,

        id_registro=asignacion.pk,

        descripcion=(
            f'Usuario "{asignacion.usuario}" asignado al '
            f'programa "{programa.nombre}" '
            f'(rol: "{asignacion.rol_en_programa}").'
        ),

    )

    return asignacion


@transaction.atomic
def desasignar_usuario_programa(
    asignacion,
    usuario_actual,
):
    """
    Desasigna un usuario de un programa y registra
    la operación en auditoría.
    """

    programa = asignacion.programa

    usuario = asignacion.usuario

    if not programa.estado:

        raise ValidationError(
            "No se puede desasignar un usuario "
            "de un programa inactivo."
        )

    id_asignacion = asignacion.pk

    descripcion = (
        f'Usuario "{usuario}" desasignado del '
        f'programa "{programa.nombre}" '
        f'(rol: "{asignacion.rol_en_programa}").'
    )

    asignacion.delete()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programa_usuario",

        operacion=OperacionAuditoria.DELETE,

        accion=AccionAuditoria.DESASIGNAR_USUARIO_PROGRAMA,

        id_registro=id_asignacion,

        descripcion=descripcion,

    )

    return id_asignacion


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


def obtener_consumos_actividad(actividad):
    """
    Obtiene los insumos utilizados en una actividad.
    """

    return (
        DetalleActividadInsumo.objects
        .filter(
            actividad=actividad,
        )
        .select_related(
            "insumo",
        )
        .order_by(
            "insumo__nombre",
        )
    )


def obtener_usuarios_actividad(actividad):
    """
    Obtiene los usuarios asignados a una actividad.
    """

    return (
        ActividadUsuario.objects
        .filter(
            actividad=actividad,
        )
        .select_related(
            "usuario",
        )
        .order_by(
            "usuario__first_name",
            "usuario__last_name",
        )
    )


@transaction.atomic
def asignar_usuario_actividad(
    formulario,
    actividad,
    usuario_actual,
):
    """
    Asigna un usuario a una actividad y registra
    la operación en auditoría.
    """

    asignacion = formulario.save(
        commit=False
    )

    asignacion.actividad = actividad

    usuario = asignacion.usuario

    if not actividad.estado:

        raise ValidationError(
            "No se puede asignar un usuario "
            "a una actividad inactiva."
        )

    if not actividad.programa.estado:

        raise ValidationError(
            "No se puede asignar un usuario "
            "porque la actividad pertenece "
            "a un programa inactivo."
        )

    if not usuario.is_active:

        raise ValidationError(
            "No se puede asignar un usuario inactivo."
        )

    asignacion.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="actividad_usuario",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_ASIGNACION_USUARIO,

        id_registro=asignacion.pk,

        descripcion=(
            f'Usuario "{usuario}" asignado a la '
            f'actividad "{actividad.nombre}" '
            f'con rol "{asignacion.rol_en_actividad}".'
        ),

    )

    return asignacion


def obtener_asignacion_usuario_actividad(
    pk,
):
    """
    Obtiene una asignación de usuario a actividad.
    """

    return get_object_or_404(
        ActividadUsuario.objects.select_related(
            "actividad",
            "actividad__programa",
            "usuario",
        ),
        pk=pk,
    )


@transaction.atomic
def desasignar_usuario_actividad(
    asignacion,
    usuario_actual,
):
    """
    Desasigna un usuario de una actividad y registra
    la operación en auditoría.
    """

    actividad = asignacion.actividad
    usuario = asignacion.usuario

    if not actividad.estado:

        raise ValidationError(
            "No se puede desasignar un usuario "
            "de una actividad inactiva."
        )

    if not actividad.programa.estado:

        raise ValidationError(
            "No se puede desasignar un usuario "
            "porque la actividad pertenece "
            "a un programa inactivo."
        )

    id_asignacion = asignacion.pk

    descripcion = (
        f'Usuario "{usuario}" desasignado de la '
        f'actividad "{actividad.nombre}" '
        f'(rol: "{asignacion.rol_en_actividad}").'
    )

    asignacion.delete()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="actividad_usuario",

        operacion=OperacionAuditoria.DELETE,

        accion=AccionAuditoria.DESASIGNAR_USUARIO,

        id_registro=id_asignacion,

        descripcion=descripcion,

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


# ==============================================================================
# Asignación de beneficiarios a programas
# ==============================================================================

@transaction.atomic
def asignar_beneficiario(
    formulario,
    beneficiario,
    usuario_actual,
):
    """
    Asigna un beneficiario a un programa.

    Si la relación ya existe pero se encuentra inactiva,
    la reactiva en lugar de crear un nuevo registro.
    """

    programa = formulario.cleaned_data["programa"]

    if not beneficiario.estado:

        raise ValueError(
            "No se puede asignar un programa "
            "a un beneficiario inactivo."
        )
    
    if not programa.estado:
    
        raise ValueError(
            "No se puede asignar un programa inactivo."
        )

    asignacion = (
        ProgramaBeneficiario.objects
        .filter(
            programa=programa,
            beneficiario=beneficiario,
        )
        .first()
    )

    if asignacion:

        asignacion.estado = True

        asignacion.save(
            update_fields=[
                "estado",
            ]
        )

        operacion = OperacionAuditoria.UPDATE

        descripcion = (
            f'Asignación del beneficiario '
            f'"{beneficiario.nombre} {beneficiario.apellido}" '
            f'al programa "{programa.nombre}" reactivada.'
        )

    else:

        asignacion = ProgramaBeneficiario.objects.create(

            programa=programa,

            beneficiario=beneficiario,

        )

        operacion = OperacionAuditoria.INSERT

        descripcion = (
            f'Beneficiario '
            f'"{beneficiario.nombre} {beneficiario.apellido}" '
            f'asignado al programa "{programa.nombre}".'
        )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programa_beneficiario",

        operacion=operacion,

        accion=AccionAuditoria.CREAR_ASIGNACION_BENEFICIARIO,

        id_registro=asignacion.pk,

        descripcion=descripcion,

    )

    return asignacion


@transaction.atomic
def desasignar_beneficiario(
    asignacion,
    usuario_actual,
):
    """
    Desactiva una asignación existente entre un beneficiario
    y un programa.
    """

    if not asignacion.estado:

        raise ValueError(
            "La asignación ya se encuentra desactivada."
        )

    asignacion.estado = False

    asignacion.save(
        update_fields=[
            "estado",
        ]
    )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="programa_beneficiario",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.DESASIGNAR_BENEFICIARIO,

        id_registro=asignacion.pk,

        descripcion=(
            f'Beneficiario '
            f'"{asignacion.beneficiario.nombre} '
            f'{asignacion.beneficiario.apellido}" '
            f'desasignado del programa '
            f'"{asignacion.programa.nombre}".'
        ),

    )

    return asignacion


def obtener_programas_beneficiario(beneficiario):
    """
    Obtiene los programas activos asignados a un beneficiario.
    """

    return (
        ProgramaBeneficiario.objects
        .filter(
            beneficiario=beneficiario,
            estado=True,
        )
        .select_related(
            "programa",
        )
        .order_by(
            "programa__nombre",
        )
    )


# ==============================================================================
# Insumos
# ==============================================================================

def obtener_insumos(request):

    """
    Obtiene el listado paginado de insumos aplicando:

    - filtro por estado
    - búsqueda
    - ordenamiento
    - paginación
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

    queryset = Insumo.objects.all()

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
        )

    queryset = queryset.order_by(
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

        "insumos": page_obj,

        "page_obj": page_obj,

        "search_value": q,

        "status_value": status,

        "visible_pages": obtener_paginas_visibles(
            page_obj
        ),

        "query_string": params.urlencode(),

    }


@transaction.atomic
def crear_insumo(formulario, usuario_actual):

    """
    Guarda un nuevo insumo y registra la acción
    realizada por el usuario.
    """

    insumo = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="insumos",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.CREAR_INSUMO,

        id_registro=insumo.pk,

        descripcion=(
            f'Insumo "{insumo.nombre}" creado.'
        ),

    )

    return insumo


def obtener_insumo(pk):

    """
    Obtiene un insumo por su identificador.
    """

    return get_object_or_404(
        Insumo,
        pk=pk,
    )


def obtener_movimientos_insumo(insumo):

    return (
        MovimientoInsumo.objects
        .filter(
            insumo=insumo
        )
        .select_related(
            "usuario_responsable",
        )
        .order_by(
            "-fecha_movimiento",
        )
    )


@transaction.atomic
def actualizar_insumo(formulario, usuario_actual):

    """
    Actualiza la información de un insumo y registra
    la acción realizada por el usuario.

    El stock actual no es modificado por esta operación.
    """

    insumo = formulario.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="insumos",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.EDITAR_INSUMO,

        id_registro=insumo.pk,

        descripcion=(
            f'Insumo "{insumo.nombre}" actualizado.'
        ),

    )

    return insumo


@transaction.atomic
def desactivar_insumo(insumo, usuario_actual):

    """
    Realiza la desactivación lógica del insumo y registra
    la acción realizada por el usuario.
    """

    if not insumo.estado:

        return insumo

    insumo.estado = False

    insumo.save(
        update_fields=[
            "estado",
        ]
    )

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="insumos",

        operacion=OperacionAuditoria.UPDATE,

        accion=AccionAuditoria.DESACTIVAR_INSUMO,

        id_registro=insumo.pk,

        descripcion=(
            f'Insumo "{insumo.nombre}" desactivado.'
        ),

    )

    return insumo


@transaction.atomic
def registrar_movimiento_insumo(
    formulario,
    usuario_actual,
):
    """
    Registra un movimiento de inventario.

    El stock_actual no se modifica desde Django.
    La actualización corresponde a los triggers SQL.
    """

    movimiento = formulario.save(
        commit=False
    )

    movimiento.usuario_responsable = usuario_actual

    movimiento.save()

    if movimiento.tipo_movimiento == TipoMovimiento.ENTRADA:

        accion = (
            AccionAuditoria.REGISTRAR_ENTRADA_INSUMO
        )

        descripcion = (
            f"Entrada de {movimiento.cantidad} "
            f"{movimiento.insumo.get_unidad_medida_display()} "
            f'de "{movimiento.insumo.nombre}".'
        )

    elif movimiento.tipo_movimiento == TipoMovimiento.SALIDA:

        accion = (
            AccionAuditoria.REGISTRAR_SALIDA_INSUMO
        )

        descripcion = (
            f"Salida de {movimiento.cantidad} "
            f"{movimiento.insumo.get_unidad_medida_display()} "
            f'de "{movimiento.insumo.nombre}".'
        )

    else:

        raise ValidationError(
            "Tipo de movimiento no válido."
        )

    registrar_auditoria(
        usuario=usuario_actual,
        tabla="movimientos_insumos",
        operacion=OperacionAuditoria.INSERT,
        accion=accion,
        id_registro=movimiento.pk,
        descripcion=descripcion,
    )

    return movimiento


@transaction.atomic
def registrar_consumo_insumo(
    formulario,
    actividad,
    usuario_actual,
):
    """
    Registra el consumo de un insumo dentro de una actividad.

    El stock_actual no se modifica desde Django.
    La actualización corresponde al trigger SQL
    de detalle_actividad_insumo.
    """

    detalle = formulario.save(
        commit=False
    )

    detalle.actividad = actividad
    insumo = detalle.insumo

    if not actividad.estado:

        raise ValidationError(
            "No se puede registrar consumo "
            "para una actividad inactiva."
        )

    if not actividad.programa.estado:

        raise ValidationError(
            "No se puede registrar consumo "
            "porque la actividad pertenece "
            "a un programa inactivo."
        )

    if not insumo.estado:

        raise ValidationError(
            "No se puede registrar consumo "
            "para un insumo inactivo."
        )

    detalle.save()

    registrar_auditoria(

        usuario=usuario_actual,

        tabla="detalle_actividad_insumo",

        operacion=OperacionAuditoria.INSERT,

        accion=AccionAuditoria.REGISTRAR_CONSUMO_INSUMO,

        id_registro=detalle.actividad.pk,

        descripcion=(
            f'Consumo de {detalle.cantidad_usada} '
            f'{insumo.get_unidad_medida_display()} '
            f'de "{insumo.nombre}" '
            f'en la actividad "{actividad.nombre}".'
        ),

    )

    return detalle