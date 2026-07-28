from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Rol, Usuario

admin.site.site_header = "Sistema de Información Cáritas San Cristóbal"
admin.site.site_title = "Administración"
admin.site.index_title = "Panel de Administración"


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Rol.
    """

    list_display = (
        "id_rol",
        "nombre",
        "estado",
    )

    list_display_links = (
        "nombre",
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
    Configuración del panel de administración para el modelo Usuario.
    """

    model = Usuario

    list_display = (
        "username",
        "nombre_completo",
        "email",
        "cedula",
        "rol",
        "is_active",
        "is_staff",
    )

    list_display_links = (
        "username",
    )

    search_fields = (
        "username",
        "cedula",
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "rol",
        "groups",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    ordering = (
        "username",
    )

    autocomplete_fields = (
        "rol",
    )

    list_select_related = (
        "rol",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    list_per_page = 20

    save_on_top = True

    fieldsets = (
        (
            "Información de acceso",
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Información personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "cedula",
                    "telefono",
                    "rol",
                ),
            },
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Fechas importantes",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "cedula",
                    "telefono",
                    "rol",
                    "password1",
                    "password2",
                    "is_active",
                ),
            },
        ),
    )

    @admin.display(description="Nombre completo", ordering="first_name")
    def nombre_completo(self, obj):
        nombre = obj.get_full_name()
        return nombre if nombre else "-"