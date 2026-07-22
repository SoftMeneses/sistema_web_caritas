from django.db import models

from apps.seguridad.models import Usuario

from .choices import OperacionAuditoria


class Auditoria(models.Model):

    id_auditoria = models.AutoField(
        primary_key=True
    )

    tabla_afectada = models.CharField(
        max_length=50
    )

    operacion = models.CharField(
        max_length=10,
        choices=OperacionAuditoria.choices
    )

    id_registro = models.IntegerField()

    descripcion = models.TextField(
        blank=True
    )

    fecha_auditoria = models.DateTimeField(
        auto_now_add=True
    )

    usuario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario_responsable",
        related_name="auditorias"
    )

    class Meta:

        db_table = "auditoria"

        verbose_name = "Auditoría"

        verbose_name_plural = "Auditorías"

        ordering = ("-fecha_auditoria",)
        

    def __str__(self):

        return (
            f"{self.get_operacion_display()} - "
            f"{self.tabla_afectada}"
        )