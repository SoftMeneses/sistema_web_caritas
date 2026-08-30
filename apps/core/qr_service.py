import qrcode

from django.conf import settings
from django.urls import reverse


def generar_qr_beneficiario(beneficiario):
    """
    Genera dinámicamente el código QR de un beneficiario.

    El QR contiene únicamente la URL de la ficha
    del beneficiario.
    """

    ruta = reverse(
        "core:beneficiario_detalle",
        kwargs={
            "pk": beneficiario.pk,
        },
    )

    url = f"{settings.SITE_URL}{ruta}"

    return qrcode.make(url)