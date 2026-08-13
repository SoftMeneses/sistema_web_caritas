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

class AccionAuditoria(models.TextChoices):

    CREAR_PROGRAMA = (
        "CREAR_PROGRAMA",
        "Crear programa",
    )

    EDITAR_PROGRAMA = (
        "EDITAR_PROGRAMA",
        "Editar programa",
    )

    DESACTIVAR_PROGRAMA = (
        "DESACTIVAR_PROGRAMA",
        "Desactivar programa",
    )

    ELIMINAR_PROGRAMA = (
        "ELIMINAR_PROGRAMA",
        "Eliminar programa",
    )

    CREAR_ACTIVIDAD = (
        "CREAR_ACTIVIDAD",
        "Crear actividad",
    )

    EDITAR_ACTIVIDAD = (
        "EDITAR_ACTIVIDAD",
        "Editar actividad",
    )

    DESACTIVAR_ACTIVIDAD = (
        "DESACTIVAR_ACTIVIDAD",
        "Desactivar actividad",
    )

    CREAR_BENEFICIARIO = (
        "CREAR_BENEFICIARIO",
        "Crear beneficiario",
    )

    EDITAR_BENEFICIARIO = (
        "EDITAR_BENEFICIARIO",
        "Editar beneficiario",
    )

    DESACTIVAR_BENEFICIARIO = (
        "DESACTIVAR_BENEFICIARIO",
        "Desactivar beneficiario",
    )