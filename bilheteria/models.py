from django.db import models
from django.contrib.auth.models import User

class Filme(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    sinopse = models.TextField(verbose_name="Sinopse")
    duracao_minutos = models.IntegerField(verbose_name="Duração (min)")
    classificacao = models.CharField(max_length=10, verbose_name="Classificação Indicativa", choices=[
        ('L', 'Livre'),
        ('10', '10 anos'),
        ('12', '12 anos'),
        ('14', '14 anos'),
        ('16', '16 anos'),
        ('18', '18 anos'),
    ])
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name="Poster do Filme")

    def __str__(self):
        return self.titulo

class Sessao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, verbose_name="Filme")
    sala = models.CharField(max_length=50, verbose_name="Sala de Exibição")
    horario = models.DateTimeField(verbose_name="Horário da Sessão")

    def __str__(self):
        return f"{self.filme.titulo} - {self.horario.strftime('%d/%m %H:%M')}"

    class Meta:
        verbose_name = "Sessão"
        verbose_name_plural = "Sessões"

class Ingresso(models.Model):
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, verbose_name="Sessão")
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendedor")
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name="Data da Venda")
    tipo = models.CharField(max_length=20, verbose_name="Tipo de Ingresso", choices=[
        ('INTEIRA', 'Inteira'),
        ('MEIA', 'Meia'),
    ], default='INTEIRA')
    valor_pago = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Pago", default=0.00)
    forma_pagamento = models.CharField(max_length=50, verbose_name="Forma de Pagamento", choices=[
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO', 'Cartão'),
        ('PIX', 'PIX'),
    ])

    def __str__(self):
        return f"Ingresso #{self.id} - {self.sessao}"
