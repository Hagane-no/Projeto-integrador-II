from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('produtos/', views.gerenciar_produtos, name='produtos'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('movimentacoes/', views.registrar_movimentacao, name='movimentacoes'),
    path('historico/', views.historico_movimentacoes, name='historico'),
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/aprovar/<int:user_id>/', views.aprovar_usuario, name='aprovar_usuario'),
]
