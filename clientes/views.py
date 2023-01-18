from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from clientes.models import Person
from produtos.models import Produto
from vendas.models import Venda
from .forms import PersonForm


@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    1/0
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})


class PersonList(LoginRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        primeiro_acesso = self.request.session.get('primeiro_acesso', False)
        if not primeiro_acesso:
            context['message'] = 'seja bem vindo ao seu primeiro acesso hoje.'
            self.request.session['primeiro_acesso'] = True
        else:
            context['message'] = 'Você já acessou hoje.'

        return context


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person

    def get_object(self, queryset=None):
        return Person.objects.select_related('doc').get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['timezone'] = datetime.now()
        context['vendas'] = Venda.objects.filter(pessoa_id=self.object.id)
        context['minha_var'] = 'Desenvolvimento web com Django 2.x'
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = '/clientes/person_list'

    def get_success_url(self):
        return reverse_lazy('person_list_cbv')


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']

    def get_success_url(self):
        return reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('clientes.deletar_clientes',)
    model = Person

    def get_success_url(self):
        return reverse_lazy('person_list_cbv')


class ProdutoBulk(LoginRequiredMixin, View):
    def get(self, request):
        produtos = ['Banana', 'Maçã', 'Limão', 'Laranja', 'Pêra', 'Melãncia']
        lista_produtos = []
        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            lista_produtos.append(p)
        Produto.objects.bulk_create(lista_produtos)
        return HttpResponse('funcionou')