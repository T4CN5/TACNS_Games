from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    # Agora 'pai' existe no Model e pode ser exibido e filtrado aqui
    list_display = ['nome', 'slug', 'pai']
    list_filter = ['pai']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Exibindo os campos corretos na tabela, incluindo a data de cadastro
    list_display = ['nome', 'categoria', 'preco', 'estoque', 'ativo', 'plataforma', 'tamanho', 'data_cadastro']
    list_editable = ['categoria', 'preco', 'estoque', 'ativo']
    list_filter = ['ativo', 'categoria', 'plataforma']
    search_fields = ['nome', 'descricao']
    # Ordena os produtos do mais novo para o mais antigo na listagem
    ordering = ['categoria', 'plataforma']
