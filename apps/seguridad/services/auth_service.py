from django.contrib.auth import authenticate, login
from ..forms import LoginForm


def obtener_formulario_login(request=None):

    if request:

        return LoginForm(request, data=request.POST or None)

    return LoginForm()


def autenticar_usuario(request):

    formulario = LoginForm(request, data=request.POST)

    if formulario.is_valid():

        usuario = authenticate(

            request,

            username=formulario.cleaned_data["username"],

            password=formulario.cleaned_data["password"]

        )

        if usuario:

            login(request, usuario)

            return True, formulario

    return False, formulario