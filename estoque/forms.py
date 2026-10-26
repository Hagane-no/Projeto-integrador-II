
from django import forms
from .models import Movimentacao, Produto, Categoria


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'observacao']
        widgets = {
            'produto': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'tipo': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                }
            ),
            'observacao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Observação opcional',
                }
            ),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']

        if quantidade <= 0:
            raise forms.ValidationError(
                'A quantidade deve ser maior que zero.'
            )

        return quantidade


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'categoria',
            'quantidade',
            'quantidade_minima',
            'preco',
        ]
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome do produto',
                }
            ),
            'categoria': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                }
            ),
            'quantidade_minima': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                }
            ),
            'preco': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'step': '0.01',
                }
            ),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome da categoria',
                }
            ),
        }
