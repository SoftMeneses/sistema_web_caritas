from django.contrib import admin

from ..models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Auditoria.
    """

    list_display = (
        "fecha_auditoria",
        "tabla_afectada",
        "operacion",
        "accion",
        "id_registro",
        "usuario_responsable",
    )

    list_display_links = (
        "fecha_auditoria",
    )

    search_fields = (
        "tabla_afectada",
        "descripcion",
        "usuario_responsable__username",
        "usuario_responsable__first_name",
        "usuario_responsable__last_name",
    )

    list_filter = (
        "operacion",
        "accion",
        "tabla_afectada",
        "fecha_auditoria",
    )

    ordering = (
        "-fecha_auditoria",
    )

    autocomplete_fields = (
        "usuario_responsable",
    )

    list_select_related = (
        "usuario_responsable",
    )

    readonly_fields = (
        "tabla_afectada",
        "operacion",
        "accion",
        "id_registro",
        "descripcion",
        "fecha_auditoria",
        "usuario_responsable",
    )

    list_per_page = 20

    save_on_top = True

    date_hierarchy = "fecha_auditoria"

    fieldsets = (
        (
            "Información de la auditoría",
            {
                "fields": (
                    "tabla_afectada",
                    "operacion",
                    "accion",
                    "id_registro",
                    "descripcion",
                ),
            },
        ),
        (
            "Información de registro",
            {
                "fields": (
                    "fecha_auditoria",
                    "usuario_responsable",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        """
        Impide crear registros de auditoría manualmente.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Impide modificar registros de auditoría.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Impide eliminar registros de auditoría.
        """
        return False