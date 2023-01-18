from django.db import models
from django.db.models import F, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from clientes.models import Person
from produtos.models import Produto
from .managers import VendaManager


class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    nfe_emitida = models.BooleanField(default=False)

    objects = VendaManager()

    class Meta:
        permissions = (
            ('Seta Nf-e', 'Usuário pode alterar parametro Nf-e'),
            ('ver_dashboard', 'Pode visualizar o dashboard'),
            ('Permissão3', 'Permissão 3')
        )


    def calcular_total(self):
        total = self.itemdopedido_set.aggregate(
            total=Sum(F('quantidade') * F('produto__preco') - F('desconto'), output_field=models.FloatField())
        ).get('total') or 0

        total -= float(self.impostos) - float(self.desconto)
        Venda.objects.filter(id=self.id).update(valor=total)

    # @property
    # def get_total(self):
    #     total = 0
    #     for produto in self.produtos.all():
    #         total += produto.preco
    #
        # return (total - self.desconto) - self.impostos

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField(default=0)
    desconto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.venda.numero} - {self.produto.descricao}'


@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total(sender, instance, **kwargs):
    instance.venda.calcular_total()


@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance, **kwargs):
    instance.calcular_total()