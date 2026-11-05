from django.contrib import admin
from .models import Categoria, Produto, Movimentacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'quantidade_minima', 'precisa_reposicao')
    search_fields = ('nome',)
    list_filter = ('categoria',)

    def precisa_reposicao(self, obj):
        return obj.quantidade < obj.quantidade_minima
    precisa_reposicao.boolean = True
    precisa_reposicao.short_description = 'Precisa de Reposição'

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'usuario', 'data_hora')
    list_filter = ('tipo', 'data_hora')
