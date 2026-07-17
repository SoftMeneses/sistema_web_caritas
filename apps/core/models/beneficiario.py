from django.db import models


class Beneficiario(models.Model):

    id_beneficiario = models.AutoField(
        primary_key=True
    )

    cedula = models.CharField(
        max_length=20,
        unique=True
    )

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=25,
        blank=True,
        null=True
    )

    direccion = models.TextField(
        blank=True,
        null=True
    )

    fecha_registro = models.DateField(
        auto_now_add=True
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "beneficiarios"

        verbose_name = "Beneficiario"

        verbose_name_plural = "Beneficiarios"

        ordering = [
            "apellido",
            "nombre"
        ]

    def __str__(self):

        return f"{self.nombre} {self.apellido}"