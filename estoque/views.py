from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Produto, Movimentacao

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'estoque/login.html')

@login_required(login_url='/login/')
def dashboard_view(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render(request, 'estoque/dashboard.html', context)

@login_required(login_url='/login/')
def historico_pedidos_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')
    
    # Filtros simples por tipo ou status se aplicável
    tipo_filtro = request.GET.get('tipo')
    if tipo_filtro:
        movimentacoes = movimentacoes.filter(tipo=tipo_filtro)

    context = {
        'movimentacoes': movimentacoes,
    }
    return render(request, 'estoque/historico.html', context)

@login_required(login_url='/login/')
def projecao_estoque_view(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render(request, 'estoque/projecao.html', context)
