from django.db import models

class Passeio(models.Model):
    nome          = models.CharField(max_length=200)
    descricao     = models.TextField(blank=True)
    duracao_horas = models.PositiveIntegerField(default=4)
    valor_onix    = models.DecimalField(max_digits=8, decimal_places=2)
    valor_spin    = models.DecimalField(max_digits=8, decimal_places=2)
    ativo         = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Passeio'
        verbose_name_plural = 'Passeios'
        ordering = ['nome']

    def __str__(self):
        return self.nome