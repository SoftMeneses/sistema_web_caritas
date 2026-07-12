from django.db import models

from django.contrib.auth.models import AbstractUser


class Rol(models.Model):

    id_rol = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.CharField(
        max_length=200,
        blank=True
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "roles"

        verbose_name = "Rol"

        verbose_name_plural = "Roles"

        ordering = ["nombre"]

    def __str__(self):

        return self.nombre
    

class Usuario(AbstractUser):

    id_usuario = models.AutoField(
        primary_key=True
    )

    cedula = models.CharField(
        max_length=20,
        unique=True
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        db_column="id_rol",
        related_name="usuarios"
    )

    class Meta:

        db_table = "usuarios"

        verbose_name = "Usuario"

        verbose_name_plural = "Usuarios"

    def __str__(self):

        return self.get_full_name() or self.username
