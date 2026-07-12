# Vistas

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import obtener_dashboard


@login_required
def dashboard(request):

    contexto = obtener_dashboard()

    contexto["usuario"] = request.user

    return render(

        request,

        "dashboard/dashboard.html",

        contexto

    )
