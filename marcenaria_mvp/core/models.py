from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Orcamento(models.Model):
    STATUS = [
        ('rascunho', 'Rascunho'),
        ('enviado', 'Enviado'),
        ('aprovado', 'Aprovado')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='rascunho')

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome}"

class ItemOrcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, related_name='itens', on_delete=models.CASCADE)
    material = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.material} ({self.quantidade})'

class ImagemOrcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='orcamento_imagens/')

    def __str__(self):
        return f'Imagem para {self.orcamento.id}'
