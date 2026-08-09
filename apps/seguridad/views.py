from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.seguridad.decorators import administrador_required
from apps.seguridad.forms import UsuarioForm
from apps.seguridad.services import (
    autenticar_usuario,
    obtener_formulario_login,
    obtener_usuarios,
    crear_usuario,
    obtener_usuario,
    actualizar_usuario,
    desactivar_usuario,
)


def login_view(request):

    if request.method == "POST":

        autenticado, formulario = autenticar_usuario(request)

        if autenticado:

            return redirect("core:dashboard")

    else:

        formulario = obtener_formulario_login()

    return render(

        request,

        "seguridad/login.html",

        {

            "form": formulario

        }

    )


def logout_view(request):
    """
    Cierra la sesión del usuario autenticado.
    """

    logout(request)

    return redirect("seguridad:login")


@login_required
@administrador_required
def usuario_lista(request):
    """
    Muestra el listado paginado de usuarios.
    """

    contexto = obtener_usuarios(request)

    contexto["usuario"] = request.user

    return render(

        request,

        "seguridad/usuario/lista.html",

        contexto,

    )


@login_required
@administrador_required
def usuario_crear(request):
    """
    Muestra el formulario para registrar un nuevo usuario.
    """

    if request.method == "POST":

        formulario = UsuarioForm(request.POST)

        if formulario.is_valid():

            crear_usuario(formulario)

            messages.success(

                request,

                "Usuario registrado correctamente."

            )

            return redirect(

                "seguridad:usuario_lista",

            )

    else:

        formulario = UsuarioForm()

    contexto = {

        "form": formulario,

        "modo": "crear",

        "titulo": "Nuevo usuario",

    }

    return render(

        request,

        "seguridad/usuario/form.html",

        contexto,

    )


@login_required
@administrador_required
def usuario_detalle(request, pk):
    """
    Muestra el detalle de un usuario.
    """

    usuario = obtener_usuario(pk)

    contexto = {

        "usuario": usuario,

    }

    return render(

        request,

        "seguridad/usuario/detalle.html",

        contexto,

    )


@login_required
@administrador_required
def usuario_editar(request, pk):
    """
    Actualiza la información de un usuario existente.
    """

    usuario = obtener_usuario(pk)

    if request.method == "POST":

        formulario = UsuarioForm(

            request.POST,

            instance=usuario,

        )

        if formulario.is_valid():

            try:
            
                actualizar_usuario(
                    formulario,
                    request.user,
                )
        
                messages.success(
                    request,
                    "Usuario actualizado correctamente."
                )
        
                return redirect(
                    "seguridad:usuario_lista",
                )
        
            except ValueError as error:
            
                messages.error(
                    request,
                    str(error),
                )

    else:

        formulario = UsuarioForm(

            instance=usuario,

        )

    contexto = {

        "form": formulario,

        "modo": "editar",

        "usuario": usuario,

    }

    return render(

        request,

        "seguridad/usuario/form.html",

        contexto,

    )


@login_required
@administrador_required
@require_POST
def usuario_desactivar(request, pk):
    """
    Realiza la desactivación lógica de un usuario.
    """

    usuario = obtener_usuario(pk)

    try:

        desactivar_usuario(

            usuario,

            request.user,

        )

        messages.success(

            request,

            "Usuario desactivado correctamente."

        )

    except ValueError as error:

        messages.error(

            request,

            str(error),

        )

    return redirect(

        "seguridad:usuario_lista",

    )