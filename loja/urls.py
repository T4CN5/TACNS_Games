from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    # Institucionais
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    
    # Catálogo e CRUD
    path('produtos/', views.produtos, name="produtos"),
    path('produtos/novo/', views.produto_novo, name="produto_novo"),
    path('produtos/esgotados/', views.produtos_esgotados, name="produtos_esgotados"),
    path('produtos/<int:id>/', views.produto_detalhe, name="produto_detalhe"),
    path('produtos/<int:id>/editar/', views.produto_editar, name="produto_editar"),
    path('produtos/<int:id>/excluir/', views.produto_excluir, name="produto_excluir"),
    path('produtos/categoria/<int:id>/', views.produtos_categoria, name="produtos_categoria"),
]
