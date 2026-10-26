
from django.contrib import admin
from .models import Categoria, Produto, Movimentacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'categoria',
        'quantidade',
        'quantidade_minima',
        'precisa_reposicao',
    )
    search_fields = ('nome',)
    list_filter = ('categoria',)

    @admin.display(boolean=True, description='Precisa de Reposição')
    def precisa_reposicao(self, obj):
        return obj.quantidade <= obj.quantidade_minima


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = (
        'produto',
        'tipo',
        'quantidade',
        'usuario',
        'data_hora',
    )
    list_filter = ('tipo', 'data_hora')
    search_fields = ('produto__nome', 'usuario__username')
    date_hierarchy = 'data_hora'
