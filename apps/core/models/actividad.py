from django.db import models

from apps.seguridad.models import Usuario

from .programa import Programa


class Actividad(models.Model):

    id_actividad = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    fecha_actividad = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.BooleanField(
        default=True
    )

    programa = models.ForeignKey(
        Programa,
        on_delete=models.PROTECT,
        db_column="id_programa",
        related_name="actividades"
    )

    usuario_creador = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario_creador",
        related_name="actividades_creadas"
    )

    class Meta:

        db_table = "actividades"

        verbose_name = "Actividad"

        verbose_name_plural = "Actividades"

        ordering = [
            "-fecha_actividad"
        ]

    def __str__(self):

        return self.nombre