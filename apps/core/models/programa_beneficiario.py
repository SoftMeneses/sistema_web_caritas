from django.db import models

from .base import AsignacionBase
from .beneficiario import Beneficiario
from .programa import Programa

class ProgramaBeneficiario(AsignacionBase):

    programa = models.ForeignKey(
        Programa,
        on_delete=models.PROTECT,
        db_column="id_programa",
        related_name="beneficiarios_asignados"
    )

    beneficiario = models.ForeignKey(
        Beneficiario,
        on_delete=models.PROTECT,
        db_column="id_beneficiario",
        related_name="programas_asignados"
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "programa_beneficiario"

        verbose_name = "Asignación de Beneficiario"

        verbose_name_plural = "Asignaciones de Beneficiarios"

        ordering = ("-fecha_asignacion",)
        
        constraints = [

            # Emula la clave primaria compuesta del diseño original.

            models.UniqueConstraint(

                fields=("programa", "beneficiario"),

                name="pk_programa_beneficiario"
            )

        ]

    def __str__(self):

        return f"{self.beneficiario} - {self.programa}"