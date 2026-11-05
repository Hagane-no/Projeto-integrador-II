from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('produtos/editar/<int:pk>/', views.editar_produto_view, name='editar_produto'),
    path('categorias/', views.categorias_view, name='categorias'),
    path('categorias/criar/', views.criar_categoria_view, name='criar_categoria'), # <-- Essencial para corrigir o erro atual
    path('movimentacoes/', views.movimentacoes_view, name='movimentacoes'),
    path('historico/', views.historico_view, name='historico'),
    path('reposicao/', views.reposicao_view, name='reposicao'),
    path('usuarios/', views.gerenciar_usuarios_view, name='gerenciar_usuarios'),
]
