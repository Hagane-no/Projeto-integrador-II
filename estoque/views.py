from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Categoria, Produto, Movimentacao
from .forms import CategoriaForm

@login_required
def dashboard_view(request):
    total_produtos = Produto.objects.count()
    produtos_baixo_estoque = Produto.objects.filter(quantidade_atual__lte=models.F('quantidade_minima'))
    total_usuarios = request.user.__class__.objects.count()
    context = {
        'total_produtos': total_produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'total_usuarios': total_usuarios,
    }
    return render(request, 'estoque/dashboard.html', context)

@login_required
def produtos_view(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/produtos.html', {'produtos': produtos})

@login_required
def editar_produto_view(request, pk):
    # Lógica de edição de produto
    produto = Produto.objects.get(pk=pk)
    # ... adicione o seu formulário ou lógica existente aqui
    return render(request, 'estoque/editar_produto.html', {'produto': produto})

@login_required
def categorias_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'estoque/categorias.html', {'categorias': categorias})

@login_required
def criar_categoria_view(request):
    """View responsável por criar uma nova categoria e evitar o erro NoReverseMatch"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'estoque/criar_categoria.html', {'form': form})

@login_required
def movimentacoes_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')
    return render(request, 'estoque/movimentacoes.html', {'movimentacoes': movimentacoes})

@login_required
def historico_view(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')
    return render(request, 'estoque/historico.html', {'movimentacoes': movimentacoes})

@login_required
def reposicao_view(request):
    produtos_reposicao = Produto.objects.filter(quantidade_atual__lte=models.F('quantidade_minima'))
    return render(request, 'estoque/reposicao.html', {'produtos': produtos_reposicao})

@login_required
def gerenciar_usuarios_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    return render(request, 'estoque/gerenciar_usuarios.html')
