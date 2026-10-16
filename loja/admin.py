from django.contrib import admin
from .models import Produto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "pai")
    search_fields = ("nome",)
    list_filter = ("pai",)
    ordering = ("nome",)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "estoque", "data_cadastro")
    search_fields = ("nome", "descricao")
    list_filter = ("categoria", "data_cadastro")
    ordering = ("-data_cadastro",)
