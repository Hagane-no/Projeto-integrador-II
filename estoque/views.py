from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Produto, Categoria, Movimentacao
from .forms import MovimentacaoForm, ProdutoForm, CategoriaForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        usuario_input = request.POST.get('username')
        senha_input = request.POST.get('password')
        user = authenticate(request, username=usuario_input, password=senha_input)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Utilizador ou palavra-passe incorretos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.usuario = request.user
            movimentacao.save()
            messages.success(request, f'Movimentação de {movimentacao.get_tipo_display()} registrada com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao registrar movimentação. Verifique os dados inseridos.')
    else:
        form = MovimentacaoForm()

    produtos = Produto.objects.all().select_related('categoria')
    total_produtos = produtos.count()
    total_categorias = Categoria.objects.count()
    produtos_alerta = [p for p in produtos if p.precisa_reposicao]
    qtd_alerta = len(produtos_alerta)
    qtd_ok = total_produtos - qtd_alerta

    context = {
        'produtos': produtos,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'produtos_alerta': produtos_alerta,
        'qtd_alerta': qtd_alerta,
        'qtd_ok': qtd_ok,
        'form': form,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def reposicao_estoque(request):
    todos_produtos = Produto.objects.all().select_related('categoria')
    produtos_criticos = [p for p in todos_produtos if p.precisa_reposicao]

    context = {
        'produtos_criticos': produtos_criticos,
        'total_criticos': len(produtos_criticos),
    }
    return render(request, 'reposicao.html', context)


@login_required(login_url='login')
def historico(request):
    movimentacoes = Movimentacao.objects.all().select_related('produto').order_by('-data')
    context = {
        'movimentacoes': movimentacoes,
    }
    return render(request, 'historico.html', context)


# --- GESTÃO DE PRODUTOS ---

@login_required(login_url='login')
def gerenciar_produtos(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('gerenciar_produtos')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os campos.')
    else:
        form = ProdutoForm()

    produtos = Produto.objects.all().select_related('categoria')
    context = {
        'produtos': produtos,
        'form': form,
    }
    return render(request, 'produtos.html', context)


@login_required(login_url='login')
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('gerenciar_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})


@login_required(login_url='login')
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido com sucesso!')
        return redirect('gerenciar_produtos')
    return render(request, 'confirmar_delecao.html', {'objeto': produto, 'tipo': 'Produto'})


# --- GESTÃO DE CATEGORIAS ---

@login_required(login_url='login')
def gerenciar_categorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('gerenciar_categorias')
        else:
            messages.error(request, 'Erro ao cadastrar categoria. Verifique os campos.')
    else:
        form = CategoriaForm()

    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias,
        'form': form,
    }
    return render(request, 'categorias.html', context)


@login_required(login_url='login')
def deletar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso!')
        return redirect('gerenciar_categorias')
    return render(request, 'confirmar_delecao.html', {'objeto': categoria, 'tipo': 'Categoria'})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Produto

@login_required
def api_produtos(request):
    """
    API JSON que retorna a lista de produtos, quantidades e status de estoque.
    """
    produtos = Produto.objects.all().select_related('categoria')
    data = []
    
    for prod in produtos:
        data.append({
            'id': prod.id,
            'nome': prod.nome,
            'categoria': prod.categoria.nome if prod.categoria else 'Sem Categoria',
            'quantidade_atual': prod.quantidade_atual,
            'quantidade_minima': prod.quantidade_minima,
            'unidade_medida': prod.unidade_medida,
            'precisa_reposicao': prod.quantidade_atual < prod.quantidade_minima
        })
        
    return JsonResponse({'status': 'sucesso', 'total': len(data), 'produtos': data}, json_dumps_params={'ensure_ascii': False})
