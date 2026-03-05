from django.db import models

class Motorista(models.Model):
    TIPO_CHOICES = [
        ('proprio', 'Próprio F&F'),
        ('parceiro', 'Parceiro de Agência'),
        ('freelancer', 'Freelancer'),
    ]

    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    cnh = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    empresa = models.CharField(max_length=150, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome