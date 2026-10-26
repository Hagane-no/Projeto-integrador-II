
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Administração do Django
    path('admin/', admin.site.urls),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Páginas principais
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('categorias/', views.categorias_view, name='categorias'),
    path(
        'categorias/criar/',
        views.criar_categoria,
        name='criar_categoria'
    ),

    # Estoque
    path(
        'movimentacoes/',
        views.movimentacoes_view,
        name='movimentacoes'
    ),
    path('historico/', views.historico_view, name='historico'),

    # Usuários
    path(
        'usuarios/',
        views.gerenciar_usuarios_view,
        name='gerenciar_usuarios'
    ),
    path(
        'usuarios/aprovar/<int:user_id>/',
        views.aprovar_usuario_view,
        name='aprovar_usuario'
    ),
]
