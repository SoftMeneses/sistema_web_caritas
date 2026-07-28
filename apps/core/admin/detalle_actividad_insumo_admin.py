from django.contrib import admin

from ..models import DetalleActividadInsumo


@admin.register(DetalleActividadInsumo)
class DetalleActividadInsumoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo
    DetalleActividadInsumo.
    """

    list_display = (
        "actividad",
        "insumo",
        "cantidad_usada",
    )

    list_display_links = (
        "actividad",
    )

    search_fields = (
        "actividad__nombre",
        "insumo__nombre",
    )

    list_filter = (
        "actividad",
        "insumo",
    )

    ordering = (
        "actividad",
        "insumo",
    )

    autocomplete_fields = (
        "actividad",
        "insumo",
    )

    list_select_related = (
        "actividad",
        "insumo",
    )

    list_per_page = 20

    save_on_top = True

    fieldsets = (
        (
            "Información del consumo",
            {
                "fields": (
                    "actividad",
                    "insumo",
                    "cantidad_usada",
                ),
            },
        ),
    )

    # Activar las siguientes funciones para preservar el historial de consumos.
'''
    def has_change_permission(self, request, obj=None):
         return False

    def has_delete_permission(self, request, obj=None):
         return False
'''