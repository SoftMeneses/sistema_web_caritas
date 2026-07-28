from django.contrib import admin

from apps.core.models import MovimientoInsumo


@admin.register(MovimientoInsumo)
class MovimientoInsumoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo MovimientoInsumo.
    """

    list_display = (
        "id_movimiento",
        "insumo",
        "tipo_movimiento",
        "cantidad",
        "fecha_movimiento",
        "usuario_responsable",
    )

    list_display_links = (
        "id_movimiento",
    )

    search_fields = (
        "insumo__nombre",
        "usuario_responsable__cedula",
        "usuario_responsable__first_name",
        "usuario_responsable__last_name",
        "observacion",
    )

    list_filter = (
        "tipo_movimiento",
        "fecha_movimiento",
        "insumo",
    )

    autocomplete_fields = (
        "insumo",
        "usuario_responsable",
    )

    list_select_related = (
        "insumo",
        "usuario_responsable",
    )

    readonly_fields = (
        "fecha_movimiento",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Movimiento",
            {
                "fields": (
                    "insumo",
                    "tipo_movimiento",
                    "cantidad",
                ),
            },
        ),
        (
            "Información adicional",
            {
                "fields": (
                    "observacion",
                ),
            },
        ),
        (
            "Control",
            {
                "fields": (
                    "usuario_responsable",
                    "fecha_movimiento",
                ),
            },
        ),
    )

# Habilitar permisos para impedir la modificación y eliminación de movimientos de inventario.

'''
    def has_change_permission(self, request, obj = None):
        if obj is not None:
            return False

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj = None):
            return False
'''
