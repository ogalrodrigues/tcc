import base64
from io import BytesIO

import qrcode
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import LoteCafe


def build_public_url(path: str, request=None) -> str:
    """
    Monta uma URL absoluta para uso no QR Code.
    - Em produção, usa settings.PUBLIC_BASE_URL (ex.: https://seu-servico.onrender.com).
    - Em desenvolvimento, usa request.build_absolute_uri.
    """
    base = getattr(settings, "PUBLIC_BASE_URL", "").rstrip("/")
    if base:
        return f"{base}{path}"
    if request is not None:
        return request.build_absolute_uri(path)
    return path


def _qrcode_png_base64(data: str) -> str:
    """
    Gera um QR Code (PNG) em memória e retorna como base64
    para uso em <img src="data:image/png;base64,..."> no template.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # mais tolerante
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def home(request):
    """
    Página inicial: mostra o último lote e o QR Code que aponta para
    a página de detalhes desse lote.
    """
    ultimo = LoteCafe.objects.order_by("-id").first()
    if not ultimo:
        return render(request, "home.html", {"mensagem": "Nenhum lote cadastrado ainda."})

    # >>> nome da rota padronizado: 'lote_detalhe'
    path = reverse("lote_detalhe", args=[ultimo.pk])

    url_publica = build_public_url(path, request)
    qr_code_b64 = _qrcode_png_base64(url_publica)

    contexto = {
        "ultimo": ultimo,
        "qr_code_b64": qr_code_b64,
        "url_publica": url_publica,
    }
    return render(request, "home.html", contexto)


def lote_detalhe(request, pk: int):
    """
    Página de detalhes de um lote específico.
    """
    lote = get_object_or_404(LoteCafe, pk=pk)
    return render(request, "lote_detalhe.html", {"lote": lote})
