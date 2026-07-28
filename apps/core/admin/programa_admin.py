from django.contrib import admin

from apps.core.models import Programa


@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Programa.
    """

    list_display = (
        "nombre",
        "fecha_inicio",
        "fecha_fin",
        "estado",
        "usuario_responsable",
    )

    list_display_links = (
        "nombre",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    list_filter = (
        "estado",
        "fecha_inicio",
        "fecha_fin",
    )

    ordering = (
        "nombre",
    )

    autocomplete_fields = (
        "usuario_responsable",
    )

    list_select_related = (
        "usuario_responsable",
    )

    list_per_page = 20