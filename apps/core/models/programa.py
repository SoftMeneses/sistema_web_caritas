from django.db import models

from apps.seguridad.models import Usuario


class Programa(models.Model):

    id_programa = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(
        blank=True,
        null=True
    )

    estado = models.BooleanField(
        default=True
    )

    # Usuario encargado de la gestión del programa.
    usuario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario_responsable",
        related_name="programas_responsables"
    )

    class Meta:

        db_table = "programas"

        verbose_name = "Programa"

        verbose_name_plural = "Programas"

        ordering = ("nombre",)

    def __str__(self):

        return self.nombre