# rastreabilidade/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("lote/<uuid:public_id>/", views.lote_detalhe, name="lote_detalhe"),
]
