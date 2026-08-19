# Vistas

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404, 
    render, 
    redirect,
) 

from django.views.decorators.http import require_POST

from apps.core.models import ProgramaBeneficiario

from apps.core.forms import (

    ProgramaForm,
    ActividadForm,
    BeneficiarioForm,
    ProgramaBeneficiarioForm,

)

from .services import ( 

    obtener_dashboard,

    obtener_programas,
    crear_programa,
    obtener_programa,
    actualizar_programa,
    desactivar_programa,

    obtener_actividades,
    crear_actividad,
    obtener_actividad,
    actualizar_actividad,
    desactivar_actividad,

    obtener_beneficiarios,
    crear_beneficiario,
    obtener_beneficiario,
    actualizar_beneficiario,
    desactivar_beneficiario,

    obtener_programas_beneficiario,
    asignar_beneficiario,
    desasignar_beneficiario,

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

            crear_programa(formulario, request.user)

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

            actualizar_programa(formulario, request.user)

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

    desactivar_programa(programa, request.user)

    messages.success(

        request,

        "Programa desactivado correctamente."

    )
        
    return redirect(

        "core:programa_lista"

    )


# ==============================================================================
# Actividades
# ==============================================================================

@login_required
def actividad_lista(request):
    """
    Muestra el listado paginado de actividades.
    """

    contexto = obtener_actividades(request)

    contexto["usuario"] = request.user

    return render(

        request,

        "core/actividad/lista.html",

        contexto,

    )


@login_required
def actividad_crear(request):
    """
    Gestiona la creación de una nueva actividad.
    """

    if request.method == "POST":

        formulario = ActividadForm(

            request.POST

        )

        if formulario.is_valid():

            crear_actividad(

                formulario,

                request.user,

            )

            messages.success(

                request,

                "Actividad registrada correctamente."

            )

            return redirect(

                "core:actividad_lista"

            )

    else:

        formulario = ActividadForm()

    contexto = {

        "form": formulario,

        "modo": "crear",

    }

    return render(

        request,

        "core/actividad/form.html",

        contexto,

    )


@login_required
def actividad_detalle(request, pk):
    """
    Muestra el detalle de una actividad.
    """

    actividad = obtener_actividad(pk)

    contexto = {

        "actividad": actividad,

    }

    return render(

        request,

        "core/actividad/detalle.html",

        contexto,

    )


@login_required
def actividad_editar(request, pk):
    """
    Gestiona la edición de una actividad existente.
    """

    actividad = obtener_actividad(pk)

    if not actividad.programa.estado:

        messages.error(

            request,

            "No puede modificar esta actividad porque "
            "pertenece a un programa inactivo."

        )

        return redirect(

            "core:actividad_detalle",

            pk=actividad.pk,

        )

    if request.method == "POST":

        formulario = ActividadForm(

            request.POST,

            instance=actividad,

        )

        if formulario.is_valid():

            try:

                actualizar_actividad(

                    formulario,

                    request.user,

                )

                messages.success(

                    request,

                    "Actividad actualizada correctamente."

                )

                return redirect(

                    "core:actividad_lista"

                )

            except ValueError as error:

                messages.error(

                    request,

                    str(error),

                )

    else:

        formulario = ActividadForm(

            instance=actividad,

        )

    contexto = {

        "form": formulario,

        "modo": "editar",

        "actividad": actividad,

    }

    return render(

        request,

        "core/actividad/form.html",

        contexto,

    )


@login_required
@require_POST
def actividad_desactivar(request, pk):
    """
    Realiza la desactivación lógica de una actividad.
    """

    actividad = obtener_actividad(pk)

    try:

        desactivar_actividad(

            actividad,

            request.user,

        )

        messages.success(

            request,

            "Actividad desactivada correctamente."

        )

    except ValueError as error:

        messages.error(

            request,

            str(error),

        )

    return redirect(

        "core:actividad_lista"

    )


# ==============================================================================
# Beneficiarios
# ==============================================================================

@login_required
def beneficiario_lista(request):
    """
    Muestra el listado paginado de beneficiarios.
    """

    contexto = obtener_beneficiarios(request)

    contexto["usuario"] = request.user

    return render(

        request,

        "core/beneficiario/lista.html",

        contexto,

    )


@login_required
def beneficiario_crear(request):
    """
    Gestiona la creación de un nuevo beneficiario.
    """

    if request.method == "POST":

        formulario = BeneficiarioForm(
            request.POST
        )

        if formulario.is_valid():

            crear_beneficiario(
                formulario,
                request.user,
            )

            messages.success(

                request,

                "Beneficiario registrado correctamente."

            )

            return redirect(
                "core:beneficiario_lista"
            )

    else:

        formulario = BeneficiarioForm()

    contexto = {

        "form": formulario,

        "modo": "crear",

    }

    return render(

        request,

        "core/beneficiario/form.html",

        contexto,

    )


@login_required
def beneficiario_detalle(request, pk):
    """
    Muestra el detalle de un beneficiario y los programas
    a los que se encuentra asignado.
    """

    beneficiario = obtener_beneficiario(pk)

    programas_asignados = obtener_programas_beneficiario(
        beneficiario
    )

    contexto = {

        "beneficiario": beneficiario,

        "programas_asignados": programas_asignados,

    }

    return render(

        request,

        "core/beneficiario/detalle.html",

        contexto,

    )


@login_required
def beneficiario_editar(request, pk):
    """
    Gestiona la edición de un beneficiario existente.
    """

    beneficiario = obtener_beneficiario(pk)

    if request.method == "POST":

        formulario = BeneficiarioForm(

            request.POST,

            instance=beneficiario,

        )

        if formulario.is_valid():

            actualizar_beneficiario(

                formulario,

                request.user,

            )

            messages.success(

                request,

                "Beneficiario actualizado correctamente."

            )

            return redirect(
                "core:beneficiario_lista"
            )

    else:

        formulario = BeneficiarioForm(

            instance=beneficiario,

        )

    contexto = {

        "form": formulario,

        "modo": "editar",

        "beneficiario": beneficiario,

    }

    return render(

        request,

        "core/beneficiario/form.html",

        contexto,

    )


@login_required
@require_POST
def beneficiario_desactivar(request, pk):
    """
    Realiza la desactivación lógica de un beneficiario.
    """

    beneficiario = obtener_beneficiario(pk)

    desactivar_beneficiario(

        beneficiario,

        request.user,

    )

    messages.success(

        request,

        "Beneficiario desactivado correctamente."

    )

    return redirect(

        "core:beneficiario_lista"

    )


@login_required
def beneficiario_asignar_programa(request, pk):
    """
    Gestiona la asignación de un beneficiario a un programa.
    """

    beneficiario = obtener_beneficiario(pk)

    if not beneficiario.estado:

        messages.error(

            request,

            "No se pueden asignar programas a un beneficiario inactivo."

        )

        return redirect(

            "core:beneficiario_detalle",

            pk=beneficiario.pk,

        )

    if request.method == "POST":

        formulario = ProgramaBeneficiarioForm(
            request.POST,
            beneficiario=beneficiario,
        )

        if formulario.is_valid():

            asignar_beneficiario(

                formulario,

                beneficiario,

                request.user,

            )

            messages.success(

                request,

                "Programa asignado correctamente."

            )

            return redirect(

                "core:beneficiario_detalle",

                pk=beneficiario.pk,

            )

    else:

        formulario = ProgramaBeneficiarioForm(

            beneficiario=beneficiario,
        )

    contexto = {

        "form": formulario,

        "beneficiario": beneficiario,

    }

    return render(

        request,

        "core/beneficiario/asignar_programa.html",

        contexto,

    )


@login_required
@require_POST
def beneficiario_desasignar_programa(
    request,
    pk,
    asignacion_pk,
):
    """
    Realiza la desasignación lógica de un programa
    perteneciente a un beneficiario.
    """

    beneficiario = obtener_beneficiario(pk)

    asignacion = get_object_or_404(

        ProgramaBeneficiario.objects.select_related(

            "beneficiario",
            "programa",

        ),

        pk=asignacion_pk,

        beneficiario=beneficiario,

    )

    desasignar_beneficiario(

        asignacion,

        request.user,

    )

    messages.success(

        request,

        "Programa desasignado correctamente."

    )

    return redirect(

        "core:beneficiario_detalle",

        pk=beneficiario.pk,

    )