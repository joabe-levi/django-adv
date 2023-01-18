from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Venda


class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Acesso negado! Você precisa de permissão.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        vendas = Venda.objects
        contexto = {
            'media': vendas.media(),
            'media_desconto': vendas.media_desconto(),
            'minimo': vendas.minimo(),
            'maximo': vendas.maximo(),
            'qtd_notas_emitidas': vendas.numero_pedidos_nfe()
        }
        return render(request, 'vendas/dashboard.html', contexto)
