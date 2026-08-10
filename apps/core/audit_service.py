from apps.core.models import Auditoria


def registrar_auditoria(
    usuario,
    tabla,
    operacion,
    accion,
    id_registro,
    descripcion="",
):
    """
    Registra una acción realizada por un usuario.
    """

    return Auditoria.objects.create(

        tabla_afectada=tabla,

        operacion=operacion,

        accion=accion,

        id_registro=id_registro,

        descripcion=descripcion,

        usuario_responsable=usuario,

    )