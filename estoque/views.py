
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Produto, Categoria, Movimentacao


# Verifica se o usuário é administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff


# --------------------------------------------------
# LOGIN, LOGOUT E CADASTRO
# --------------------------------------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')

        if user is not None:
            messages.error(
                request,
                'Sua conta ainda não foi aprovada pelo administrador.'
            )
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username or not password:
            messages.error(
                request,
                'Preencha o nome de usuário e a senha.'
            )
            return render(request, 'register.html')

        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Este nome de usuário já está cadastrado.'
            )
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )

        messages.success(
            request,
            'Cadastro solicitado! Aguarde a aprovação do administrador.'
        )
        return redirect('login')

    return render(request, 'register.html')


# --------------------------------------------------
# GERENCIAMENTO DE USUÁRIOS
# --------------------------------------------------

@login_required
@user_passes_test(is_admin)
def gerenciar_usuarios_view(request):
    usuarios_pendentes = User.objects.filter(
        is_active=False
    ).order_by('date_joined')

    todos_usuarios = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'gerenciar_usuarios.html',
        {
            'usuarios_pendentes': usuarios_pendentes,
            'todos_usuarios': todos_usuarios,
        }
    )


@login_required
@user_passes_test(is_admin)
def aprovar_usuario_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        usuario.is_active = True
        usuario.save(update_fields=['is_active'])
        messages.success(
            request,
            f'O usuário "{usuario.username}" foi aprovado.'
        )

    return redirect('gerenciar_usuarios')


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@login_required
def dashboard_view(request):
    produtos = Produto.objects.select_related('categoria').all()

    total_produtos = produtos.count()

    produtos_criticos = [
        produto for produto in produtos
        if produto.quantidade <= produto.quantidade_minima
    ]

    quantidade_criticos = len(produtos_criticos)
    quantidade_em_dia = total_produtos - quantidade_criticos

    context = {
        'total_produtos': total_produtos,
        'quantidade_criticos': quantidade_criticos,
        'quantidade_em_dia': quantidade_em_dia,
        'produtos_criticos': produtos_criticos,
    }

    return render(request, 'dashboard.html', context)


# --------------------------------------------------
# PRODUTOS
# --------------------------------------------------

