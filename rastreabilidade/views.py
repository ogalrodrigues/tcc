# rastreabilidade/views.py
import io, base64, qrcode
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .models import LoteCafe


def build_public_url(path: str, request=None) -> str:
    """
    Monta uma URL absoluta para uso no QR Code.
    - Em produção, usa settings.PUBLIC_BASE_URL.
    - Em dev, usa request.build_absolute_uri.
    """
    base = getattr(settings, "PUBLIC_BASE_URL", "").rstrip("/")
    if base:
        return f"{base}{path}"
    if request is not None:
        return request.build_absolute_uri(path)
    return path


def _qrcode_png_base64(data: str) -> str:
    """
    Gera QR em memória e retorna como base64 para <img src="data:image/png;base64,...">
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def home(request):
    """
    Página inicial: mostra o último lote e o QR inline em base64.
    """
    ultimo = LoteCafe.objects.order_by("-id").first()
    if not ultimo:
        return render(request, "home.html", {"mensagem": "Nenhum lote cadastrado ainda."})

    path = reverse("lote_detalhe", args=[ultimo.public_id])
    url_publica = build_public_url(path, request)
    qr_code_b64 = _qrcode_png_base64(url_publica)

    contexto = {
        "ultimo": ultimo,
        "qr_code_b64": qr_code_b64,
        "url_publica": url_publica,
    }
    return render(request, "home.html", contexto)


def lote_detalhe(request, public_id):
    """
    Página de detalhes de um lote específico.
    """
    lote = get_object_or_404(LoteCafe, public_id=public_id)
    return render(request, "lote_detalhe.html", {"lote": lote})


@cache_page(60 * 60 * 24 * 365)  # cache 1 ano
def qr_lote(request, public_id):
    """
    Gera o QR como image/png para cache/CDN.
    """
    lote = get_object_or_404(LoteCafe, public_id=public_id)
    base = (getattr(settings, "PUBLIC_BASE_URL", "") or "").rstrip("/")
    target = f"{base}/lote/{lote.public_id}/" if base else f"/lote/{lote.public_id}/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(target)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)

    resp = HttpResponse(buf.getvalue(), content_type="image/png")
    resp["Cache-Control"] = "public, max-age=31536000"
    return resp
