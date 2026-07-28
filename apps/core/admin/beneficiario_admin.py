from django.contrib import admin

from apps.core.models import Beneficiario


@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Beneficiario.
    """

    list_display = (
        "cedula",
        "nombre",
        "apellido",
        "telefono",
        "estado",
    )

    list_display_links = (
        "cedula",
    )

    search_fields = (
        "cedula",
        "nombre",
        "apellido",
        "telefono",
    )

    list_filter = (
        "estado",
    )

    ordering = (
        "apellido",
        "nombre",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Información personal",
            {
                "fields": (
                    "cedula",
                    "nombre",
                    "apellido",
                ),
            },
        ),
        (
            "Información de contacto",
            {
                "fields": (
                    "telefono",
                    "direccion",
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