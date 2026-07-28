from django.contrib import admin

from ..models import ProgramaBeneficiario


@admin.register(ProgramaBeneficiario)
class ProgramaBeneficiarioAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo
    ProgramaBeneficiario.
    """

    list_display = (
        "programa",
        "beneficiario",
        "estado",
        "fecha_asignacion",
    )

    list_display_links = (
        "programa",
    )

    search_fields = (
        "programa__nombre",
        "beneficiario__cedula",
        "beneficiario__nombre",
        "beneficiario__apellido",
    )

    list_filter = (
        "estado",
        "programa",
        "fecha_asignacion",
    )

    ordering = (
        "-fecha_asignacion",
    )

    autocomplete_fields = (
        "programa",
        "beneficiario",
    )

    list_select_related = (
        "programa",
        "beneficiario",
    )

    readonly_fields = (
        "fecha_asignacion",
    )

    list_per_page = 20

    save_on_top = True

    fieldsets = (
        (
            "Asignación",
            {
                "fields": (
                    "programa",
                    "beneficiario",
                    "estado",
                ),
            },
        ),
        (
            "Información de registro",
            {
                "fields": (
                    "fecha_asignacion",
                ),
            },
        ),
    )