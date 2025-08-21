from django.contrib import admin
from django.utils.html import format_html
from .models import LoteCafe

@admin.register(LoteCafe)
class LoteCafeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome_produtor',
        'nome_chacara',
        'tipo_grao',
        'tipo_processamento',
        'data_plantio',
        'data_colheita',
        'data_torrefacao',
        'data_validade',
        'qr_code_thumb',   # miniatura do QR (ok manter)
    )

    list_filter = (
        'tipo_grao',
        'tipo_processamento',
        'data_plantio',
        'data_colheita',
        'data_torrefacao',
        'data_validade',
    )

    search_fields = ('nome_produtor', 'nome_chacara', 'observacoes')
    date_hierarchy = 'data_colheita'

    @admin.display(description="QR")
    def qr_code_thumb(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" style="height:50px;border:1px solid #ddd;padding:2px;border-radius:4px;">',
                obj.qr_code.url
            )
        return "—"
