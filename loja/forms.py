from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Removido o 'tamanho' da lista de fields
        fields = [
            'nome', 'descricao', 'preco', 'categoria', 'estoque', 
            'imagem', 'ativo', 'plataforma', 'digital'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plataforma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PC, PS5, Retro'}),
            'digital': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
