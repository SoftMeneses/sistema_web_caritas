from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):

    list_display = (
        "id_rol",
        "nombre",
        "estado",
    )

    list_filter = (
        "estado",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )

    list_per_page = 20


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    
    """
    Personalización del panel de administración para el modelo Usuario.
    Conserva toda la funcionalidad de UserAdmin e incorpora los campos
    adicionales definidos en el modelo personalizado.
    """

    model = Usuario

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cedula",
        "rol",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "rol",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cedula",
    )

    ordering = (
        "username",
    )

    list_per_page = 20

    fieldsets = UserAdmin.fieldsets + (

        (
            "Información adicional",

            {

                "fields": (

                    "cedula",

                    "telefono",

                    "rol",

                )

            },

        ),

    )

    add_fieldsets = UserAdmin.add_fieldsets + (

        (
            "Información adicional",

            {

                "fields": (

                    "cedula",

                    "telefono",

                    "rol",

                )

            },

        ),

    )