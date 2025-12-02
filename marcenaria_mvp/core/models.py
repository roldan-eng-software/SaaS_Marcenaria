from django.db import models

class Cliente(models.Model):
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

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    itens = models.JSONField(default=list)  # [{"material": "...", "qtd": 2, "preco_unit": 150}]
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='rascunho')
    imagens = models.JSONField(default=list)  # [{"s3_url": "...", "descricao": "..."}]

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome}"
