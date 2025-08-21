from django.contrib import admin

admin.site.site_header = "☕ Coffee Trace — Do grão à xícara: confiança em cada etapa"
admin.site.site_title  = "Coffee Trace"
admin.site.index_title = "Transparência e rastreabilidade em cada etapa da produção"

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rastreabilidade import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("lote/<int:pk>/", views.detalhe_cafe, name="lote_detalhe"),
]

# Somente MEDIA em dev (NÃO adicione static() para STATIC_URL)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


