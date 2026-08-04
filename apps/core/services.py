from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404

from apps.core.models import Programa


def obtener_dashboard():

    return {

        "usuario": "",

        "fecha": datetime.now(),

        "programas": 0,

        "actividades": 0,

        "beneficiarios": 0,

        "inventario": 0,

    }


def obtener_programas(request):

    """
    Obtiene el listado de programas aplicando:

    - búsqueda
    - ordenamiento
    - paginación

    Retorna el contexto requerido por la vista lista.html.
    """

    queryset = (

        Programa.objects

        .select_related("usuario_responsable")

        .all()

        .order_by("nombre")
    )

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

    paginator = Paginator(

        queryset,

        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return {

        "programas": page_obj,

        "search_value": q,

        "visible_pages": obtener_paginas_visibles(page_obj),

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


def crear_programa(formulario):
    """
    Guarda un nuevo programa en la base de datos.

    Parámetros:
        formulario (ProgramaForm): formulario validado.

    Retorna:
        Programa: instancia creada.
    """

    programa = formulario.save()

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
