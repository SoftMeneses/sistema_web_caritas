from django.contrib import admin

from .models import (
    Actividad,
    ActividadUsuario,
    Auditoria,
    Beneficiario,
    DetalleActividadInsumo,
    Insumo,
    MovimientoInsumo,
    Programa,
    ProgramaBeneficiario,
    ProgramaUsuario,
)


admin.site.register(Programa)

admin.site.register(Actividad)

admin.site.register(Beneficiario)

admin.site.register(ProgramaUsuario)

admin.site.register(ActividadUsuario)

admin.site.register(ProgramaBeneficiario)

admin.site.register(Insumo)

admin.site.register(MovimientoInsumo)

admin.site.register(DetalleActividadInsumo)

admin.site.register(Auditoria)