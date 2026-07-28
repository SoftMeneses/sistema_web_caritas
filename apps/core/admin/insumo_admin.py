from django.contrib import admin

from apps.core.models import Insumo


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Insumo.
    """

    list_display = (
        "nombre",
        "stock_actual",
        "unidad_medida",
        "estado",
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
        "unidad_medida",
    )

    ordering = (
        "nombre",
    )

    readonly_fields = (
        "stock_actual",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Información del insumo",
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "unidad_medida",
                ),
            },
        ),
        (
            "Inventario",
            {
                "fields": (
                    "stock_actual",
                ),
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "estado",
                ),
            },
        ),
    )