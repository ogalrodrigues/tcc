from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class LoteCafe(models.Model):
    nome_produtor = models.CharField(max_length=100)
    nome_chacara = models.CharField(max_length=100)
    tipo_grao = models.CharField(max_length=50)
    tipo_processamento = models.CharField(max_length=50)

    data_plantio = models.DateField()
    data_colheita = models.DateField()
    data_lavagem = models.DateField()
    data_secagem = models.DateField()
    data_pilagem = models.DateField()
    data_torrefacao = models.DateField()
    data_embalagem = models.DateField()
    data_validade = models.DateField()

    observacoes = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='lotes/', blank=True, null=True)

    # QR Code salvo em arquivo
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # salva primeiro para garantir que exista self.pk
        super().save(*args, **kwargs)

        # gera QR apenas se ainda não existir
        if not self.qr_code:
            url = f"http://127.0.0.1:8000/lote/{self.pk}/"
            img = qrcode.make(url)
            buf = BytesIO()
            img.save(buf, format='PNG')
            filename = f"qr_{self.pk}.png"
            self.qr_code.save(filename, File(buf), save=False)

            # atualiza só o campo qr_code para evitar loop
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return f"{self.nome_produtor} — {self.nome_chacara}"

