from django.db import models

from .actividad import Actividad
from .insumo import Insumo


class DetalleActividadInsumo(models.Model):

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.PROTECT,
        db_column="id_actividad",
        related_name="insumos_utilizados"
    )

    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        db_column="id_insumo",
        related_name="consumos"
    )

    cantidad_usada = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:

        db_table = "detalle_actividad_insumo"

        verbose_name = "Insumo Utilizado"

        verbose_name_plural = "Insumos Utilizados"

        ordering = [
            "actividad"
        ]

        constraints = [

            models.UniqueConstraint(

                fields=[
                    "actividad",
                    "insumo"
                ],

                name="pk_detalle_actividad_insumo"

            )

        ]

    def __str__(self):

        return f"{self.actividad} - {self.insumo}"