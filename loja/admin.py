from django.contrib import admin
from .models import Categoria, Produto, Variacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'slug', 'pai']
    list_filter = ['pai']

# Adiciona os tamanhos dentro da tela de edição do Produto
class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'estoque', 'ativo', 'plataforma', 'data_cadastro']
    list_editable = ['categoria', 'preco', 'estoque', 'ativo']
    list_filter = ['ativo', 'categoria', 'plataforma']
    search_fields = ['nome', 'descricao']
    ordering = ['categoria', 'plataforma']
    inlines = [VariacaoInline] # Carrega as variações aqui