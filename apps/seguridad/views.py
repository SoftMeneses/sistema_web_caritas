from django.shortcuts import redirect, render

from .services import autenticar_usuario, obtener_formulario_login

from django.contrib.auth import logout


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

    logout(request)

    return redirect("seguridad:login")