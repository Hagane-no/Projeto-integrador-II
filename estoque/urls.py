from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('historico/', views.historico_pedidos_view, name='historico'),
    path('projecao/', views.projecao_estoque_view, name='projecao'),
]
