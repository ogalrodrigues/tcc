import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from .models import LoteCafe

def home(request):
    ultimo = LoteCafe.objects.order_by("-id").first()
    if not ultimo:
        return render(request, "home.html", {"mensagem": "Nenhum lote cadastrado ainda."})

    # URL absoluta do último lote
    url = request.build_absolute_uri(f"/lote/{ultimo.pk}/")

    # Gerar QR Code em memória
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, "home.html", {
        "ultimo": ultimo,
        "qr_code": qr_code_base64,
    })

def detalhe_cafe(request, pk):
    lote = get_object_or_404(LoteCafe, pk=pk)
    return render(request, "detalhe.html", {"lote": lote})
