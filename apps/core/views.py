# Vistas

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from apps.core.forms import ProgramaForm

from .services import ( 

    obtener_dashboard,

    obtener_programas,

    crear_programa,

    obtener_programa,

)


@login_required
def dashboard(request):

    contexto = obtener_dashboard()

    contexto["usuario"] = request.user

    return render(

        request,

        "dashboard/dashboard.html",

        contexto

    )


@login_required
def programa_lista(request):

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
    Muestra el formulario para registrar un nuevo programa.
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

    }

    return render(

        request,

        "core/programa/form.html",

        contexto,

    )

@login_required
def programa_detalle(request, pk):

    programa = obtener_programa(pk)

    contexto = {

        "programa": programa,

    }

    return render(

        request,

        "core/programa/detalle.html",

        contexto,

    )
