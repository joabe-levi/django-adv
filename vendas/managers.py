from django.db import models
from django.db.models import Max, Avg, Min, Count


class VendaManager(models.Manager):
    def media(self):
        return self.aggregate(Avg('valor')).get('valor__avg')

    def media_desconto(self):
        return self.aggregate(Avg('desconto')).get('desconto__avg')

    def minimo(self):
        return self.aggregate(Min('valor')).get('valor__min')

    def maximo(self):
        return self.aggregate(Max('valor')).get('valor__max')

    def numero_pedidos(self):
        return self.aggregate(Count('id')).get('id__count')

    def numero_pedidos_nfe(self):
        return self.filter(nfe_emitida=True).aggregate(Count('id')).get('id__count')