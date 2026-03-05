from django.db import models
from clientes.models import Cliente
from veiculos.models import Veiculo
from motoristas.models import Motorista
from passeios.models import Passeio


class Agendamento(models.Model):

    class TipoServico(models.TextChoices):
        TRANSFER_IN        = 'transfer_in',        'Transfer In (chegada)'
        TRANSFER_OUT       = 'transfer_out',        'Transfer Out (saída)'
        TRANSFER_IDA_VOLTA = 'transfer_ida_volta',  'Transfer Ida + Volta'
        CITY_TOUR          = 'city_tour',           'City Tour'

    class Status(models.TextChoices):
        PENDENTE   = 'pendente',   'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        CONCLUIDO  = 'concluido',  'Concluído'
        CANCELADO  = 'cancelado',  'Cancelado'

    class Pagamento(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PARCIAL  = 'parcial',  'Parcial (sinal pago)'
        PAGO     = 'pago',     'Pago integralmente'

    cliente   = models.ForeignKey(Cliente,   on_delete=models.PROTECT, related_name='agendamentos')
    veiculo   = models.ForeignKey(Veiculo,   on_delete=models.PROTECT, related_name='agendamentos')
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, related_name='agendamentos')
    passeio   = models.ForeignKey(Passeio,   on_delete=models.PROTECT, related_name='agendamentos', blank=True, null=True)

    tipo_servico      = models.CharField(max_length=30, choices=TipoServico.choices)
    data_hora         = models.DateTimeField()
    endereco_embarque = models.CharField(max_length=300)
    destino           = models.CharField(max_length=300)
    codigo_voo        = models.CharField(max_length=20, blank=True, null=True)

    num_adultos      = models.PositiveIntegerField(default=1)
    num_adolescentes = models.PositiveIntegerField(default=0)
    num_criancas     = models.PositiveIntegerField(default=0)

    malas_despachadas = models.PositiveIntegerField(default=0)
    malas_mao         = models.PositiveIntegerField(default=0)
    reboque           = models.BooleanField(default=False)

    valor_total  = models.DecimalField(max_digits=10, decimal_places=2)
    valor_sinal  = models.DecimalField(max_digits=10, decimal_places=2)

    status    = models.CharField(max_length=20, choices=Status.choices,    default=Status.PENDENTE)
    pagamento = models.CharField(max_length=20, choices=Pagamento.choices, default=Pagamento.PENDENTE)

    observacoes = models.TextField(blank=True)
    criado_em   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_hora']

    @property
    def num_passageiros(self):
        return self.num_adultos + self.num_adolescentes + self.num_criancas

    @property
    def valor_restante(self):
        return self.valor_total - self.valor_sinal

    def __str__(self):
        return f'OS #{self.pk:04d} — {self.cliente} — {self.data_hora:%d/%m/%Y %H:%M}'


class Passageiro(models.Model):

    class Tipo(models.TextChoices):
        ADULTO      = 'adulto',      'Adulto'
        ADOLESCENTE = 'adolescente', 'Adolescente'
        CRIANCA     = 'crianca',     'Criança'

    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='passageiros')
    nome        = models.CharField(max_length=200)
    tipo        = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ADULTO)
    documento   = models.CharField(max_length=30, blank=True, null=True)
    telefone    = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'