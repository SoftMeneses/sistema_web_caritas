from io import BytesIO

from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from .qr_service import generar_qr_beneficiario


def generar_pdf_beneficiario(beneficiario, programas_asignados):
    """
    Genera el PDF con la información de un beneficiario.

    Incluye:
    - Datos personales.
    - Estado.
    - Fecha de registro.
    - Programas asignados.
    - Código QR para consultar el beneficiario.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloCaritas",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloCaritas",
        parent=estilos["Heading2"],
        spaceBefore=12,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Ficha del beneficiario",
            estilo_subtitulo,
        )
    )

    elementos.append(Spacer(1, 0.3 * cm))

    # -------------------------------------------------------------------------
    # Información del beneficiario
    # -------------------------------------------------------------------------

    nombre_completo = (
        f"{beneficiario.nombre} {beneficiario.apellido}"
    )

    estado = "Activo" if beneficiario.estado else "Inactivo"

    datos_beneficiario = [
        ["Cédula", beneficiario.cedula],
        ["Nombre completo", nombre_completo],
        [
            "Teléfono",
            beneficiario.telefono or "No registrado",
        ],
        [
            "Dirección",
            beneficiario.direccion or "Sin dirección registrada.",
        ],
        [
            "Fecha de registro",
            beneficiario.fecha_registro.strftime("%d/%m/%Y"),
        ],
        ["Estado", estado],
    ]

    tabla_beneficiario = Table(
        datos_beneficiario,
        colWidths=[4 * cm, 12 * cm],
    )

    tabla_beneficiario.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(tabla_beneficiario)

    # -------------------------------------------------------------------------
    # Programas asignados
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "Programas asignados",
            estilo_subtitulo,
        )
    )

    if programas_asignados:

        datos_programas = [
            [
                "Programa",
                "Fecha de asignación",
            ]
        ]

        for asignacion in programas_asignados:

            datos_programas.append(
                [
                    asignacion.programa.nombre,
                    asignacion.fecha_asignacion.strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                ]
            )

        tabla_programas = Table(
            datos_programas,
            colWidths=[10 * cm, 6 * cm],
        )

        tabla_programas.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        elementos.append(tabla_programas)

    else:

        elementos.append(
            Paragraph(
                "Este beneficiario no tiene programas asignados actualmente.",
                estilo_normal,
            )
        )

    # -------------------------------------------------------------------------
    # Código QR
    # -------------------------------------------------------------------------

    elementos.append(Spacer(1, 0.8 * cm))

    elementos.append(
        Paragraph(
            "Consultar ficha digital",
            estilo_subtitulo,
        )
    )

    qr = generar_qr_beneficiario(beneficiario)

    qr_buffer = BytesIO()

    qr.save(
        qr_buffer,
        format="PNG",
    )

    qr_buffer.seek(0)

    imagen_qr = Image(
        qr_buffer,
        width=4 * cm,
        height=4 * cm,
    )

    tabla_qr = Table(
        [
            [imagen_qr],
            [
                Paragraph(
                    "Escanee el código QR para consultar "
                    "la ficha del beneficiario.",
                    estilo_normal,
                )
            ],
        ],
        colWidths=[8 * cm],
    )

    tabla_qr.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elementos.append(tabla_qr)

    # -------------------------------------------------------------------------
    # Construcción del documento
    # -------------------------------------------------------------------------

    documento.build(elementos)

    buffer.seek(0)

    return buffer


def generar_pdf_beneficiarios(beneficiarios):
    """
    Genera un PDF con el listado de beneficiarios.

    Incluye:
    - Fecha de generación.
    - Cédula.
    - Nombre completo.
    - Teléfono.
    - Estado.
    - Total de beneficiarios.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloListadoBeneficiarios",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloListadoBeneficiarios",
        parent=estilos["Heading2"],
        spaceBefore=8,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Listado de beneficiarios",
            estilo_subtitulo,
        )
    )

    elementos.append(
        Paragraph(
            f"Fecha de generación: "
            f"{timezone.localtime().strftime('%d/%m/%Y %H:%M')}",
            estilo_normal,
        )
    )

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    # -------------------------------------------------------------------------
    # Tabla de beneficiarios
    # -------------------------------------------------------------------------

    datos = [
        [
            "Cédula",
            "Nombre completo",
            "Teléfono",
            "Estado",
        ]
    ]

    for beneficiario in beneficiarios:

        nombre_completo = (
            f"{beneficiario.nombre} "
            f"{beneficiario.apellido}"
        )

        estado = (
            "Activo"
            if beneficiario.estado
            else "Inactivo"
        )

        datos.append(
            [
                beneficiario.cedula,
                nombre_completo,
                beneficiario.telefono or "No registrado",
                estado,
            ]
        )

    tabla = Table(
        datos,
        colWidths=[
            3 * cm,
            6 * cm,
            4 * cm,
            3 * cm,
        ],
        repeatRows=1,
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elementos.append(tabla)

    # -------------------------------------------------------------------------
    # Total
    # -------------------------------------------------------------------------

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    elementos.append(
        Paragraph(
            f"Total de beneficiarios: {len(beneficiarios)}",
            estilo_normal,
        )
    )

    # -------------------------------------------------------------------------
    # Construcción del documento
    # -------------------------------------------------------------------------

    documento.build(
        elementos
    )

    buffer.seek(0)

    return buffer


def generar_pdf_programa(programa, usuarios_asignados):
    """
    Genera el PDF con la información de un programa.

    Incluye:
    - Datos generales del programa.
    - Responsable.
    - Fechas.
    - Estado.
    - Descripción.
    - Usuarios asignados.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloPrograma",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloPrograma",
        parent=estilos["Heading2"],
        spaceBefore=12,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Ficha del programa",
            estilo_subtitulo,
        )
    )

    elementos.append(
        Spacer(
            1,
            0.3 * cm,
        )
    )

    # -------------------------------------------------------------------------
    # Información del programa
    # -------------------------------------------------------------------------

    responsable = (
        programa.usuario_responsable.get_full_name()
        or programa.usuario_responsable.username
    )

    estado = (
        "Activo"
        if programa.estado
        else "Inactivo"
    )

    fecha_fin = (
        programa.fecha_fin.strftime("%d/%m/%Y")
        if programa.fecha_fin
        else "No definida"
    )

    datos_programa = [
        ["Nombre", programa.nombre],
        ["Responsable", responsable],
        [
            "Fecha de inicio",
            programa.fecha_inicio.strftime("%d/%m/%Y"),
        ],
        ["Fecha de finalización", fecha_fin],
        ["Estado", estado],
        [
            "Descripción",
            programa.descripcion
            or "Sin descripción registrada.",
        ],
    ]

    tabla_programa = Table(
        datos_programa,
        colWidths=[
            5 * cm,
            11 * cm,
        ],
    )

    tabla_programa.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(tabla_programa)

    # -------------------------------------------------------------------------
    # Usuarios asignados
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "Usuarios asignados",
            estilo_subtitulo,
        )
    )

    if usuarios_asignados:

        datos_usuarios = [
            [
                "Usuario",
                "Rol en el programa",
                "Fecha de asignación",
            ]
        ]

        for asignacion in usuarios_asignados:

            usuario = (
                asignacion.usuario.get_full_name()
                or asignacion.usuario.username
            )

            datos_usuarios.append(
                [
                    usuario,
                    asignacion.rol_en_programa,
                    asignacion.fecha_asignacion.strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                ]
            )

        tabla_usuarios = Table(
            datos_usuarios,
            colWidths=[
                6 * cm,
                5 * cm,
                5 * cm,
            ],
            repeatRows=1,
        )

        tabla_usuarios.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        elementos.append(tabla_usuarios)

    else:

        elementos.append(
            Paragraph(
                "No existen usuarios asignados a este programa.",
                estilo_normal,
            )
        )

    # -------------------------------------------------------------------------
    # Construcción del documento
    # -------------------------------------------------------------------------

    documento.build(elementos)

    buffer.seek(0)

    return buffer


def generar_pdf_programas(programas):
    """
    Genera un PDF con el listado de programas.

    Incluye:
    - Fecha de generación.
    - Nombre.
    - Responsable.
    - Fecha de inicio.
    - Fecha de finalización.
    - Estado.
    - Total de programas.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloListadoProgramas",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloListadoProgramas",
        parent=estilos["Heading2"],
        spaceBefore=8,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Listado de programas",
            estilo_subtitulo,
        )
    )

    elementos.append(
        Paragraph(
            f"Fecha de generación: "
            f"{timezone.localtime().strftime('%d/%m/%Y %H:%M')}",
            estilo_normal,
        )
    )

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    # -------------------------------------------------------------------------
    # Tabla
    # -------------------------------------------------------------------------

    datos = [
        [
            "Programa",
            "Responsable",
            "Inicio",
            "Finalización",
            "Estado",
        ]
    ]

    for programa in programas:

        responsable = (
            programa.usuario_responsable.get_full_name()
            or programa.usuario_responsable.username
        )

        fecha_fin = (
            programa.fecha_fin.strftime("%d/%m/%Y")
            if programa.fecha_fin
            else "No definida"
        )

        estado = (
            "Activo"
            if programa.estado
            else "Inactivo"
        )

        datos.append(
            [
                programa.nombre,
                responsable,
                programa.fecha_inicio.strftime("%d/%m/%Y"),
                fecha_fin,
                estado,
            ]
        )

    tabla = Table(
        datos,
        colWidths=[
            4 * cm,
            4 * cm,
            3 * cm,
            3 * cm,
            2 * cm,
        ],
        repeatRows=1,
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elementos.append(tabla)

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    elementos.append(
        Paragraph(
            f"Total de programas: {len(datos) - 1}",
            estilo_normal,
        )
    )

    documento.build(elementos)

    buffer.seek(0)

    return buffer


def generar_pdf_actividades(actividades):
    """
    Genera un PDF con el listado de actividades.

    Incluye:
    - Fecha de generación.
    - Nombre de la actividad.
    - Programa asociado.
    - Fecha y hora de la actividad.
    - Usuario creador.
    - Estado.
    - Total de actividades.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloListadoActividades",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloListadoActividades",
        parent=estilos["Heading2"],
        spaceBefore=8,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Listado de actividades",
            estilo_subtitulo,
        )
    )

    elementos.append(
        Paragraph(
            f"Fecha de generación: "
            f"{timezone.localtime().strftime('%d/%m/%Y %H:%M')}",
            estilo_normal,
        )
    )

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    # -------------------------------------------------------------------------
    # Tabla de actividades
    # -------------------------------------------------------------------------

    datos = [
        [
            "Actividad",
            "Programa",
            "Fecha y hora",
            "Usuario creador",
            "Estado",
        ]
    ]

    for actividad in actividades:

        usuario_creador = (
            actividad.usuario_creador.get_full_name()
            or actividad.usuario_creador.username
        )

        estado = (
            "Activo"
            if actividad.estado
            else "Inactivo"
        )

        datos.append(
            [
                actividad.nombre,
                actividad.programa.nombre,
                actividad.fecha_actividad.strftime(
                    "%d/%m/%Y %H:%M"
                ),
                usuario_creador,
                estado,
            ]
        )

    tabla = Table(
        datos,
        colWidths=[
            4 * cm,
            4 * cm,
            3.5 * cm,
            3 * cm,
            1.5 * cm,
        ],
        repeatRows=1,
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elementos.append(tabla)

    # -------------------------------------------------------------------------
    # Total
    # -------------------------------------------------------------------------

    elementos.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    elementos.append(
        Paragraph(
            f"Total de actividades: {len(actividades)}",
            estilo_normal,
        )
    )

    # -------------------------------------------------------------------------
    # Construcción del documento
    # -------------------------------------------------------------------------

    documento.build(
        elementos
    )

    buffer.seek(0)

    return buffer


def generar_pdf_actividad(actividad, usuarios_asignados, consumos):
    """
    Genera el PDF con la información de una actividad.

    Incluye:
    - Datos generales de la actividad.
    - Programa asociado.
    - Usuario creador.
    - Fecha y hora.
    - Estado.
    - Descripción.
    - Usuarios asignados.
    - Insumos utilizados.
    """

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloActividad",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloActividad",
        parent=estilos["Heading2"],
        spaceBefore=12,
        spaceAfter=8,
    )

    estilo_normal = estilos["BodyText"]

    elementos = []

    # -------------------------------------------------------------------------
    # Encabezado
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "CARITAS",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Ficha de la actividad",
            estilo_subtitulo,
        )
    )

    elementos.append(
        Spacer(
            1,
            0.3 * cm,
        )
    )

    # -------------------------------------------------------------------------
    # Información de la actividad
    # -------------------------------------------------------------------------

    creador = (
        actividad.usuario_creador.get_full_name()
        or actividad.usuario_creador.username
    )

    estado = (
        "Activo"
        if actividad.estado
        else "Inactivo"
    )

    estado_programa = (
        "Activo"
        if actividad.programa.estado
        else "Inactivo"
    )

    datos_actividad = [
        [
            "Nombre",
            actividad.nombre,
        ],
        [
            "Programa",
            actividad.programa.nombre,
        ],
        [
            "Fecha y hora",
            actividad.fecha_actividad.strftime(
                "%d/%m/%Y %H:%M"
            ),
        ],
        [
            "Registrada por",
            creador,
        ],
        [
            "Estado",
            estado,
        ],
        [
            "Estado del programa",
            estado_programa,
        ],
        [
            "Descripción",
            actividad.descripcion
            or "Sin descripción registrada.",
        ],
    ]

    tabla_actividad = Table(
        datos_actividad,
        colWidths=[
            5 * cm,
            11 * cm,
        ],
    )

    tabla_actividad.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(
        tabla_actividad
    )

    # -------------------------------------------------------------------------
    # Usuarios asignados
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "Usuarios asignados",
            estilo_subtitulo,
        )
    )

    if usuarios_asignados:

        datos_usuarios = [
            [
                "Usuario",
                "Rol en la actividad",
                "Fecha de asignación",
            ]
        ]

        for asignacion in usuarios_asignados:

            usuario = (
                asignacion.usuario.get_full_name()
                or asignacion.usuario.username
            )

            datos_usuarios.append(
                [
                    usuario,
                    asignacion.rol_en_actividad,
                    asignacion.fecha_asignacion.strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                ]
            )

        tabla_usuarios = Table(
            datos_usuarios,
            colWidths=[
                6 * cm,
                5 * cm,
                5 * cm,
            ],
            repeatRows=1,
        )

        tabla_usuarios.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        elementos.append(
            tabla_usuarios
        )

    else:

        elementos.append(
            Paragraph(
                "No hay usuarios asignados a esta actividad.",
                estilo_normal,
            )
        )

    # -------------------------------------------------------------------------
    # Insumos utilizados
    # -------------------------------------------------------------------------

    elementos.append(
        Paragraph(
            "Insumos utilizados",
            estilo_subtitulo,
        )
    )

    if consumos:

        datos_consumos = [
            [
                "Insumo",
                "Cantidad utilizada",
                "Unidad de medida",
            ]
        ]

        for consumo in consumos:

            datos_consumos.append(
                [
                    consumo.insumo.nombre,
                    f"{consumo.cantidad_usada:.2f}",
                    consumo.insumo.get_unidad_medida_display(),
                ]
            )

        tabla_consumos = Table(
            datos_consumos,
            colWidths=[
                7 * cm,
                4 * cm,
                5 * cm,
            ],
            repeatRows=1,
        )

        tabla_consumos.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        elementos.append(
            tabla_consumos
        )

    else:

        elementos.append(
            Paragraph(
                "No se han registrado insumos utilizados "
                "en esta actividad.",
                estilo_normal,
            )
        )

    # -------------------------------------------------------------------------
    # Construcción del documento
    # -------------------------------------------------------------------------

    documento.build(
        elementos
    )

    buffer.seek(0)

    return buffer