from django.contrib import admin
from .models import Categoria, Produto, Movimentacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Usamos uma função customizada 'get_categoria' para garantir a exibição do nome do texto
    list_display = ('nome', 'get_categoria', 'quantidade_atual', 'quantidade_minima', 'precisa_reposicao')
    list_filter = ('categoria',)
    search_fields = ('nome',)

    @admin.display(description='Categoria')
    def get_categoria(self, obj):
        return obj.categoria.nome

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'data', 'usuario')
    list_filter = ('tipo', 'data')