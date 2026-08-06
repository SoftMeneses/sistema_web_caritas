# Vistas

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from apps.core.forms import ProgramaForm

from .services import ( 

    obtener_dashboard,
    obtener_programas,
    crear_programa,
    obtener_programa,
    actualizar_programa,
    desactivar_programa,

)

# ==============================================================================
# Dashboard
# ==============================================================================

@login_required
def dashboard(request):
    """
    Muestra el panel principal del sistema.
    """

    contexto = obtener_dashboard()

    contexto["usuario"] = request.user

    return render(

        request,

        "dashboard/dashboard.html",

        contexto

    )


# ==============================================================================
# Programas
# ==============================================================================

@login_required
def programa_lista(request):
    """
    Muestra el listado paginado de programas.
    """

    contexto = obtener_programas(request)

    contexto["usuario"] = request.user

    return render(

        request,

        "core/programa/lista.html",

        contexto,

    )


@login_required
def programa_crear(request):
    """
    Gestiona la creación de un nuevo programa.
    """

    if request.method == "POST":

        formulario = ProgramaForm(request.POST)

        if formulario.is_valid():

            crear_programa(formulario)

            messages.success(

                request,

                "Programa registrado correctamente."

            )

            return redirect("core:programa_lista")

    else:

        formulario = ProgramaForm()

    contexto = {

        "form": formulario,

        "modo": "crear",

    }

    return render(

        request,

        "core/programa/form.html",

        contexto,

    )


@login_required
def programa_detalle(request, pk):
    """
    Muestra el detalle de un programa.
    """

    programa = obtener_programa(pk)

    contexto = {

        "programa": programa,

    }

    return render(

        request,

        "core/programa/detalle.html",

        contexto,

    )


@login_required
def programa_editar(request, pk):
    """
    Gestiona la edición de un programa existente.
    """

    programa = obtener_programa(pk)

    if request.method == "POST":

        formulario = ProgramaForm(

            request.POST, 

            instance=programa,

        )

        if formulario.is_valid():

            actualizar_programa(formulario)

            messages.success(

                request,

                "Programa actualizado correctamente."

            )

            return redirect("core:programa_lista")

    else:

        formulario = ProgramaForm(

            instance=programa,

        )

    contexto = {

        "form": formulario,

        "modo": "editar",

        "programa": programa,

    }

    return render(

        request,

        "core/programa/form.html",

        contexto,

    )


@login_required
@require_POST
def programa_desactivar(request, pk):
    """
    Realiza la desactivación lógica de un programa.
    """

    programa = obtener_programa(pk)

    desactivar_programa(programa)

    messages.success(

        request,

        "Programa desactivado correctamente."

    )
        
    return redirect(

        "core:programa_lista"

    )
