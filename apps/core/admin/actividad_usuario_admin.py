from django.contrib import admin

from apps.core.models import ActividadUsuario


@admin.register(ActividadUsuario)
class ActividadUsuarioAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ActividadUsuario.
    """

    list_display = (
        "actividad",
        "usuario",
        "rol_en_actividad",
        "fecha_asignacion",
    )

    list_display_links = (
        "actividad",
    )

    search_fields = (
        "actividad__nombre",
        "usuario__cedula",
        "usuario__first_name",
        "usuario__last_name",
        "rol_en_actividad",
    )

    list_filter = (
        "actividad",
        "rol_en_actividad",
        "fecha_asignacion",
    )

    autocomplete_fields = (
        "actividad",
        "usuario",
    )

    list_select_related = (
        "actividad",
        "usuario",
    )

    readonly_fields = (
        "fecha_asignacion",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Asignación",
            {
                "fields": (
                    "actividad",
                    "usuario",
                    "rol_en_actividad",
                ),
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "fecha_asignacion",
                ),
            },
        ),
    )