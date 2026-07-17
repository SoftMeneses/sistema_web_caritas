from django.db import models

from apps.seguridad.models import Usuario

from .choices import TipoMovimiento

from .insumo import Insumo


class MovimientoInsumo(models.Model):

    id_movimiento = models.AutoField(
        primary_key=True
    )

    tipo_movimiento = models.CharField(
        max_length=10,
        choices=TipoMovimiento.choices
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True
    )

    observacion = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        db_column="id_insumo",
        related_name="movimientos"
    )

    usuario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario_responsable",
        related_name="movimientos_insumos"
    )

    class Meta:

        db_table = "movimientos_insumos"

        verbose_name = "Movimiento de Insumo"

        verbose_name_plural = "Movimientos de Insumos"

        ordering = [
            "-fecha_movimiento"
        ]

    def __str__(self):

        return f"{self.get_tipo_movimiento_display()} - {self.insumo}"