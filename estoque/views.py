from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Produto, Categoria, Movimentacao

# Verifica se o usuário é Administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff

# ----------------------------------------------------
# AUTENTICAÇÃO E CADASTRO
# ----------------------------------------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Sua conta ainda não foi aprovada pelo Administrador.')
        else:
            messages.error(request, 'Utilizador ou palavra-passe incorretos.')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'As palavras-passe não coincidem.')
            return render(request, 'register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de utilizador já existe.')
            return render(request, 'register.html')
            
        # Cria o usuário INATIVO aguardando aprovação do ADM
        user = User.objects.create_user(username=username, password=password)
        user.is_active = False  
        user.save()
        
        messages.success(request, 'Conta solicitada com sucesso! Aguarde a aprovação do Administrador para fazer login.')
        return redirect('login')
        
    return render(request, 'register.html')

# ----------------------------------------------------
# PAINEL DO ADMINISTRADOR (GERENCIAR USUÁRIOS)
# ----------------------------------------------------

@login_required
@user_passes_test(is_admin)
def gerenciar_usuarios_view(request):
    usuarios_pendentes = User.objects.filter(is_active=False)
    todos_usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'gerenciar_usuarios.html', {
        'usuarios_pendentes': usuarios_pendentes,
        'todos_usuarios': todos_usuarios
    })

@login_required
@user_passes_test(is_admin)
def aprovar_usuario_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f'O utilizador "{usuario.username}" foi aprovado com sucesso!')
    return redirect('gerenciar_usuarios')

# ----------------------------------------------------
# PRINCIPAIS VISUALIZAÇÕES DO SISTEMA
# ----------------------------------------------------

@login_required
def dashboard_view(request):
    produtos = Produto.objects.all()
    total_produtos = produtos.count()
    criticos = [p for p in produtos if p.quantidade < p.quantidade_minima]
    em_dia = total_produtos - len(criticos)
    
    context = {
        'total_produtos': total_produtos,
        'quantidade_criticos': len(criticos),
        'quantidade_em_dia': em_dia,
        'produtos_criticos': criticos,
    }
    return render(request, 'dashboard.html', context)

@login_required
def produtos_view(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos, 'categorias': categorias})

@login_required
def categorias_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})

@login_required
def movimentacoes_view(request):
    produtos = Produto.objects.all()
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade', 0))
        observacao = request.POST.get('observacao', '')
        
        produto = get_object_or_404(Produto, id=produto_id)
        
        if tipo == 'SAIDA' and produto.quantidade < quantidade:
            messages.error(request, 'Quantidade insuficiente em estoque.')
        else:
            if tipo == 'ENTRADA':
                produto.quantidade += quantidade
            else:
                produto.quantidade -= quantidade
            produto.save()
            
            Movimentacao.objects.create(
                produto=produto,
                usuario=request.user,
                tipo=tipo,
                quantidade=quantidade,
                observacao=observacao
            )
            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('movimentacoes')
            
    return render(request, 'movimentacoes.html', {'produtos': produtos})

@login_required
def historico_view(request):
    historico = Movimentacao.objects.all().order_by('-data_hora')
    return render(request, 'historico.html', {'historico': historico})
