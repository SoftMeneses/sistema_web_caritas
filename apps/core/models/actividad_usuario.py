from django.db import models

from apps.seguridad.models import Usuario

from .actividad import Actividad


class ActividadUsuario(models.Model):

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.PROTECT,
        db_column="id_actividad",
        related_name="asignaciones_usuarios"
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario",
        related_name="asignaciones_actividades"
    )

    rol_en_actividad = models.CharField(
        max_length=50
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "actividad_usuario"

        verbose_name = "Asignación de Actividad"

        verbose_name_plural = "Asignaciones de Actividades"

        ordering = [
            "-fecha_asignacion"
        ]

        constraints = [

            models.UniqueConstraint(

                fields=[

                    "actividad",

                    "usuario"

                ],

                name="pk_actividad_usuario"

            )

        ]

    def __str__(self):

        return f"{self.usuario} - {self.actividad}"