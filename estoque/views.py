from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
    
    produtos_criticos = [p for p in produtos if p.precisa_reposicao]
    reposicao_necessaria = len(produtos_criticos)
    stock_em_dia = total_produtos - reposicao_necessaria

    context = {
        'produtos': produtos,
        'produtos_criticos': produtos_criticos,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'reposicao_necessaria': reposicao_necessaria,
        'stock_em_dia': stock_em_dia,
        'form': form,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def reposicao_estoque(request):
    produtos = Produto.objects.all().select_related('categoria')
    
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        qtd = request.POST.get('quantidade')
        if produto_id and qtd:
            prod = get_object_or_404(Produto, id=produto_id)
            Movimentacao.objects.create(
                produto=prod,
                tipo='ENTRADA',
                quantidade=int(qtd),
                usuario=request.user
            )
            messages.success(request, 'Reposição efetuada com sucesso!')
            return redirect('reposicao')  # Redirecionamento correto conforme urls.py

    context = {
        'produtos': produtos,
    }
    return render(request, 'reposicao.html', context)


@login_required(login_url='login')
def historico(request):
    movimentacoes = Movimentacao.objects.all().select_related('produto', 'usuario').order_by('-data')
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
    categorias = Categoria.objects.all()
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
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


@login_required
def api_produtos(request):
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
            'precisa_reposicao': prod.precisa_reposicao
        })
        
    return JsonResponse({'status': 'sucesso', 'total': len(data), 'produtos': data}, json_dumps_params={'ensure_ascii': False})
