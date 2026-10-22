from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from loja.models import Produto, Variacao
from .models import Pedido, ItemPedido

def carrinho(request):
    produtos, total = obter_dados_carrinho(request)
    return render(request, "pedidos/carrinho.html", {"produtos": produtos, "total": total})

def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    variacao_id = request.POST.get('variacao_id')
    
    if produto.variacoes.exists() and not variacao_id:
        messages.warning(request, "Por favor, escolha um tamanho antes de adicionar ao carrinho.")
        return redirect('loja:produto_detalhe', id=produto.id)

    chave_carrinho = f"{produto.id}-{variacao_id}" if variacao_id else f"{produto.id}-None"
    carrinho = request.session.get("carrinho", {})

    if chave_carrinho in carrinho:
        carrinho[chave_carrinho] += 1
    else:
        carrinho[chave_carrinho] = 1

    request.session["carrinho"] = carrinho
    tamanho_msg = f" ({Variacao.objects.get(id=variacao_id).nome})" if variacao_id else ""
    messages.success(request, f"{produto.nome}{tamanho_msg} adicionado ao carrinho!")
    return redirect("pedidos:carrinho")

def somar_carrinho(request, chave):
    carrinho = request.session.get("carrinho", {})
    if chave in carrinho:
        carrinho[chave] += 1
    request.session["carrinho"] = carrinho
    return redirect("pedidos:carrinho")

def remover_carrinho(request, chave):
    carrinho = request.session.get("carrinho", {})
    if chave in carrinho:
        carrinho[chave] -= 1
        if carrinho[chave] <= 0:
            del carrinho[chave]
    request.session["carrinho"] = carrinho
    return redirect("pedidos:carrinho")

def excluir_carrinho(request, chave):
    carrinho = request.session.get("carrinho", {})
    if chave in carrinho:
        del carrinho[chave]
    request.session["carrinho"] = carrinho
    return redirect("pedidos:carrinho")

def contador_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    quantidade = sum(carrinho.values())
    return {"quantidade_carrinho": quantidade}

def obter_dados_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    produtos = []
    total = Decimal("0.00")

    for chave, quantidade in carrinho.items():
        partes = chave.split('-')
        id_produto = partes[0]
        id_variacao = partes[1] if partes[1] != 'None' else None

        produto = get_object_or_404(Produto, id=id_produto)
        variacao = Variacao.objects.filter(id=id_variacao).first() if id_variacao else None

        subtotal = produto.preco * quantidade
        total += subtotal

        produtos.append({
            "chave": chave,
            "produto": produto,
            "variacao": variacao,
            "quantidade": quantidade,
            "subtotal": subtotal,
        })

    return produtos, total

@login_required
@require_POST
def finalizar_pedido(request):
    carrinho = request.session.get("carrinho", {})

    if not carrinho:
        messages.warning(request, "O seu carrinho está vazio.")
        return redirect("pedidos:carrinho")

    try:
        with transaction.atomic():
            produtos_pedido = []
            total = Decimal("0.00")

            for chave, quantidade in carrinho.items():
                partes = chave.split('-')
                id_produto = partes[0]
                id_variacao = partes[1] if partes[1] != 'None' else None

                produto = Produto.objects.select_for_update().get(id=int(id_produto))
                variacao = None
                
                if id_variacao:
                    variacao = Variacao.objects.select_for_update().get(id=int(id_variacao))
                    if quantidade <= 0 or quantidade > variacao.estoque:
                        raise ValueError(f"Stock insuficiente para {produto.nome} (Tamanho {variacao.nome}).")
                else:
                    if quantidade <= 0 or quantidade > produto.estoque:
                        raise ValueError(f"Stock insuficiente para {produto.nome}.")

                subtotal = produto.preco * quantidade
                total += subtotal

                produtos_pedido.append({
                    "produto": produto,
                    "variacao": variacao,
                    "quantidade": quantidade,
                    "preco": produto.preco,
                })

            pedido = Pedido.objects.create(usuario=request.user, total=total)

            for item in produtos_pedido:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item["produto"],
                    variacao=item["variacao"],
                    quantidade=item["quantidade"],
                    preco_unitario=item["preco"],
                )

                if item["variacao"]:
                    item["variacao"].estoque -= item["quantidade"]
                    item["variacao"].save(update_fields=["estoque"])
                else:
                    item["produto"].estoque -= item["quantidade"]
                    item["produto"].save(update_fields=["estoque"])

    except Produto.DoesNotExist:
        messages.error(request, "Um produto do carrinho já não está disponível.")
        return redirect("pedidos:carrinho")
    except Variacao.DoesNotExist:
        messages.error(request, "O tamanho selecionado já não está disponível.")
        return redirect("pedidos:carrinho")
    except ValueError as erro:
        messages.error(request, str(erro))
        return redirect("pedidos:carrinho")

    request.session["carrinho"] = {}
    messages.success(request, f"Pedido #{pedido.id} realizado com sucesso!")
    return redirect("pedidos:pedido_sucesso", id=pedido.id)

@login_required
def pedido_sucesso(request, id):
    pedido = get_object_or_404(Pedido, id=id, usuario=request.user)
    return render(request, "pedidos/pedido_sucesso.html", {"pedido": pedido})

@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-id")
    return render(request, "pedidos/meus_pedidos.html", {"pedidos": pedidos})

@login_required
def pedido_detalhe(request, id):
    pedido = get_object_or_404(Pedido.objects.prefetch_related("itens__produto", "itens__variacao"), id=id, usuario=request.user)
    return render(request, "pedidos/pedido_detalhe.html", {"pedido": pedido})