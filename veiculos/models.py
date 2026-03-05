from django.db import models

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    capacidade = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"