from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("lote/<int:pk>/", views.lote_detalhe, name="lote_detalhe"),
]
