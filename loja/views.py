from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# ATUALIZAÇÃO 1: Importamos os novos modelos Avaliacao e ListaDesejo
from .models import Produto, Categoria, Avaliacao, ListaDesejo
from .forms import ProdutoForm

# --- INSTITUCIONAL ---
def home(request):
    produtos_do_banco = Produto.objects.filter(ativo=True)[:6]
    categorias_principais = Categoria.objects.filter(pai__isnull=True)
    
    contexto = {
        "titulo": "Bem-vindo à TACNS Games",
        "subtitulo": "A sua loja de jogos online!",
        "categorias_principais": categorias_principais,
        "produtos": produtos_do_banco
    }
    return render(request, "loja/index.html", contexto)

def sobre(request):
    return render(request, "loja/sobre.html", {"titulo": "Sobre Nós"})

def contato(request):
    return render(request, "loja/contato.html", {"titulo": "Contato"})


# --- CATÁLOGO & PRODUTOS ---
def produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    categorias_principais = Categoria.objects.filter(pai__isnull=True)
    
    # 1. Captura a palavra digitada na barra (name="busca" no HTML)
    termo_busca = request.GET.get('busca')
    
    # 2. Se existir uma busca, filtra os jogos que contêm esse texto no nome (icontains ignora maiúsculas/minúsculas)
    if termo_busca:
        produtos = produtos.filter(nome__icontains=termo_busca)
        titulo_pagina = f"Resultados para: '{termo_busca}'"
    else:
        titulo_pagina = "Produtos"
        
    contexto = {
        "titulo": titulo_pagina,
        "subtitulo": "Todos os produtos da loja" if not termo_busca else "Jogos encontrados",
        "produtos": produtos,
        "categorias_principais": categorias_principais,
    }
    return render(request, "loja/produtos.html", contexto)

# Adicione esta função auxiliar para ler a árvore de categorias
def obter_todas_categorias(categoria):
    categorias = [categoria]
    for sub in categoria.subcategorias.all():
        categorias.extend(obter_todas_categorias(sub))
    return categorias

# Atualize a sua view existente
def produtos_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, id=id)
        
    # 2. O comando "__in" diz ao Django para procurar em toda a lista
    todas_categorias = obter_todas_categorias(categoria_obj)
    
    # CORREÇÃO: Adicionado o ativo=True aqui!
    produtos = Produto.objects.filter(categoria__in=todas_categorias, ativo=True)
    
    categorias_principais = Categoria.objects.filter(pai__isnull=True)
    
    contexto = {
        "titulo": f"Categoria: {categoria_obj.nome}",
        "subtitulo": f"Produtos em {categoria_obj.nome}",
        "produtos": produtos,
        "categorias_principais": categorias_principais,
    }
    return render(request, "loja/produtos.html", contexto)

#  A view de detalhe agora envia as avaliações e checa a Wishlist
def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    # Busca todas as avaliações deste produto específico
    avaliacoes = produto.avaliacoes.all()
    na_wishlist = False
    
    # Só verifica se está na wishlist se o cliente tiver feito login (evita erros com usuários anónimos)
    if request.user.is_authenticated:
        na_wishlist = ListaDesejo.objects.filter(usuario=request.user, produto=produto).exists()
        
    contexto = {
        "produto": produto,
        "avaliacoes": avaliacoes,    # Enviamos as avaliações para o HTML
        "na_wishlist": na_wishlist   # Enviamos um Booleano (True/False) para pintar o coração de vermelho ou não
    }
    return render(request, "loja/produto_detalhe.html", contexto)

def produtos_esgotados(request):
    produtos = Produto.objects.filter(estoque=0)
    return render(request, "loja/produtos.html", {"produtos": produtos, "titulo": "Produtos Esgotados"})


# --- OPERAÇÕES CRUD ---
@login_required
def produto_novo(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect("loja:produtos")
    else:
        form = ProdutoForm()
    return render(request, "loja/produto_form.html", {"form": form, "titulo": "Novo Produto"})

@login_required
def produto_editar(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("loja:produto_detalhe", id=produto.id)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "loja/produto_form.html", {"form": form, "titulo": "Editar produto"})

@login_required
def produto_excluir(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect("loja:produtos")
    return render(request, "loja/produto_confirmar_exclusao.html", {"produto": produto})


# ==========================================
# NOVAS VIEWS: WISHLIST E AVALIAÇÕES
# ==========================================

@login_required
def toggle_wishlist(request, produto_id):
    """
    Função 'Toggle' (Alternar): Se o produto não estiver na wishlist, adiciona.
    Se já estiver, remove. Funciona como um interruptor liga/desliga.
    """
    produto = get_object_or_404(Produto, id=produto_id)
    
    # get_or_create tenta encontrar o registo. Se não encontrar, cria-o.
    # Retorna o objeto (item) e um Booleano (created) que diz se foi acabado de criar.
    item, created = ListaDesejo.objects.get_or_create(usuario=request.user, produto=produto)
    
    if not created:
        # Se NÃO foi criado (já existia), então o cliente quer remover o coração.
        item.delete()
        messages.info(request, f"{produto.nome} removido da lista de desejos.")
    else:
        # Se FOI criado, avisa que deu sucesso.
        messages.success(request, f"{produto.nome} guardado na lista de desejos!")
        
    # Redireciona de volta para a EXATA página onde o cliente clicou (seja a vitrine ou o detalhe)
    return redirect(request.META.get('HTTP_REFERER', 'loja:produtos'))

@login_required
def wishlist(request):
    """ Exibe todos os itens guardados pelo utilizador logado. """
    # select_related otimiza a busca na base de dados (traz a wishlist e o produto na mesma query)
    itens = ListaDesejo.objects.filter(usuario=request.user).select_related('produto')
    return render(request, 'loja/wishlist.html', {'itens': itens, 'titulo': 'Minha Lista de Desejos'})

@login_required
def adicionar_avaliacao(request, produto_id):
    """ Recebe o POST do formulário de estrelas na página de detalhes. """
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        # Captura os dados do formulário HTML
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario')
        
        if nota:
            # Cria a avaliação no banco ligando ao produto e ao cliente
            Avaliacao.objects.create(
                produto=produto,
                usuario=request.user,
                nota=int(nota),
                comentario=comentario
            )
            messages.success(request, "Obrigado! A sua avaliação foi publicada.")
            
    # Redireciona de volta para ver a avaliação recém-criada
    return redirect('loja:produto_detalhe', id=produto.id)