@login_required
def produtos_view(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            messages.error(
                request,
                'Somente administradores podem cadastrar produtos.'
            )
            return redirect('produtos')

        nome = request.POST.get('nome', '').strip()
        categoria_id = request.POST.get('categoria', '').strip()
        quantidade_texto = request.POST.get('quantidade', '0').strip()
        minimo_texto = request.POST.get('quantidade_minima', '0').strip()
        preco_texto = request.POST.get('preco', '0').strip()

        if not nome:
            messages.error(request, 'Informe o nome do produto.')
            return redirect('produtos')

        categoria = get_object_or_404(
            Categoria,
            id=categoria_id
        )

        try:
            quantidade = int(quantidade_texto)
            quantidade_minima = int(minimo_texto)
            preco = Decimal(preco_texto.replace(',', '.'))
        except (ValueError, InvalidOperation):
            messages.error(
                request,
                'Informe quantidades inteiras e um preço válido.'
            )
            return redirect('produtos')

        if quantidade < 0 or quantidade_minima < 0:
            messages.error(
                request,
                'As quantidades não podem ser negativas.'
            )
            return redirect('produtos')

        if not preco.is_finite() or preco < 0:
            messages.error(
                request,
                'O preço deve ser um valor válido e não negativo.'
            )
            return redirect('produtos')

        if preco.as_tuple().exponent < -2:
            messages.error(
                request,
                'O preço deve ter no máximo duas casas decimais.'
            )
            return redirect('produtos')

        try:
            produto = Produto(
                nome=nome,
                categoria=categoria,
                quantidade=quantidade,
                quantidade_minima=quantidade_minima,
                preco=preco,
            )
            produto.full_clean()
            produto.save()
        except Exception as erro:
            from django.core.exceptions import ValidationError

            if isinstance(erro, ValidationError):
                messages.error(
                    request,
                    'Não foi possível cadastrar o produto. '
                    'Confira os dados informados.'
                )
                return redirect('produtos')
            raise

        messages.success(
            request,
            f'Produto "{produto.nome}" cadastrado com sucesso.'
        )
        return redirect('produtos')

    produtos = Produto.objects.select_related(
        'categoria'
    ).all().order_by('nome')

    categorias = Categoria.objects.all().order_by('nome')

    return render(
        request,
        'produtos.html',
        {
            'produtos': produtos,
            'categorias': categorias,
        }
    )


# --------------------------------------------------
# CATEGORIAS
# --------------------------------------------------

@login_required
def categorias_view(request):
    categorias = Categoria.objects.all().order_by('nome')

    return render(
        request,
        'categorias.html',
        {'categorias': categorias}
    )


@login_required
@user_passes_test(is_admin)
def criar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            messages.error(request, 'Informe o nome da categoria.')
        elif Categoria.objects.filter(nome__iexact=nome).exists():
            messages.error(
                request,
                'Já existe uma categoria com esse nome.'
            )
        else:
            Categoria.objects.create(nome=nome)
            messages.success(
                request,
                'Categoria cadastrada com sucesso.'
            )
            return redirect('categorias')

    categorias = Categoria.objects.all().order_by('nome')

    return render(
        request,
        'categorias.html',
        {
            'categorias': categorias,
            'mostrar_form_categoria': True,
        }
    )


# --------------------------------------------------
# ENTRADAS E SAÍDAS DO ESTOQUE
# --------------------------------------------------

@login_required
def movimentacoes_view(request):
    produtos = Produto.objects.select_related(
        'categoria'
    ).all().order_by('nome')

    if request.method == 'POST':
        produto_id = request.POST.get('produto', '').strip()
        tipo = request.POST.get('tipo', '')
        quantidade_texto = request.POST.get('quantidade', '').strip()
        observacao = request.POST.get('observacao', '').strip()

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            messages.error(
                request,
                'Informe uma quantidade inteira válida.'
            )
            return redirect('movimentacoes')

        if quantidade <= 0:
            messages.error(
                request,
                'A quantidade deve ser maior que zero.'
            )
            return redirect('movimentacoes')

        if tipo not in ('ENTRADA', 'SAIDA'):
            messages.error(
                request,
                'Selecione um tipo de movimentação válido.'
            )
            return redirect('movimentacoes')

        produto = get_object_or_404(Produto, id=produto_id)

        if tipo == 'SAIDA' and produto.quantidade < quantidade:
            messages.error(
                request,
                'Quantidade insuficiente em estoque.'
            )
            return redirect('movimentacoes')

        if tipo == 'ENTRADA':
            produto.quantidade += quantidade
        else:
            produto.quantidade -= quantidade

        produto.save(update_fields=['quantidade'])

        Movimentacao.objects.create(
            produto=produto,
            usuario=request.user,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao,
        )

        messages.success(
            request,
            'Movimentação registrada com sucesso.'
        )
        return redirect('movimentacoes')

    return render(
        request,
        'reposicao.html',
        {'produtos': produtos}
    )


# --------------------------------------------------
# HISTÓRICO DE MOVIMENTAÇÕES
# --------------------------------------------------

@login_required
def historico_view(request):
    historico = Movimentacao.objects.select_related(
        'produto',
        'usuario'
    ).all().order_by('-data_hora')

    return render(
        request,
        'historico.html',
        {
            'historico': historico,
            'movimentacoes': historico,
        }
    )


# --------------------------------------------------
# COMPATIBILIDADE COM NOMES DE ROTAS ANTIGAS
# --------------------------------------------------

lista_produtos = produtos_view
lista_categorias = categorias_view
registrar_movimentacao = movimentacoes_view
historico_movimentacoes = historico_view
gerenciar_usuarios = gerenciar_usuarios_view
aprovar_usuario = aprovar_usuario_view
