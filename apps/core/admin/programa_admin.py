from django.contrib import admin
from django.db import transaction

from apps.core.audit_service import registrar_auditoria
from apps.core.models import Programa
from apps.core.models.choices import (
    OperacionAuditoria,
    AccionAuditoria,
)


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

    def save_model(self, request, obj, form, change):
        """
        Registra la creación o modificación de un programa
        realizada desde Django Admin.
        """

        with transaction.atomic():

            super().save_model(

                request,

                obj,

                form,

                change,

            )

            if change:

                operacion = OperacionAuditoria.UPDATE

                accion = AccionAuditoria.EDITAR_PROGRAMA

                descripcion = (
                    f'Programa "{obj.nombre}" actualizado '
                    "desde el panel de administración."
                )

            else:

                operacion = OperacionAuditoria.INSERT

                accion = AccionAuditoria.CREAR_PROGRAMA

                descripcion = (
                    f'Programa "{obj.nombre}" creado '
                    "desde el panel de administración."
                )

            registrar_auditoria(

                usuario=request.user,

                tabla="programas",

                operacion=operacion,

                accion=accion,

                id_registro=obj.pk,

                descripcion=descripcion,

            )

    def delete_model(self, request, obj):
        """
        Registra la eliminación física del programa
        antes de eliminarlo desde Django Admin.
        """

        with transaction.atomic():

            registrar_auditoria(

                usuario=request.user,

                tabla="programas",

                operacion=OperacionAuditoria.DELETE,

                accion=AccionAuditoria.ELIMINAR_PROGRAMA,

                id_registro=obj.pk,

                descripcion=(
                    f'Programa "{obj.nombre}" eliminado físicamente '
                    "desde el panel de administración."
                ),

            )

            super().delete_model(

                request,

                obj,

            )

    def delete_queryset(self, request, queryset):
        """
        Registra la eliminación física de los programas
        eliminados mediante la acción masiva del administrador.
        """

        with transaction.atomic():

            programas = list(

                queryset.values(
                    "pk",
                    "nombre",
                )

            )

            for programa in programas:

                registrar_auditoria(

                    usuario=request.user,

                    tabla="programas",

                    operacion=OperacionAuditoria.DELETE,

                    accion=AccionAuditoria.ELIMINAR_PROGRAMA,

                    id_registro=programa["pk"],

                    descripcion=(
                        f'Programa "{programa["nombre"]}" eliminado físicamente '
                        "desde el panel de administración."
                    ),

                )

            super().delete_queryset(

                request,

                queryset,

            )