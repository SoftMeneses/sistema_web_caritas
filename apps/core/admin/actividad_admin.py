from django.contrib import admin

from apps.core.models import Actividad

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Actividad.
    """

    list_display = (
        "nombre",
        "programa",
        "fecha_actividad",
        "estado",
        "usuario_creador",
    )

    list_display_links = (
        "nombre",
    )

    search_fields = (
        "nombre",
        "descripcion",
        "programa__nombre",
        "usuario_creador__cedula",
        "usuario_creador__first_name",
        "usuario_creador__last_name",
    )

    list_filter = (
        "estado",
        "programa",
        "fecha_actividad",
    )

    ordering = (
        "-fecha_actividad",
    )

    autocomplete_fields = (
        "programa",
        "usuario_creador",
    )

    list_select_related = (
        "programa",
        "usuario_creador",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "programa",
                    "nombre",
                    "descripcion",
                ),
            },
        ),
        (
            "Planificación",
            {
                "fields": (
                    "fecha_actividad",
                    "estado",
                ),
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "usuario_creador",
                ),
            },
        ),
    )