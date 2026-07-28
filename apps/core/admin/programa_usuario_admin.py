from django.contrib import admin

from apps.core.models import ProgramaUsuario


@admin.register(ProgramaUsuario)
class ProgramaUsuarioAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ProgramaUsuario.
    """

    list_display = (
        "programa",
        "usuario",
        "rol_en_programa",
        "fecha_asignacion",
    )

    list_display_links = (
        "programa",
    )

    search_fields = (
        "programa__nombre",
        "usuario__cedula",
        "usuario__first_name",
        "usuario__last_name",
        "rol_en_programa",
    )

    list_filter = (
        "programa",
        "rol_en_programa",
        "fecha_asignacion",
    )

    autocomplete_fields = (
        "programa",
        "usuario",
    )

    list_select_related = (
        "programa",
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
                    "programa",
                    "usuario",
                    "rol_en_programa",
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