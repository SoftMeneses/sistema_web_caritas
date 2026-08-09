def es_administrador(usuario):
    """
    Determina si el usuario posee el rol Administrador
    y dicho rol se encuentra activo.
    """

    return (
        usuario.is_authenticated
        and usuario.rol is not None
        and usuario.rol.estado
        and usuario.rol.nombre == "Administrador"
    )