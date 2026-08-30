from io import BytesIO

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