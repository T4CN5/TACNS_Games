from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    # Permite categorias filhas (ex: Categoria 'PS5' dentro de 'Jogos')
    pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategorias')

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2) 
    imagem = models.ImageField(upload_to='produtos/')
    estoque = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    # Registra automaticamente a data em que o produto foi cadastrado
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    # Campos específicos para Jogos
    plataforma = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: PC, PS5, Retro")
    digital = models.BooleanField(default=False, help_text="Marque se for um jogo por download")

    # Campos específicos para Roupas/Acessórios
    tamanho = models.CharField(max_length=10, blank=True, null=True, help_text="Ex: P, M, G, GG")

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome})"
