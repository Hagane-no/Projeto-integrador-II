from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')])
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    status_pedido = models.CharField(max_length=20, default='FECHADO')

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} ({self.quantidade})"
