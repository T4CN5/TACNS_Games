from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path("carrinho/", views.carrinho, name="carrinho"),
    path("carrinho/adicionar/<int:id>/",
        views.adicionar_carrinho,
        name="adicionar_carrinho"
    ),
    path(
        "carrinho/remover/<int:id>/",
        views.remover_carrinho,
        name="remover_carrinho"
    ),
    path(
        "carrinho/excluir/<int:id>/",
        views.excluir_carrinho,
        name="excluir_carrinho"
    ),
    path(
        "finalizar/",
        views.finalizar_pedido,
        name="finalizar_pedido"
    ),
    path(
        "pedido/<int:id>/sucesso/",
        views.pedido_sucesso,
        name="pedido_sucesso"
    ),
    path(
        "meus-pedidos/",
        views.meus_pedidos,
        name="meus_pedidos"
    ),
    path(
        "meus-pedidos/<int:id>/",
        views.pedido_detalhe,
        name="pedido_detalhe"
    ),
]