from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Categoria
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

def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, "loja/produto_detalhe.html", {"produto": produto})

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
