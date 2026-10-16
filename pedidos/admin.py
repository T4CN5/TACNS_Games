from django.contrib import admin
from .models import Pedido, ItemPedido

# Register your models here.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("preco_unitario",)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "status")
    list_filter = ("status", "data_criacao")
    search_fields = ("usuario_username", "id")
    inlines = [ItemPedidoInline]

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade", "preco_unitario")
    list_filter = ("pedido", "produto")
    search_fields = ("pedido_id", "produto_nome")