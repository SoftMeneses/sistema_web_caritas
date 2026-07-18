from django.db import models


class AsignacionBase(models.Model):

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
