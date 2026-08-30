import base64
from io import BytesIO

import qrcode

from django import template


register = template.Library()


@register.simple_tag
def generar_qr(texto):
    """
    Genera un código QR a partir de un texto o URL
    y devuelve una imagen en formato Base64.
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(texto)

    qr.make(fit=True)

    imagen = qr.make_image()

    buffer = BytesIO()

    imagen.save(
        buffer,
        format="PNG",
    )

    imagen_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return f"data:image/png;base64,{imagen_base64}"