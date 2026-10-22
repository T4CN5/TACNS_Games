from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    # Campos específicos para Jogos
    plataforma = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: PC, PS5, Retro")
    digital = models.BooleanField(default=False, help_text="Marque se for um jogo por download")

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome})"

# NOVA TABELA PARA OS TAMANHOS (VARIAÇÕES)
class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    nome = models.CharField(max_length=50, help_text='Ex: P, M, G, GG ou Único')
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}"