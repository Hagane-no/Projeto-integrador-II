from django.contrib import admin
from django.urls import path
from estoque.views import (
    dashboard, reposicao_estoque, historico, login_view, logout_view,
    gerenciar_produtos, editar_produto, deletar_produto,
    gerenciar_categorias, deletar_categoria, api_produtos
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', dashboard, name='dashboard'),
    path('reposicao/', reposicao_estoque, name='reposicao'),
    path('historico/', historico, name='historico'),
    
    # Produtos
    path('produtos/', gerenciar_produtos, name='gerenciar_produtos'),
    path('produtos/editar/<int:pk>/', editar_produto, name='editar_produto'),
    path('produtos/deletar/<int:pk>/', deletar_produto, name='deletar_produto'),
    
    # Categorias
    path('categorias/', gerenciar_categorias, name='gerenciar_categorias'),
    path('categorias/deletar/<int:pk>/', deletar_categoria, name='deletar_categoria'),
    
    # API JSON
    path('api/produtos/', api_produtos, name='api_produtos'),
]