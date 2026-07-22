from django.db import models

from .choices import UnidadMedida

class Insumo(models.Model):

    id_insumo = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True
    )

    stock_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unidad_medida = models.CharField(
        max_length=20,
        choices=UnidadMedida.choices
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "insumos"

        verbose_name = "Insumo"

        verbose_name_plural = "Insumos"

        ordering = ("nombre",)
        

    def __str__(self):

        return self.nombre