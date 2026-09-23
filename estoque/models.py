from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    quantidade_atual = models.IntegerField(default=0)
    quantidade_minima = models.IntegerField(default=0)
    unidade_medida = models.CharField(max_length=50, default='Unidade')

    def __str__(self):
        return self.nome

    @property
    def precisa_reposicao(self):
        return self.quantidade_atual < self.quantidade_minima


class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.tipo == 'ENTRADA':
                self.produto.quantidade_atual += self.quantidade
            elif self.tipo == 'SAIDA':
                nova_qtd = self.produto.quantidade_atual - self.quantidade
                self.produto.quantidade_atual = max(0, nova_qtd)
            self.produto.save()
        super().save(*args, **kwargs)
