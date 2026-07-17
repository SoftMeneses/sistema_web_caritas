from django.db import models

class UnidadMedida(models.TextChoices):

    UNIDAD = "Unidad", "Unidad"

    KILOGRAMO = "Kg", "Kilogramo"

    GRAMO = "g", "Gramo"

    LITRO = "L", "Litro"

    MILILITRO = "mL", "Mililitro"

    CAJA = "Caja", "Caja"

    PAQUETE = "Paquete", "Paquete"

    FARDO = "Fardo", "Fardo"

    SACO = "Saco", "Saco"

    METRO = "Metro", "Metro"

class TipoMovimiento(models.TextChoices):

    ENTRADA = "entrada", "Entrada"

    SALIDA = "salida", "Salida"

class OperacionAuditoria(models.TextChoices):

    INSERT = "INSERT", "Inserción"

    UPDATE = "UPDATE", "Actualización"

    DELETE = "DELETE", "Eliminación"