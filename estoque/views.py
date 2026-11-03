
from django.shortcuts import render
from .models import Produto, Movimentacao


def dashboard_view(request):
    produtos = Produto.objects.all()
    movimentacoes = Movimentacao.objects.all()

    contexto = {
        'produtos': produtos,
        'total_produtos': produtos.count(),
        'total_movimentacoes': movimentacoes.count(),
    }

    return render(request, 'estoque/dashboard.html', contexto)


def historico_pedidos_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')

    contexto = {
        'movimentacoes': movimentacoes,
    }

    return render(request, 'estoque/historico.html', contexto)


def projecao_estoque_view(request):
    produtos = Produto.objects.all()

    contexto = {
        'produtos': produtos,
    }

    return render(request, 'estoque/projecao.html', contexto)
  
