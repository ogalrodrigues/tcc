# rastreabilidade/models.py
from django.db import models
import uuid

class LoteCafe(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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
    imagem = models.ImageField(upload_to="lotes/", blank=True, null=True)

    def __str__(self):
        return f"{self.nome_produtor} — {self.nome_chacara}"
