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


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    model = Usuario

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cedula",
        "rol",
        "is_active",
    )

    list_filter = (
        "rol",
        "is_active",
        "is_staff",
    )

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