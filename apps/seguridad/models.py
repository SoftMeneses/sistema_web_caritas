from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UsuarioManager


class Rol(models.Model):

    id_rol = models.AutoField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.TextField(
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

    first_name = models.CharField(
        max_length=150
    )

    last_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        max_length=254,
        unique=True
    )

    cedula = models.CharField(
        max_length=20,
        unique=True
    )

    telefono = models.CharField(
        max_length=25,
        blank=True
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        db_column="id_rol",
        related_name="usuarios"
    )

    objects = UsuarioManager()

    class Meta:

        db_table = "usuarios"

        verbose_name = "Usuario"

        verbose_name_plural = "Usuarios"

    def __str__(self):

        return self.get_full_name() or self.username
