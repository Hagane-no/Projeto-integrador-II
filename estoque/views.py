@login_required
def movimentacoes_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data_hora')
    return render(request, 'estoque/movimentacoes.html', {'movimentacoes': movimentacoes})

@login_required
def historico_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data_hora')
    return render(request, 'estoque/historico.html', {'movimentacoes': movimentacoes})
