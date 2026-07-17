from django.db import models

from apps.seguridad.models import Usuario

from .programa import Programa


class ProgramaUsuario(models.Model):

    programa = models.ForeignKey(
        Programa,
        on_delete=models.PROTECT,
        db_column="id_programa",
        related_name="asignaciones_usuarios"
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario",
        related_name="asignaciones_programas"
    )

    rol_en_programa = models.CharField(
        max_length=50
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "programa_usuario"

        verbose_name = "Asignación de Programa"

        verbose_name_plural = "Asignaciones de Programas"

        ordering = [
            "-fecha_asignacion"
        ]

        constraints = [

            models.UniqueConstraint(

                fields=[

                    "programa",

                    "usuario"

                ],

                name="pk_programa_usuario"

            )

        ]

    def __str__(self):

        return f"{self.usuario} - {self.programa}"